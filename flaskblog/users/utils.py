#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Utils for the users routes
"""

import os
import secrets
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message
from flaskblog import mail


def save_picture(form_picture):
    """ Save a picture to the local filesystem """
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn)
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn


def send_reset_email(user):
    """ Function used to send an email for resetting a password """
    token = user.get_reset_token()
    msg = Message('Password Reset Request', sender='noreply@redds.be', recipients=[user.email],)
    msg.body = f'''To reset your password, visit the following link:
{url_for('users.reset_token', token=token, _external=True)}

If you did not make this request, you can ignore this message.    
    '''
    mail.send(msg)
