from flask import Flask , render_template
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from os import path


DB_NAME = "dbBaratto.sqlite"
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    app.config["SECRET_KEY"] = "O#r@4lU0%Dv9AsK*aM*sVlro9hWrWc"
    app.config["SQLALCHEMY_DATABASE_URI"] = f'sqlite:///{DB_NAME}'


    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config['SQLALCHEMY_ECHO'] = True

    db.init_app(app)

    from .views import views
    from .auth import auth
    from .proposal import proposal
    from .messages import messages

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(proposal, url_prefix='/')
    app.register_blueprint(messages, url_prefix='/')

    from .models import Utente
    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return Utente.query.get(int(id))

    return app

def create_database(app):
    if not path.exists('appbaratto/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')