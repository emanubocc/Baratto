from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import UserMixin


# Classe Utente
class Utente(db.Model, UserMixin):

    # Create a table in the db
    __tablename__ = 'Utente'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Nome = db.Column(db.String(64), nullable=False)
    Cognome = db.Column(db.String(64), nullable=False)
    Password_hash = db.Column(db.String(128))
    Email = db.Column(db.String(120), nullable=False, unique=True)
    Citta = db.Column(db.String(30), nullable=False)
    Provincia = db.Column(db.String(30), nullable=False)
    Via = db.Column(db.String(120), nullable=False)

    def __init__(self, nome, cognome, password, email, citta, provincia, via):

        self.Nome = nome
        self.Cognome = cognome
        self.Password_hash = generate_password_hash(password)
        self.Email = email
        self.Citta = citta
        self.Provincia = provincia
        self.Via = via

    def __repr__(self):
        return f'<Utente {self.id + self.Nome + self.Cognome + self.Password_hash + self.Email + self.Citta + self.Provincia + self.Via!r}>'


# Classe Prodotto
class Oggetto(db.Model):

    # Create a table in the db
    __tablename__ = 'Oggetto'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Nome = db.Column(db.String(64), nullable=False)
    Desc = db.Column(db.String(250), nullable=False)
    Img = db.Column(db.String(100), unique=True, nullable=False)
    Provincia = db.Column(db.String(30), nullable=False)

    def __init__(self, nome, desc, img, provincia):

        self.Nome = nome
        self.Desc = desc
        self.Img = img
        self.Provincia = provincia

    def __repr__(self):
        return f'<Prodotto {self.id + self.Nome + self.Desc + self.Img + self.Provincia!r}>'