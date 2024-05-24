from modules.config import db
from datetime import datetime
# Definición del modelo de reclamo
class Reclamo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    estado = db.Column(db.String(20), nullable=False, default='Pendiente')
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    contenido = db.Column(db.Text, nullable=False)
    adherentes = db.Column(db.Integer, default=0)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    foto = db.Column(db.String(120), nullable=True)

    def sumar_adherentes(self, adherentes):
        pass