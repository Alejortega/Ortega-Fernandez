from modules.config import db
from modules.usuario import Usuario
from modules.reclamo import Reclamo

class Gestor:
    
    def guardar_user(self, usuario_data):
        nuevo_usuario = Usuario(nombre=usuario_data['nombre'], apellido=usuario_data['apellido'], email=usuario_data['email'], username=usuario_data['username'], password=usuario_data['password'], claustro=usuario_data['claustro'])
         
        db.session.add(nuevo_usuario)
        db.session.commit()

    def guardar_reclamo(self, reclamo_data):
        nuevo_reclamo = Reclamo(estado=reclamo_data['estado'], contenido=reclamo_data['contenido'], user_id=reclamo_data['user_id'], foto=reclamo_data.get('foto'))
        db.session.add(nuevo_reclamo)
        db.session.commit()