from flask import Blueprint, render_template, redirect
from flask_login import login_required, current_user

from .crud import insert
from .forms import MessageForm
from .models import Messaggi, Utente


messages = Blueprint('messages', __name__)


@messages.route('/profilo/messaggia/destinatario/<int:user_id_receiver>', methods=["GET", "POST"])
@login_required
def send_message(user_id_receiver):

    #Query che prende tutti i messaggi inviati e ricevuti dai due interlocutori
    msgs = Messaggi.query\
    .filter(((Messaggi.Mittente==current_user.id) & (Messaggi.Destinatario==user_id_receiver))\
         | ((Messaggi.Mittente == user_id_receiver) & (Messaggi.Destinatario == current_user.id)))\
        .order_by(Messaggi.id).all()

    nome_utente = (Utente.query.filter_by(id=user_id_receiver).first()).Nome

    form_message = MessageForm()

    if form_message.validate_on_submit():
        contenuto = form_message.contenuto.data
        messaggio = Messaggi( contenuto, current_user.id, user_id_receiver)
        insert(messaggio)
        return redirect('/profilo/messaggia/destinatario/' + str(user_id_receiver))

    return render_template('send-message.html', msgs=msgs, nome_utente=nome_utente, form=form_message)


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