import uuid
from flask import Blueprint, render_template, request, redirect
from flask_login import login_required, current_user

from .models import Utente
from .forms import ProposalForm
from .crud import *
from . import db

proposal = Blueprint('proposal', __name__)


# Vedi le proposte ricevute per annuncio con (id_annuncio)
@proposal.route('/vedi-annunci/proposte/<int:id_annuncio>', methods=["GET", "POST"])
@login_required
def show_proposal(id_annuncio):
    item_1 = Oggetto.query.filter_by(id=id_annuncio).one_or_none()
    users = {}

    if item_1.id_utente == current_user.id:

        proposals = Proposta.query.filter_by(id_oggetto=id_annuncio).all()
        if not proposals:
            flash('Non ci sono proposte per questo oggetto.', category='error')
        else:
            for proposal in proposals:
                Nome =  (Utente.query.filter_by(id=proposal.id_utente_offerente).first()).Nome
                users[proposal.id_utente_offerente] = Nome

    else:
        flash('Non puoi vedere le proposte di un altro utente.', category='error')
        return redirect('/vedi-annunci/' + str(id_annuncio))

    return render_template('proposal-item.html', item_1=item_1, proposal=proposals, users=users)


# Un utente rifiuta una proposta(id_proposta) per l'oggetto (id_oggetto)
@proposal.route('/vedi-annunci/proposte/<int:id_oggetto>/rifiuta/<int:id_proposta>')
@login_required
def reject_proposal(id_proposta, id_oggetto):
    proposal = Proposta.query.filter_by(id=id_proposta).one_or_none()
    item = Oggetto.query.filter_by(id=id_oggetto).one_or_none()

    if proposal is None:
        flash('Nessun annuncio trovato con questo id.', category='error')

    else:
        if current_user.id == item.id_utente:  # Se l'utente è proprietario dell'annuncio
            try:
                db.session.execute(update(Proposta).where(Proposta.id == id_proposta).values(accettata=False))
                db.session.commit()
                flash('La proposta è stata rifiutata con successo.', category='success')

            except Exception as e:
                flash(f"Eccezione: {e}", category='error')
                db.session.rollback()

        else:
            flash('Non hai i permessi per accettare questa proposta.', category='error')

    return redirect('/vedi-annunci/proposte/' + str(id_oggetto))


# Un utente accetta una proposta(id_proposta) inviata da un utente all' oggetto(id_oggetto)
@proposal.route('/vedi-annunci/proposte/<int:id_oggetto>/accetta/<int:id_proposta>')
@login_required
def accept_proposal(id_proposta, id_oggetto):
    proposal = Proposta.query.filter_by(id=id_proposta).one_or_none()
    item = Oggetto.query.filter_by(id=id_oggetto).one_or_none()

    if proposal is None:
        flash('Nessuna proposta trovato con questo id.', category='error')

    else:
        if current_user.id == item.id_utente:  # Se l'utente è proprietario dell'annuncio
            try:
                db.session.execute(update(Proposta).where(Proposta.id == id_proposta).values(accettata=True))
                db.session.commit()
                flash('Dati aggiornati con successo', category='success')
            except Exception as e:
                flash(f"Eccezione: {e}", category='error')
                db.session.rollback()

        else:
            flash('Non hai i permessi per accettare questa proposta.', category='error')

    return redirect('/vedi-annunci/proposte/' + str(id_oggetto))


# Invia una proposta ad un oggetto (id_annuncio)
@proposal.route('/vedi-annunci/proponi/<int:id_annuncio>', methods=["GET", "POST"])
@login_required
def add_proposal(id_annuncio):
    item = Oggetto.query.filter_by(id=id_annuncio).one_or_none()
    form_item = ProposalForm()

    if item.id_utente != current_user.id:

        if form_item.validate_on_submit():

            nome = form_item.nome.data
            desc = form_item.desc.data
            pics = request.files.getlist(form_item.image.name)

            img_urls = []

            if pics:
                for img in pics:
                    file_uuid = uuid.uuid4().hex

                    if len(file_uuid) > 70:
                        file_uuid = file_uuid[0:70]

                    file_uuid = file_uuid + '.jpg'
                    img_urls.append(file_uuid)
                    img.save('appbaratto/static/uploads/images/' + file_uuid)

            img_1 = img_urls[0]
            new_proposal = Proposta(nome, desc, img_1, item.id, current_user.id, None)
            insert(new_proposal)

    else:
        flash('Non puoi fare una proposta al tuo stesso annuncio', category='error')
        return redirect('/vedi-annunci/' + str(id_annuncio))

    return render_template('proposal.html', item=item, form=form_item)


# Mostra tutte le tue proposte inviate
@proposal.route('/profilo/le-tue-proposte/')
@login_required
def your_proposal():
    all_proposal = Proposta.query.filter_by(id_utente_offerente=current_user.id).all()

    if not all_proposal:
        flash('Non hai inviato alcuna proposta', category='error')

    return render_template('your-proposal.html', items=all_proposal)


# Elimina una proposta inviata
@proposal.route('/profilo/le-tue-proposte/elimina/<int:id_proposta>')
@login_required
def delete_proposal(id_proposta):
    proposal = Proposta.query.filter_by(id=id_proposta).one_or_none()

    if proposal is None:
        flash('Nessun annuncio trovato con questo id.', category='error')

    else:
        if current_user.id == proposal.id_utente_offerente:  # Se l'utente è lo stesso che ha inserito l'annuncio
            try:
                db.session.execute(delete(Proposta).where(Proposta.id == id_proposta))  # Allora posso eliminare
                db.session.commit()
                flash('Annuncio eliminato con successo', category='success')
            except Exception as e:
                flash(f"Eccezione: {e}", category='error')
                db.session.rollback()
        else:
            flash('Non hai i permessi per eliminare questo oggetto.', category='error')


    return redirect('/profilo/le-tue-proposte')
