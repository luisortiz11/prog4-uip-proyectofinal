from flask import Flask, render_template, request
from flask_restful import Resource, Api, reqparse
import pandas as pd
import ast
import requests


app = Flask(__name__)
api = Api(app)


class Citas(Resource):
    def get(self):
        data = pd.read_csv('citasdb.csv')
        data = data.to_dict()
        return {'citas': data}, 200

    def post(self):
        print("entre")
        parser = reqparse.RequestParser()

        parser.add_argument('Id', type=str, required=True)
        parser.add_argument('Nombre', type=str, required=True)
        parser.add_argument('Apellido', type=str, required=True)
        parser.add_argument('Cedula', type=str, required=True)
        parser.add_argument('Telefono', type=str, required=True)
        parser.add_argument('FechaCita', type=str, required=True)

        args = parser.parse_args()
        print(args['Id'])
        new_data = pd.DataFrame({
            'Id': [args['Id']],
            'Nombre': [args['Nombre']],
            'Apellido': [args['Apellido']],
            'Cedula': [args['Cedula']],
            'Telefono': [args['Telefono']],
            'FechaCita': [args['FechaCita']],
        })

        data = pd.read_csv('citasdb.csv')
        data = data.append(new_data, ignore_index=True)
        data.to_csv('citasdb.csv', index=False)
        return {'data': data.to_dict()}, 200

    # añadir metodo delete
    pass


api.add_resource(Citas, '/citas')

# usar method tipo DELETE


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        users = requests.get("http://127.0.0.1:5000/citas").json()
        id = len(users['citas']['Id']) + 1
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        cedula = request.form['cedula']
        telefono = request.form['telefono']
        fecha = request.form['fecha']

        requests.post("http://127.0.0.1:5000/citas", params={
                      'Id': id, 'Nombre': nombre, 'Apellido': apellido, 'Cedula': cedula, 'Telefono': telefono, 'FechaCita': fecha})
        return render_template("index.html")

    return render_template("index.html")


@app.route('/mostrarcitas', methods=['GET', 'POST'])
def mostrarcitas():
    users = requests.get("http://127.0.0.1:5000/citas").json()
    nombres = users['citas']['Nombre']
    for nombre in nombres:
        print(nombres[nombre])

    return render_template("mostrarcitas.html", nombres=users['citas']['Nombre'], apellidos=users['citas']['Apellido'], cedulas=users['citas']['Cedula'], telefonos=users['citas']['Telefono'], fechas=users['citas']['FechaCita'])


if __name__ == '__main__':
    app.run()
