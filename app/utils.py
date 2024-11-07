import os
import secrets
from PIL import Image
from flask import current_app
from .config import Config
from functools import wraps
from flask_login import current_user
from random import sample
from .models import Category, Post


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, Config.UPLOAD_FOLDER, picture_fn)
    os.makedirs(os.path.dirname(picture_path), exist_ok=True)

    output_size = (800, 600)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash('You do not have access to this page.', 'danger')
            return redirect(url_for('main.home'))
        return f(*args, **kwargs)
    return decorated_function

def get_sidebar_data():
    return {
        'categories': Category.query.all(),
        'popular': Post.query.filter_by(status='p').order_by(Post.views.desc()).first(),
        'random_posts': sample(Post.query.filter_by(status='p').all(), 5)
    }