from flask import Flask, redirect, url_for, render_template, session
from flask_wtf import FlaskForm
from wtforms.fields.html5 import DateField
from wtforms.fields.simple import TextField
from wtforms import validators, SubmitField
import pymongo 
import datetime



app = Flask(__name__)

app.config['SECRET_KEY'] = "123*"
app.config['MONGO_URI']= 'mongodb://localhost:27017/final'

class InfoForm(FlaskForm):
    nombre = TextField('Nombre:', validators=(validators.DataRequired(),))
    apellido = TextField('Apellido:', validators=(validators.DataRequired(),))
    telefono = TextField('Telefono:', validators=(validators.DataRequired(),))
    correo = TextField('Correo:', validators=(validators.DataRequired(),))
    startdate = DateField('Fecha:', format='%Y-%m-%d', validators=(validators.DataRequired(),))
    submit = SubmitField('Enviar')

# Establece conexion con servidor MongoDB
con = pymongo.MongoClient("mongodb://localhost:27017/")
db = con["final"] # Base de datos
col = db["citas"] # Coleccion


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
def response():
    cursor = col.find({})
    id = 0
    for el in cursor:
        citas = {}
        citas[id] = el
        id += 1 
    return render_template('response.html', citas = list(citas.values())[-1])


if __name__ == '__main__':
   app.run(debug = True)