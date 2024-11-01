from flask import Flask, session
from .config import Config
from .models import db, User
from .error_handlers import error_handlers
from flask_login import LoginManager
from .views import main, account
import os
from flask_mail import Mail

login_manager = LoginManager()
mail = Mail()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)

    with app.app_context():
       db.create_all()
       User.create_admin()
    
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(app.config['TEMPLATES_FOLDER'], exist_ok=True)
    os.makedirs(app.config['STATIC_FOLDER'], exist_ok=True)

    mail.init_app(app)

    app.register_blueprint(main, url_prefix = '/')
    app.register_blueprint(account, url_prefix = '/account/')
    app.register_blueprint(error_handlers, url_prefix= '/errors/')

    @app.before_request
    def make_session_permanent():
        session.permanent = True

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    return app