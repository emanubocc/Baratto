
from flask import Blueprint

messages = Blueprint('messages', __name__)


'''
@messages.route('/messaggia/mittente/<int:user.id>/destinatario/<int:id_utente_offerente>/oggetto/<int:item.id>')
def all_items():'''