from modules.gestores import GestorDB
from modules.config import app, db


#carga de jefes fijos a la base de datos

jefe_maestranza = {
    "nombre": "Mariana",
    "apellido": "Pereira",
    "email": "maestranza@example.com",
    "departamento": "maestranza",
    "username": "Maestranza",
    "password": "maestranza2024",
    #"claustro": "" #quedo como común en la función de guardar persona de gestordb
}

jefe_secretaria = {
    "nombre": "Franco",
    "apellido": "Lopez",
    "email": "secretaria@example.com",
    "departamento": "secretaria técnica",
    "username": "Secretaria",
    "password": "secretaria2024",
    #"claustro": ""
}

jefe_soporte = {
    "nombre": "Luis",
    "apellido": "Torres",
    "email": "soporte@example.com",
    "departamento": "soporte informático",
    "username": "Soporte",
    "password": "soporte2024",
    #"claustro": ""
}



with app.app_context():
    #Guardar los jefes en la base de datos usando el gestor 
    #db.create_all()
    gestordb = GestorDB()
    gestordb.guardar_persona(jefe_maestranza, 'jefe')
    gestordb.guardar_persona(jefe_secretaria, 'jefe')
    gestordb.guardar_persona(jefe_soporte, 'jefe')

#no sé si tiene que ser como antes o así ja
#jefe_maestranza = Jefe(0, "Mariana", "Pereira", "maestranza@example.com", "Maestranza" , "maestranza2024", "maestranza" )
#jefe_soporte = Jefe(0, "Luis","Torres", "soporte@example.com", "Soporte", "soporte2024", "soporte informático ")
#jefe_secretaria = Jefe(0, "Franco", "Lopez", "secretaria@example.com", "Secretaria", "secretaria2024", "secretaria técnica")

#claustro=""




