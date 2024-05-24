from modules.config import db
from modules.persona import Persona

class Usuario(Persona, db.Model):
    claustro = db.Column(db.String(20), nullable=False)


    def crear_reclamo():
        pass

    def adherirse_a_reclamo():
        pass