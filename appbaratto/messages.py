from flask import Blueprint, render_template, redirect
from flask_login import login_required, current_user
from .models import Messaggi, Utente
from sqlalchemy import or_
from . import db

messages = Blueprint('messages', __name__)


@messages.route('/profilo/messaggia/destinatario/<int:item_id>')
@login_required
def send_message(item_id):
    return render_template('send-message.html')


@messages.route('/profilo/messaggia')
@login_required
def view_message():

    msgs = Messaggi.query.filter_by(Destinatario=current_user.id).group_by(Messaggi.Mittente).all()
    users_msg = {}

    for msg in msgs:
        users_msg[msg.Mittente] = (Utente.query.filter_by(id=msg.Mittente).first()).Nome


    return render_template('view-messages.html', users_msg=users_msg)