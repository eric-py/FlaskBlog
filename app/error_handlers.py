from flask import Blueprint, render_template

error_handlers = Blueprint('error_handlers', __name__)

@error_handlers.app_errorhandler(404)
def e_404(error):
    return render_template(''), 404 # template file name here