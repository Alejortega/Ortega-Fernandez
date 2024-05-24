from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session

app = Flask("server")

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///base_datos.db'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
SESSION_TYPE = 'filesystem'
app.config.from_object(__name__)
app.config["SESSION_FILE_DIR"] = "./flask_session_cache"
Session(app)


