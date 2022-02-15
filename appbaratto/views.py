from flask import Blueprint, render_template, flash, jsonify, request
from werkzeug.security import generate_password_hash
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename

from sqlalchemy import update, select, delete, desc
from .forms import EditForm, ItemsForm
from .models import Utente, Oggetto
from . import db

views = Blueprint('views', __name__)


@views.route('/')
def home():
    addclass = 'Homepage'
    return render_template('homepage.html', hideBreadcrumbs=addclass)

@views.route('/vedi-annunci')
def allItems():

    all_items = Oggetto.query.order_by(desc(Oggetto.Provincia)).all()
    return render_template('all-items.html', items=all_items)

@views.route('/vedi-annunci/<int:id_annuncio>')
def item_selected( id_annuncio ):
    item = Oggetto.query.filter_by(id=id_annuncio).one_or_none()
    if( item == None):
        flash('Nessun annuncio trovato con questo id.', category='error')
    return render_template('selected-item.html', item=item)


@views.route('/profilo')
@login_required
def profile():
    return render_template('profile.html')


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
                file_name = secure_filename(img.filename)
                img_urls.append(file_name)
                img.save('appbaratto/static/uploads/images/' + file_name)

        img_1 = img_urls[0]
        img_2 = ""
        img_3 = ""

        if (len(img_urls) == 2):
            img_2 = img_urls[1]
        if (len(img_urls) == 3):
            img_3 = img_urls[2]

        new_item = Oggetto(nome, desc, img_1, img_2, img_3, provincia, current_user.id)

        # Inserimento in DB
        try:
            db.session.add(new_item)
            db.session.commit()
            flash('Inserimento annuncio avvenuto con successo', category='success')
        except Exception as IntegrityError:
            flash(f"Le immagini presentano nomi già utilizzati.", category='error')
            db.session.rollback()
        except Exception as e:
            flash(f"Eccezione: {e}", category='error')
            db.session.rollback()




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


