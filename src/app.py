from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from datetime import datetime

app = Flask(__name__)

# Conecxión a la base de datos
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root:crisda24@localhost/car_microservice'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

db = SQLAlchemy(app) # Interactura con la base de datos
ma = Marshmallow(app) # Crear esquema


class Cars(db.Model):
    id= db.Column(db.Integer, primary_key=True)
    marca= db.Column(db.String(70))
    modelo= db.Column(db.String(70))
    anio= db.Column(db.Integer)
    puertas= db.Column(db.String(70))
    color= db.Column(db.String(70))
    transmision= db.Column(db.String(70))
    existencia= db.Column(db.Integer)
    precio= db.Column(db.Integer)
    creado= db.Column(db.DateTime, index=True, default=datetime.now)
    
    def __init__(self,marca, modelo, anio, puertas, color, transmision, existencia, precio):
        self.marca = marca
        self.modelo = modelo
        self.anio = anio
        self.puertas = puertas
        self.color= color
        self.transmision = transmision
        self.existencia = existencia
        self.precio = precio
        
db.create_all()

class CarSchema(ma.Schema):
    class Meta:
        fields = ('id', 'creado', 'marca', 'modelo', 'anio', 'puertas',  'color',  'transmision',  'existencia', 'precio' )
    
car_schema = CarSchema()
cars_schema = CarSchema(many=True)

@app.route('/cars', methods=['POST'])       
def createCar():
    marca      = request.json['marca']
    modelo      = request.json['modelo']
    anio        = request.json['anio']
    puertas     = request.json['puertas']
    color       = request.json['color']
    transmision = request.json['transmision']
    existencia  = request.json['existencia']
    precio      = request.json['precio']
        
    new_car = Cars(marca, modelo, anio, puertas, color, transmision, existencia, precio)
    db.session.add(new_car)
    db.session.commit()
    
    return car_schema.jsonify(new_car)

@app.route('/cars', methods=['GET'])
def get_cars():
    all_cars=Cars.query.all()
    result = cars_schema.dump(all_cars)
    return jsonify(result)

@app.route('/cars/<id>', methods=['GET'])
def get_car(id):
    car = Cars.query.get(id)
    return car_schema.jsonify(car)

@app.route('/cars/<id>', methods=['PUT'])
def update_car(id):
    car=Cars.query.get(id)
    marca       = request.json['marca']
    modelo      = request.json['modelo']
    anio        = request.json['anio']
    puertas     = request.json['puertas']
    color       = request.json['color']
    transmision = request.json['transmision']
    existencia  = request.json['existencia']
    precio      = request.json['precio']
    
    car.marca       = marca
    car.modelo      = modelo
    car.anio        = anio
    car.puertas     = puertas
    car.color       = color
    car.transmision = transmision
    car.existencia  = existencia
    car.precio      = precio
    
    db.session.commit()
    return car_schema.jsonify(car)

@app.route('/cars/<id>', methods=['DELETE'])
def delete_car(id):
    car =  Cars.query.get(id)
    db.session.delete(car)
    db.session.commit()
    return car_schema.jsonify(car)
    
if __name__=="__main__":
    app.run(debug =True)
