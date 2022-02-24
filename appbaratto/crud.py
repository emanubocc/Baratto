from . import db
from .models import Oggetto, Proposta
from sqlalchemy import update, select, delete, desc
from flask import flash


def update_item(nome, desc, img_1, img_2, img_3, provincia, id_annuncio, oggetti_preferiti):
    # update in DB
    try:
        db.session.execute(update(Oggetto).where(Oggetto.id == id_annuncio).
                           values(Nome=nome, Desc=desc, Img_1=img_1, Img_2=img_2, Img_3=img_3, Provincia=provincia, Oggetti_preferiti=oggetti_preferiti))
        db.session.commit()
        flash('Modifica avvenuta con successo.', category='success')
    except Exception as e:
        flash(f"Eccezione: {e}", category='error')
        db.session.rollback()


def insert_item(new_item):
    # Inserimento in DB
    try:
        db.session.add(new_item)
        db.session.commit()
        flash('Inserimento annuncio avvenuto con successo', category='success')
    except Exception as e:
        flash(f"Eccezione: {e}", category='error')
        db.session.rollback()


def insert_proposal(new_proposal):
    # Inserimento in DB
    print("hello!")
    try:
        print("hi!")
        db.session.add(new_proposal)
        db.session.commit()
        flash('Inserimento annuncio avvenuto con successo', category='success')
    except Exception as e:
        flash(f"Eccezione: {e}", category='error')
        db.session.rollback()
    print("bye!")