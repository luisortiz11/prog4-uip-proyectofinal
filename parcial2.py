from flask import Flask, redirect, url_for, render_template, session
from flask_wtf import FlaskForm
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired
from wtforms import validators, SubmitField
import pymongo 

app = Flask(__name__)

app.config['SECRET_KEY'] = '#$%^&*'

class InfoForm(FlaskForm):
    startdate = DateField('Start Date', format='%Y-%m-%d', validators=(validators.DataRequired(),))
    enddate = DateField('End Date', format='%Y-%m-%d', validators=(validators.DataRequired(),))
    submit = SubmitField('Submit')

# Establece conexion con servidor MongoDB
con = pymongo.MongoClient("mongodb://localhost:27017/")
db = con["final"] # Base de datos
col = db["citas"] # Coleccion

app = Flask(__name__)


def res(a):
    query = col.find_one({"key": a})
    return query

@app.route('/' , methods=[ 'GET','POST'])
def menu():
    form = InfoForm()
    if form.validate_on_submit():
        session['startdate'] = form.startdate.data
        session['enddate'] = form.enddate.data
        return redirect('date')
    return render_template('menu.html', form=form)


@app.route('/api/info/',  methods=['GET'])
def info():
    return jsonify({"Informacion general" : dict(zip(titulo[:3], pan[:3]))} )
 
@app.route('/api/año/<int:number>/',  methods=['GET'])
def vacunas(number):
    query = res(str(number))
    return jsonify({"Vacunaciones" : query})

@app.route('/api/datos/',  methods=['GET'])
def datos():
    dk = {}
    for i in col.find({},{"_id": 0, "key": 1, "value": 1}):
        dk[i["key"]] = i["value"]
    return jsonify({"Vacunaciones por año": dk})

if __name__ == '__main__':
   app.debug = True
   app.run()
   app.run(debug = True)