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