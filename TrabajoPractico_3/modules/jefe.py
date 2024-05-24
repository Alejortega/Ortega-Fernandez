from modules.persona import Persona
from modules.config import db

class Jefe(Persona, db.Model):
    departamento = db.Column(db.String(50), nullable=False)

    def manejar_reclamo():
        pass
    def generar_estadisticas():
        pass
    def generar_reporte():
        pass