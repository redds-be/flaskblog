#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Routes for posts pages
"""

from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from flaskblog import db
from flaskblog.models import Post
from flaskblog.posts.forms import PostForm

posts = Blueprint('posts', __name__)


@posts.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    """ Route for creating a new post """
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data,  # pylint: disable=redefined-outer-name
                    content=form.content.data,
                    author=current_user)
        db.session.add(post)  # pylint: disable=no-member
        db.session.commit()  # pylint: disable=no-member
        flash('Your post has been created!', 'success')
        return redirect(url_for('main.home'))
    return render_template('create_post.html', title='New Post', form=form, legend='New Post')


@posts.route("/post/<int:post_id>")
def post(post_id):
    """ Route for the post view """
    post = Post.query.get_or_404(post_id)  # pylint: disable=redefined-outer-name
    return render_template('post.html', title=post.title, post=post)


@posts.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    """ Route for update post function """
    post = Post.query.get_or_404(post_id)  # pylint: disable=redefined-outer-name
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():  # pylint: disable=no-else-return
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()  # pylint: disable=no-member
        flash('Your post has been updated!', 'success')
        return redirect(url_for('posts.post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='Update Post', form=form, legend='Update Post')


@posts.route("/post/<int:post_id>/delete", methods=['POST', 'GET'])
@login_required
def delete_post(post_id):
    """ Route for the delete post function """
    post = Post.query.get_or_404(post_id)  # pylint: disable=redefined-outer-name
    if post.author != current_user:
        abort(403)
    db.session.delete(post)  # pylint: disable=no-member
    db.session.commit()  # pylint: disable=no-member
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('main.home'))
