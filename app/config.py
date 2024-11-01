from datetime import timedelta
from dotenv import load_dotenv
import os

load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")
    PERMANENT_SESSION_LIFETIME = timedelta(days=30)
    UPLOAD_FOLDER = os.path.abspath(os.path.dirname(__file__)) + '/uploads'
    TEMPLATES_FOLDER = os.path.abspath(os.path.dirname(__file__)) + '/templates'
    STATIC_FOLDER = os.path.abspath(os.path.dirname(__file__)) + '/static'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///%s' % os.path.join(os.path.abspath(os.path.dirname(__file__)), os.getenv("DB_NAME"))
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')