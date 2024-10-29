from flask import Flask, session
from .config import Config
from .views import main
from .models import db
from .error_handlers import error_handlers
import os

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(app.config['TEMPLATES_FOLDER'], exist_ok=True)
    os.makedirs(app.config['STATIC_FOLDER'], exist_ok=True)

    app.register_blueprint(main, url_prefix = '/')
    app.register_blueprint(error_handlers, url_prefix= '/errors/')

    @app.before_request
    def make_session_permanent():
        session.permanent = True

    with app.app_context():
        db.create_all()
    
    return app