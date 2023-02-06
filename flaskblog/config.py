#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Configuration file
"""

import os


class Config:  # pylint: disable=too-few-public-methods
    """ Configuration class that gets the environments variables created by a script """
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    MAIL_SERVER = 'mailserv'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
