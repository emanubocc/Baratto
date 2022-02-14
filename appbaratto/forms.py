from flask_wtf import FlaskForm
from wtforms import (StringField, SubmitField, PasswordField, EmailField, SelectField, HiddenField, TextAreaField)
from flask_wtf.file import FileField, FileRequired, FileAllowed

from wtforms.validators import DataRequired
from .utility import PROVINCIE_CHOICES


# Definizione campi form di Login
class LoginForm(FlaskForm):
    loginEmail = EmailField("", validators=[DataRequired()], description="La tua email")
    loginPassword = PasswordField("", validators=[DataRequired()], description="La tua password")
    submit = SubmitField("Login")


# Definizione campi form di Registrazione
class RegistrationForm(FlaskForm):
    nome = StringField("", validators=[DataRequired()], description="Nome")
    cognome = StringField("", validators=[DataRequired()], description="Cognome")
    password = PasswordField("", validators=[DataRequired()], description="Password")
    password2 = PasswordField("", validators=[DataRequired()], description="Ripeti Password")
    regEmail = EmailField("", validators=[DataRequired()], description="Email")
    citta = StringField("", validators=[DataRequired()], description="Città")
    provincia = SelectField("", validators=[DataRequired()], choices=PROVINCIE_CHOICES)
    via = StringField("", validators=[DataRequired()], description="Via")
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
    nome = StringField("", validators=[DataRequired()], description="Nome oggetto")
    desc = TextAreaField("", validators=[DataRequired()], description="Descrizione oggetto...")
    provincia = SelectField("", validators=[DataRequired()], choices=PROVINCIE_CHOICES)
    image = FileField(u'image',  validators=[FileRequired(),  FileAllowed(['jpg', 'png'], 'Images only!')])
    submit = SubmitField("Invia")

