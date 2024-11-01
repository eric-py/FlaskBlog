from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import login_user, current_user, logout_user, login_required
from .forms import LoginForm, RegistrationForm, RequestResetForm, ResetPasswordForm
from .models import User, db
from flask_mail import Message

main = Blueprint('main', __name__)

@main.route('/')
def home():
    return render_template('blog/index.html')

account = Blueprint('account', __name__)

@account.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            flash('You have successfully logged in.', 'success')
            return redirect(next_page or url_for('main.home'))
        else:
            flash('Login failed. Please check your username and password.', 'danger')
    return render_template('account/login.html', title='login', form=form)

@account.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.home'))

@account.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('account.login'))
    return render_template('account/register.html', title='Register', form=form)

def send_reset_email(user):
    from . import mail
    token = user.get_reset_token()
    msg = Message(subject='Password Reset Request',
                  sender='sample@demo.com',
                  recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
    {url_for('account.reset_token', token=token, _external=True)}

    If you did not make this request then simply ignore this email and no changes will be made.
    '''
    
    mail.send(msg)

@account.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            token = user.get_reset_token()
            send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('account.login'))
    return render_template('account/reset_request.html', title='Reset Password', form=form)

@account.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('account.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        user.reset_token = None
        user.reset_token_expiration = None
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('account.login'))
    return render_template('account/reset_token.html', title='Reset Password', form=form)