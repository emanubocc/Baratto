from flask import Blueprint, render_template, redirect
from flask_login import login_required, current_user
from .models import Messaggi, Utente
from sqlalchemy import or_
from . import db

messages = Blueprint('messages', __name__)


@messages.route('/profilo/messaggia/destinatario/<int:user_id_receiver>')
@login_required
def send_message(user_id_receiver):

    #Query che prende tutti i messaggi inviati e ricevuti dai due interlocutori
    msgs = Messaggi.query\
    .filter(((Messaggi.Mittente==current_user.id) & (Messaggi.Destinatario==user_id_receiver))\
         | ((Messaggi.Mittente == user_id_receiver) & (Messaggi.Destinatario == current_user.id))).order_by(Messaggi.id).all()

    return render_template('send-message.html', msgs=msgs)


@messages.route('/profilo/messaggia')
@login_required
def view_message():

    msgs = Messaggi.query.filter_by(Destinatario=current_user.id).group_by(Messaggi.Mittente).all()
    users_msg = {}


    for msg in msgs:
        nome_utente = (Utente.query.filter_by(id=msg.Mittente).first()).Nome
        num_msg = Messaggi.query.filter_by(Mittente=msg.Mittente, Destinatario=current_user.id).count()
        users_msg[msg.Mittente] = ( nome_utente, num_msg )


    return render_template('view-messages.html', users_msg=users_msg)