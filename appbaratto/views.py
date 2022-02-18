
import uuid
from flask import Blueprint, render_template, request, url_for, redirect
from werkzeug.security import generate_password_hash
from flask_login import login_required, current_user

from .forms import EditForm, ItemsForm
from .models import Utente, Proposta
from .crud import *
from . import db

views = Blueprint('views', __name__)


@views.route('/')
def home():
    addclass = 'Homepage'
    return render_template('homepage.html', hideBreadcrumbs=addclass)


@views.route('/vedi-annunci/proponi/<int:id_annuncio>',  methods=["GET", "POST"])
@login_required
def proposal(id_annuncio):
    item = Oggetto.query.filter_by(id=id_annuncio).one_or_none()

    if item.id_utente != current_user.id :
        form_item = ItemsForm()

        if form_item.validate_on_submit():

            nome = form_item.nome.data
            desc = form_item.desc.data
            pics = request.files.getlist(form_item.image.name)

            img_urls = []

            if pics:
                for img in pics:
                    file_uuid = uuid.uuid4().hex

                    if (len(file_uuid) > 70):
                        file_uuid = file_uuid[0:70]

                    file_uuid = file_uuid + '.jpg'
                    img_urls.append(file_uuid)
                    img.save('appbaratto/static/uploads/images/' + file_uuid)

            img_1 = img_urls[0]
            new_proposal = Proposta(nome, desc, img_1, item.id)

    else:
        flash('Non puoi fare una proposta al tuo stesso annuncio', category='error')
        return redirect('/vedi-annunci/'+ str(id_annuncio))

    return render_template('proposal.html', item=item, form=form_item)


@views.route('/vedi-annunci')
def allItems():
    all_items = Oggetto.query.order_by(desc(Oggetto.Provincia)).all()

    for item in all_items: # Tronca nomi
        if(len(item.Nome) > 30):
            item.Nome = item.Nome[0:30] + " ..."
        if (len(item.Desc) > 80):
            item.Desc = item.Desc[0:80] + " ..."

    return render_template('all-items.html', items=all_items)


@views.route('/vedi-annunci/<int:id_annuncio>')
def item_selected( id_annuncio ):
    item = Oggetto.query.filter_by(id=id_annuncio).one_or_none()
    if( item == None):
        flash('Nessun annuncio trovato con questo id.', category='error')
    return render_template('selected-item.html', item=item)



@views.route('/vedi-annunci/elimina/<int:id_annuncio>')
def delete_item( id_annuncio ):

    item = Oggetto.query.filter_by(id=id_annuncio).one_or_none()

    if( item == None):
        flash('Nessun annuncio trovato con questo id.', category='error')
    else:
        if(current_user.id == item.id_utente):    # Se l'utente è lo stesso che ha inserito l'annuncio
            try:
                db.session.execute(delete(Oggetto).where(Oggetto.id == id_annuncio))  # Allora posso eliminare
                db.session.commit()
                flash('Annuncio eliminato con successo', category='success')
            except Exception as e:
                flash(f"Eccezione: {e}", category='error')
                db.session.rollback()
        else:
            flash('Non hai i permessi per eliminare a questo oggetto.', category='error')

    return redirect(url_for("views.yourItems"))


@views.route('/vedi-annunci/modifica/<int:id_annuncio>', methods=["GET", "POST"])
def edit_item( id_annuncio ):
    item = Oggetto.query.filter_by(id=id_annuncio).one_or_none()

    # Creo form
    form_items = ItemsForm()
    if item.id_utente == current_user.id:
        if form_items.validate_on_submit():

            nome = form_items.nome.data
            desc = form_items.desc.data
            provincia = form_items.provincia.data
            pics = request.files.getlist(form_items.image.name)

            img_urls = []

            if pics:
                for img in pics:
                    file_uuid = uuid.uuid4().hex

                    if (len(file_uuid) > 70):
                        file_uuid = file_uuid[0:70]

                    file_uuid = file_uuid + '.jpg'
                    img_urls.append(file_uuid)
                    img.save('appbaratto/static/uploads/images/' + file_uuid)

            img_1 = ""
            img_2 = ""
            img_3 = ""

            img_1 = img_urls[0]
            if (len(img_urls) == 2):
                img_2 = img_urls[1]
            if (len(img_urls) == 3):
                img_2 = img_urls[1]
                img_3 = img_urls[2]

            update_item(nome, desc, img_1, img_2, img_3, provincia, id_annuncio)

    return render_template('edit-item.html', item=item, form=form_items)


@views.route('/profilo')
@login_required
def profile():
    return render_template('profile.html')


@views.route('/profilo/i-tuoi-annunci')
@login_required
def yourItems():
    items = Oggetto.query.filter_by(id_utente=current_user.id).all()
    if not items:
        flash('Non hai annunci attivi da gestire.', category='error')
    for item in items: # Tronca nomi
        if(len(item.Nome) > 30):
            item.Nome = item.Nome[0:30] + " ..."

    return render_template('your-items.html', items=items)


@views.route('/profilo/aggiungi-oggetto', methods=["GET", "POST"])
@login_required
def addItem():
    form_items = ItemsForm()

    if form_items.validate_on_submit():

        nome = form_items.nome.data
        desc = form_items.desc.data
        provincia = form_items.provincia.data

        pics = request.files.getlist(form_items.image.name)
        img_urls = []

        if pics:
            for img in pics:
                file_uuid = uuid.uuid4().hex

                if (len(file_uuid) > 70):
                    file_uuid = file_uuid[0:70]

                file_uuid = file_uuid + '.jpg'
                img_urls.append(file_uuid)
                img.save('appbaratto/static/uploads/images/' + file_uuid)

        img_1 = ""
        img_2 = ""
        img_3 = ""

        img_1 = img_urls[0]
        if (len(img_urls) == 2):
            img_2 = img_urls[1]
        if (len(img_urls) == 3):
            img_2 = img_urls[1]
            img_3 = img_urls[2]

        new_item = Oggetto(nome, desc, img_1, img_2, img_3, provincia, current_user.id)

        # Insert in db
        insert_item(new_item)

    return render_template('add-item.html', form=form_items)


@views.route('/profilo/modifica-profilo', methods=["GET", "POST"])
@login_required
def editUser():

    form_modify = EditForm()

    if form_modify.validate_on_submit():
        password = form_modify.password.data
        password2 = form_modify.password2.data
        citta = form_modify.citta.data
        provincia = form_modify.provincia.data
        via = form_modify.via.data

        if password != password2:
            flash('Le due password inserite non combaciano.', category='error')
        elif len(password) < 6:
            flash('La password deve essere almeno 6 caratteri.', category='error')
        else:
            psw_hash = generate_password_hash(password)
            db.session.execute(update(Utente).where(Utente.id == current_user.id).
                               values(Password_hash=psw_hash, Citta=citta, Provincia=provincia, Via=via))
            db.session.commit()

    return render_template('edit-user.html', form=form_modify)


@views.errorhandler(404)
def page_not_found(error):
    return render_template('errore-404.html'), 404




