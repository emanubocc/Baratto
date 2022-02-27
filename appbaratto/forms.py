from flask_wtf import FlaskForm
from wtforms import (StringField, SubmitField, PasswordField, EmailField, SelectField, HiddenField, TextAreaField,MultipleFileField)

from wtforms.validators import DataRequired, Length
from .utility import PROVINCIE_CHOICES


# Definizione campi form di Login
class LoginForm(FlaskForm):
    loginEmail = EmailField("", validators=[DataRequired()], description="La tua email")
    loginPassword = PasswordField("", validators=[DataRequired()], description="La tua password")
    submit = SubmitField("Login")


# Definizione campi form di Registrazione
class RegistrationForm(FlaskForm):
    nome = StringField("", validators=[DataRequired(), Length(min=1, max=64, message='Massimo 64 Caratteri')], description="Nome")
    cognome = StringField("", validators=[DataRequired(), Length(min=1, max=64, message='Massimo 64 Caratteri')], description="Cognome")
    password = PasswordField("", validators=[DataRequired(), Length(min=6, max=12, message='Min 6 caratteri, Max 12')], description="Password")
    password2 = PasswordField("", validators=[DataRequired()], description="Ripeti Password")
    regEmail = EmailField("", validators=[DataRequired(), Length( max=120, message='Max 120 caratteri')], description="Email")
    citta = StringField("", validators=[DataRequired(), Length( max=30, message='Max 30 caratteri')], description="Città")
    provincia = SelectField("", validators=[DataRequired()], choices=PROVINCIE_CHOICES)
    via = StringField("", validators=[DataRequired(), Length( max=120, message='Max 120 caratteri')], description="Via")
    submit = SubmitField("Registrati")


# Form modifica dati personali
class EditForm(FlaskForm):
    password = PasswordField("", validators=[DataRequired()], description="Password")
    password2 = PasswordField("", validators=[DataRequired()], description="Ripeti Password")
    citta = StringField("", validators=[DataRequired()], description="Città")
    provincia = SelectField("", validators=[DataRequired()], choices=PROVINCIE_CHOICES)
    via = StringField("", validators=[DataRequired()], description="Via")
    submit = SubmitField("Modifica")


# Form per inserimento oggetti
class ItemsForm(FlaskForm):
    nome = StringField("", validators=[DataRequired(), Length(min=1, max=64, message='Massimo 64 Caratteri')], description="Nome oggetto")
    desc = TextAreaField("", validators=[DataRequired(),  Length(min=1, max=250, message='Massimo 250 Caratteri')], description="Descrizione oggetto...")
    oggetti_preferiti = TextAreaField("", validators=[DataRequired(),  Length(min=1, max=100, message='Massimo 100 Caratteri')], description="Oggetti che vorresti...")
    provincia = SelectField("", validators=[DataRequired()], choices=PROVINCIE_CHOICES)
    image = MultipleFileField('Images', validators=[DataRequired()] )


    submit = SubmitField("Invia")

class ProposalForm(FlaskForm):
    nome = StringField("", validators=[DataRequired(), Length(min=1, max=64, message='Massimo 64 Caratteri')],description="Nome oggetto")
    desc = TextAreaField("", validators=[DataRequired(), Length(min=1, max=250, message='Massimo 250 Caratteri')],description="Descrizione oggetto...")
    image = MultipleFileField('Images', validators=[DataRequired()])
    submit = SubmitField("Invia")

class MessageForm(FlaskForm):
    contenuto = StringField("", validators=[Length(min=1, max=64, message='Massimo 250 Caratteri')], description="Scrivi il tuo messaggio...")
