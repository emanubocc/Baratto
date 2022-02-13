from flask import Blueprint, render_template, flash, redirect, url_for, session, request
from werkzeug.security import check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from .forms import LoginForm, RegistrationForm

from .models import Utente
from . import db


auth = Blueprint('auth', __name__)


@auth.route('/registrazione', methods=["GET", "POST"])
def registration():
    form_registration = RegistrationForm()
    if form_registration.validate_on_submit():

        nome = form_registration.nome.data
        cognome = form_registration.cognome.data
        regEmail = form_registration.regEmail.data
        password = form_registration.password.data
        password2 = form_registration.password2.data
        citta = form_registration.citta.data
        provincia = form_registration.provincia.data
        via = form_registration.via.data

        utente = Utente.query.filter_by(Email=regEmail).first()

        if utente:
            flash('Email già estistente.', category='error')
        elif len(regEmail) < 4:
            flash('Il campo email deve essere maggiore di 3 caratteri', category='error')
        elif len(nome) < 2:
            flash('Il campo nome deve essere maggiore di 1 carattere', category='error')
        elif password != password2:
            flash('Le password inserite non combaciano', category='error')
        elif len(password) < 6:
            flash('La password deve essere almeno 6 caratteri', category='error')
        else:
            new_user = Utente(nome, cognome, password, regEmail, citta, provincia, via)
            db.session.add(new_user)
            db.session.commit()
            flash('Account creato con successo!', category='success')

    return render_template('signup.html', form=form_registration)


@auth.route('/login', methods=["GET", "POST"])
def login():
    form_login = LoginForm()

    if form_login.validate_on_submit():
        loginEmail = form_login.loginEmail.data
        loginPassword = form_login.loginPassword.data

        utente = Utente.query.filter_by(Email=loginEmail).first()

        if utente:
            if check_password_hash(utente.Password_hash, loginPassword):
                flash('Login effettuato con successo.', category='success')
                login_user(utente, remember=True)
                return redirect(url_for('views.profile'))
            else:
                flash('Password non corretta.', category='error')
        else:
            flash('Email non esistente.', category='error')

    return render_template('login.html', form=form_login)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
