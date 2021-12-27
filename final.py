from flask import Flask, redirect, render_template, session
from flask_wtf import FlaskForm
from wtforms.fields.html5 import DateField
from wtforms.fields.simple import TextField
from wtforms import validators, SubmitField
from flask_mail import Mail, Message
import pymongo 
import datetime
from threading import Thread


app = Flask(__name__)

app.config['SECRET_KEY'] = "123*"
app.config['MONGO_URI']= 'mongodb://localhost:27017/final'

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'smiledr507@gmail.com'
app.config['MAIL_PASSWORD'] = 'xHnfXYUDfNNsD8M'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail = Mail(app)
class InfoForm(FlaskForm):
    nombre = TextField('Nombre:', validators=(validators.DataRequired(),))
    apellido = TextField('Apellido:', validators=(validators.DataRequired(),))
    telefono = TextField('Telefono:', validators=(validators.DataRequired(),))
    correo = TextField('Correo:', validators=(validators.DataRequired(),))
    startdate = DateField('Fecha:', format='%Y-%m-%d', validators=(validators.DataRequired(),))
    submit = SubmitField('Enviar')
    
class Peticion(FlaskForm):
    correo = TextField('Correo:', validators=(validators.DataRequired(),))
    submit = SubmitField('Enviar')

# Establece conexion con servidor MongoDB
con = pymongo.MongoClient("mongodb://localhost:27017/")
db = con["final"] # Base de datos
col = db["citas"] # Coleccion

def msg_send(msg,msg_body):
    msg = msg
    msg.body = msg_body
    return mail.send(msg)

@app.route('/' , methods=[ 'GET','POST'])
def menu():
    form = InfoForm()
    if form.validate_on_submit():
        session['nombre'] = form.nombre.data
        session['apellido'] = form.apellido.data
        session['telefono'] = form.telefono.data
        session['correo'] = form.correo.data
        session['startdate'] = form.startdate.data
        col.insert_one({'nombre': session['nombre'], 'apellido': session['apellido'], 
        'telefono': session['telefono'], 'correo': session['correo'], 'fecha' : datetime.datetime.combine(session['startdate'], datetime.time.min)})
        return redirect('/cita')
    return render_template('menu.html', form=form)

@app.route('/cita' , methods=[ 'GET','POST'])
async def response():
    nombre = session.get('nombre')
    apellido = session.get('apellido')
    telefono = session.get('telefono')
    correo = session.get('correo')
    fecha = session.get('startdate')
    
    respuesta = "Hola {} {}, se ha registrado la cita satisfactoriamente para el dia {}, te enviaremos un correo de confirmacion a {}. Posteriormente te llamaremos a {} para informarte la disponibilidad durante el día.".format(nombre,apellido,fecha, correo,telefono )
    #msg_send(Message('Cita para Odontología', sender ='smiledr507@gmail.com', recipients = correo.split()), "Confirmación de cita," + respuesta)
    #msg_send(Message('Cita para Odontología', sender ='smiledr507@gmail.com', recipients =  'smiledr507@gmail.com'.split()), "Fecha de cita {} Llamar a {} {} al {} para confimar hora de la cita".format(fecha, nombre, apellido,telefono ))

    return render_template('response.html', citas = respuesta)


@app.route('/citas' , methods=[ 'GET','POST'])
def qery():
    form = Peticion()
    if form.validate_on_submit():
        session['correobusca'] = form.correo.data
    
        return redirect('/resultado')
    return render_template('busca.html', form=form)

@app.route('/resultado' , methods=[ 'GET','POST'])
def busca():
    correo = session.get('correobusca')
    citas = col.find_one({"correo": correo})
    respuesta = "Hola {} {}, la cita es el dia {}, te enviaremos un correo de confirmacion a {}. Posteriormente te llamaremos a {} para informarte la disponibilidad durante el día.".format(citas['nombre'], citas['apellido'], citas['fecha'], citas['correo'],citas['telefono'] )
    #msg_send(Message('Cita para Odontología', sender ='smiledr507@gmail.com', recipients = correo.split()), "Confirmación de cita" + respuesta)
    #msg_send(Message('Cita para Odontología', sender ='smiledr507@gmail.com', recipients =  'smiledr507@gmail.com'.split()), "Fecha de cita {} Llamar a {} {} al {} para confimar hora de la cita".format(citas['fecha'], citas['nombre'], citas['apellido'], citas['telefono'] ))

    return render_template('response.html', citas = respuesta)


if __name__ == '__main__':
   app.run(debug = True)

