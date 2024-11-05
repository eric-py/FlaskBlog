from flask import Blueprint, render_template, flash, redirect, url_for, request, abort
from flask_login import login_user, current_user, logout_user, login_required
from .forms import LoginForm, RegistrationForm, RequestResetForm, ResetPasswordForm, PostForm, CategoryForm
from .models import User, db, Post, Category
from flask_mail import Message
from .utils import save_picture
from flask import send_from_directory
from flask import current_app
import os

main = Blueprint('main', __name__)

@main.route('/')
def home():
    return render_template('blog/index.html')

@main.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)

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

profile = Blueprint('profile', __name__)

@profile.route('')
@login_required
def profile_index():
    posts = Post.query.filter_by(author=current_user).all()
    return render_template('profile/index.html', posts=posts)

@profile.route('/new', methods=['GET', 'POST'])
@login_required
def new_article():
    form = PostForm()
    
    if form.validate_on_submit():
        post = Post(title=form.title.data,
                    content=form.content.data,
                    status=form.status.data,
                    author=current_user)
        
        selected_categories = Category.query.filter(Category.id.in_(form.categories.data)).all()
        post.categories = selected_categories
        
        if form.image.data:
            image_file = save_picture(form.image.data)
            post.image_filename = image_file
        
        db.session.add(post)
        db.session.commit()
        flash('Your article has been created!', 'success')
        return redirect(url_for('profile.profile_index'))
    
    return render_template('profile/new_article.html', title='New Article', form=form)

@profile.route('/edit/<int:post_id>', methods=['GET', 'POST'])
@login_required
def edit_article(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        post.status = form.status.data
        
        selected_categories = Category.query.filter(Category.id.in_(form.categories.data)).all()
        post.categories = selected_categories
        
        if form.image.data:
            image_file = save_picture(form.image.data)
            if post.image_filename:
                old_image_path = os.path.join(current_app.root_path, current_app.config['UPLOAD_FOLDER'], post.image_filename)
                if os.path.exists(old_image_path):
                    os.remove(old_image_path)
            post.image_filename = image_file
        
        db.session.commit()
        flash('Your article has been updated!', 'success')
        return redirect(url_for('profile.profile_index'))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
        form.status.data = post.status
        form.categories.data = [category.id for category in post.categories]
    
    return render_template('profile/new_article.html', title='Edit Article', form=form, post=post)

@profile.route("/delete_article/<int:post_id>")
@login_required
def delete_article(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        flash('You do not have permission to delete this post.', 'danger')
        return redirect(url_for('main.home'))
    
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('profile.profile_index'))

@profile.route("/new_category", methods=['GET', 'POST'])
@login_required
def new_category():
    if not current_user.is_admin:
        abort(403)
    
    form = CategoryForm()
    if form.validate_on_submit():
        category = Category(name=form.name.data)
        db.session.add(category)
        db.session.commit()
        flash('New category has been created!', 'success')
        return redirect(url_for('profile.new_category'))
    
    categories = Category.query.order_by(Category.id.desc()).all()
    return render_template('profile/new_category.html', title='New Category', form=form, categories=categories)

@profile.route("/edit_category/<int:category_id>", methods=['GET', 'POST'])
@login_required
def edit_category(category_id):
    if not current_user.is_admin:
        abort(403)

    category = Category.query.get_or_404(category_id)
    form = CategoryForm()
    if form.validate_on_submit():
        category.name = form.name.data
        db.session.commit()
        flash('The category has been updated!', 'success')
        return redirect(url_for('profile.new_category'))
    elif request.method == 'GET':
        form.name.data = category.name
    return render_template('profile/edit_category.html', title='Edit Category', form=form, category=category)

@profile.route("/delete_category/<int:category_id>", methods=['GET'])
@login_required
def delete_category(category_id):
    if not current_user.is_admin:
        abort(403)

    category = Category.query.get_or_404(category_id)
    db.session.delete(category)
    db.session.commit()
    flash('The category has been deleted!', 'success')
    return redirect(url_for('profile.new_category'))