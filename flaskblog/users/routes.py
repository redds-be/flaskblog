#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Routes for users pages
"""

from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from flaskblog import db, bcrypt
from flaskblog.models import User, Post
from flaskblog.users.forms import (RegistrationForm, LoginForm, UpdateAccountForm,
                                   RequestResetForm, ResetPasswordForm)
from flaskblog.users.utils import save_picture, send_reset_email

users = Blueprint('users', __name__)


@users.route("/register", methods=['GET', 'POST'])
def register():
    """ Registration Page """
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)  # pylint: disable=no-member
        db.session.commit()  # pylint: disable=no-member
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('users.login'))
    return render_template('register.html', title='Register', form=form)


@users.route("/login", methods=['GET', 'POST'])
def login():
    """ Login page """
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if not user or not bcrypt.check_password_hash(user.password, form.password.data):
            flash('Invalid username or password!', 'danger')
        else:
            login_user(user, remember=form.remember.data)
            flash(f'Now logged in as : {user.username}', 'success')
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
    return render_template('login.html', title='Login', form=form)


@users.route("/logout")
def logout():
    """ Logout Function """
    logout_user()
    return redirect(url_for('main.home'))


@users.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    """ Account Page """
    form = UpdateAccountForm()
    if form.validate_on_submit():  # pylint: disable=no-else-return
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()  # pylint: disable=no-member
        flash('Your account has been updated!', 'success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename=f'profile_pics/{current_user.image_file}')
    print(image_file)
    return render_template('account.html', title='Account', image_file=image_file, form=form)


@users.route("/account/reset_password", methods=['GET', 'POST'])
@login_required
def reset_account_password():
    """ Route for resetting the account's password """
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user = current_user
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()  # pylint: disable=no-member
        flash('Your password has been updated!', 'success')
        return redirect(url_for('users.account'))
    return render_template('reset_token.html', title='Reset Password', form=form)


@users.route("/account/delete", methods=['POST', 'GET'])
@login_required
def delete_account():
    """ Route for deleting the account """
    db.session.delete(current_user)  # pylint: disable=no-member
    db.session.commit()  # pylint: disable=no-member
    flash('Your account has been deleted!', 'success')
    return redirect(url_for('main.home'))


@users.route("/user/<string:username>")
def about_user(username):
    """ Route for the 'about user' page """
    user = User.query.filter_by(username=username).first_or_404(username)
    image_file = url_for('static', filename=f'profile_pics/{user.image_file}')
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter_by(author=user).order_by(Post.date_posted.desc()).paginate(page=page,
                                                                                         per_page=5)  # pylint: disable=line-too-long
    return render_template('about_user.html', title=user.username, user=user,
                           image_file=image_file, posts=posts)


@users.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    """ Route for the 'reset_password' page """
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
    """ Route for the 'reset_password' page using the token to validate the request """
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('Your token is invalid or expired', 'warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()  # pylint: disable=no-member
        flash('Your password has been updated! You are now able to log in.', 'success')
        return redirect(url_for('users.login'))
    return render_template('reset_token.html', title='Reset Password', form=form)
