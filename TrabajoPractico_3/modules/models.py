from modules.config import db
from datetime import datetime
from sqlalchemy import Column, Integer, String, Float

#Definimos las tablas con als que trabajaremos: 

class PersonaDB(db.Model):
    __tablename__ = 'personas'
    #Persona
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    apellido = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)


    #parámetro propio de usuario:
    claustro = db.Column(db.String(20), nullable=False)

    #Parámetro propio de jefe
    departamento = db.Column(db.String(50), nullable=True)

class ReclamoDB(db.Model):
    __tablename__ = 'reclamos'
    id = db.Column(db.Integer, primary_key=True)
    estado = db.Column(db.String(20), nullable=False, default='pendiente')
    tiempo_resolucion = db.Column(db.Integer, nullable=True)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    contenido = db.Column(db.Text, nullable=False)
    adherentes = db.Column(db.Integer, default=0)
    user_id = db.Column(db.Integer, db.ForeignKey('personas.id'), nullable=False)
    foto = db.Column(db.String(120), nullable=True)
    departamento = db.Column(db.String(50))

    #relación con la tabla de usuarios (Personas)
    usuario = db.relationship('PersonaDB', backref=db.backref('reclamos', lazy=True))