import os
import secrets
from PIL import Image
from flask import current_app
from .config import Config

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