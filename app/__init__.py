from flask import Flask, session
from .config import Config
from .models import db, User
from .error_handlers import error_handlers
from flask_login import LoginManager
from .views import main
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

    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
    
    app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
    
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(app.config['TEMPLATES_FOLDER'], exist_ok=True)
    os.makedirs(app.config['STATIC_FOLDER'], exist_ok=True)

    mail.init_app(app)

    app.register_blueprint(main, url_prefix = '/')
    app.register_blueprint(error_handlers, url_prefix= '/errors/')

    @app.before_request
    def make_session_permanent():
        session.permanent = True

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    return app