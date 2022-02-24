from sqlalchemy import Boolean
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

    # Tabella di relazione 1 Utente : N Oggetti
    Oggetto = db.relationship("Oggetto")
    Utente_offerente = db.relationship("Proposta")

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
    Oggetti_preferiti = db.Column(db.String(100), nullable=False)
    Img_1 = db.Column(db.String(75), nullable=False)
    Img_2 = db.Column(db.String(75), nullable=True)
    Img_3 = db.Column(db.String(75), nullable=True)
    Provincia = db.Column(db.String(30), nullable=False)


    # Tabella di relazione 1 Utente : N Oggetti
    id_utente = db.Column(db.Integer, db.ForeignKey('Utente.id'))

    # Tabella di relazione 1 Oggetto : N Proposte
    Proposta = db.relationship("Proposta")


    def __init__(self, nome, desc, oggetti_preferiti, img_1, img_2, img_3, provincia, id_utente):

        self.Nome = nome
        self.Desc = desc
        self.Oggetti_preferiti = oggetti_preferiti
        self.Img_1 = img_1
        self.Img_2 = img_2
        self.Img_3 = img_3
        self.Provincia = provincia
        self.id_utente = id_utente

    def __repr__(self):
        return f'<Prodotto {self.id + self.Nome + self.Desc + self.Img_1 + self.Img_2 + self.Img_3 + self.Provincia!r}>'



# Classe Proposta
class Proposta(db.Model):

    # Create a table in the db
    __tablename__ = 'Proposta'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Nome = db.Column(db.String(64), nullable=False)
    Desc = db.Column(db.String(250), nullable=False)
    Img_1 = db.Column(db.String(75), nullable=False)
    accettata = db.Column(Boolean, unique=False, default=None, nullable=True)

    # Tabella di relazione 1 oggetto : N proposte
    id_oggetto = db.Column(db.Integer, db.ForeignKey('Oggetto.id'))
    id_utente_offerente = db.Column(db.Integer, db.ForeignKey('Utente.id'))

    def __init__(self, nome, desc, img_1, id_oggetto, id_utente_offerente, accettata):

        self.Nome = nome
        self.Desc = desc
        self.Img_1 = img_1
        self.id_oggetto = id_oggetto
        self.id_utente_offerente = id_utente_offerente
        self.accettata = accettata

    def __repr__(self):
        return f'<Proposta {self.id + self.Nome + self.Desc + self.Img_1 + self.id_oggetto + self.id_utente_offerente + self.accettata!r}>'

# Classe Messaggi
class Messaggi(db.Model):

    __tablename__ = 'Messaggio'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Contenuto = db.Column(db.String(250), nullable=False)
    Mittente = db.Column(db.Integer, db.ForeignKey('Utente.id'))
    Destinatario = db.Column(db.Integer, db.ForeignKey('Utente.id'))

    def __init__(self, contenuto, mittente, destinatario):

        self.Contenuto = contenuto
        self.Mittente = mittente
        self.Destinatario = destinatario


    def __repr__(self):
        return f'<Proposta {self.Content + self.Mittente + self.Destinatario!r}>'