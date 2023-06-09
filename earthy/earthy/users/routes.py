from flask import abort, render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from earthy import db, bcrypt
from earthy.models import User, Post
from earthy.users.forms import (RegistrationForm, LoginForm, RequestResetForm, ResetPasswordForm, UpdateAccountForm)
from earthy.users.utils import password_check, save_picture, send_reset_email

users = Blueprint('users', __name__)


@users.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        if (password_check(form.password.data)):
            hashed_password = bcrypt.generate_password_hash(
                form.password.data).decode('utf-8')
            user = User(username=form.username.data,
                        email=form.email.data, members=form.members.data, password=hashed_password)
            db.session.add(user)
            db.session.commit()
            flash('Your account has been created!', 'success')
            login_user(user, remember=True)
            return redirect(url_for('main.home'))
        else: flash('Please choose a strong password, it should have between 6 and 20 characters, with at least one numeral, uppercase, lower case, and one of these symbols: $@#. ', 'danger')
        
    return render_template('register.html', form=form, title='Register')


@users.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', form=form, title='Login')


@users.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.home'))


@users.route("/edit-account", methods=['GET', 'POST'])
@login_required
def edit_account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.members = form.members.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.members.data=current_user.members
    image_file = url_for(
        'static', filename='profile_pics/' + current_user.image_file)
    return render_template('edit_account.html',
                           image_file=image_file, form=form, title='Edit Account')


@users.route("/account")
@login_required
def account():
    username = current_user.username
    email = current_user.email
    score=current_user.score
    image_file = url_for(
        'static', filename='profile_pics/' + current_user.image_file)
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=current_user.username).first_or_404()
    posts = Post.query.filter_by(author=user)\
        .order_by(Post.date_created.desc())\
        .paginate(page=page, per_page=5)
    return render_template('account.html', posts=posts, user=current_user, image_file=image_file, score=score, title='Account')

@users.route("/account/delete", methods=['POST'])
@login_required
def delete_account():
    account = User.query.get_or_404(current_user.id)
    db.session.delete(account)
    db.session.commit()
    flash('Your account has been deleted!', 'success')
    return redirect(url_for('main.home'))

    
@users.route("/user/<string:username>")
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user)\
        .order_by(Post.date_created.desc())\
        .paginate(page=page, per_page=5)
    return render_template('user_posts.html', posts=posts, user=user)

@users.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('users.login'))
    return render_template('reset_request.html', title='Reset Password', form=form)


@users.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        if (password_check(form.password.data)):
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            user.password = hashed_password
            db.session.commit()
            flash('Your password has been updated! You are now able to log in', 'success')
            return redirect(url_for('users.login'))
        else: flash('Please choose a strong password, it should have between 6 and 20 characters, with at least one numeral, uppercase, lower case, and one of these symbols: $@#. ', 'danger')

    return render_template('reset_token.html', title='Reset Password', form=form)