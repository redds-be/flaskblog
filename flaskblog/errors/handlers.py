#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Error Pages handler
"""

from flask import Blueprint, render_template

errors = Blueprint('errors', __name__)


@errors.app_errorhandler(404)
def error_404(error):  # pylint: disable=unused-argument
    """ Route for 404 error """
    return render_template('errors/404.html'), 404


@errors.app_errorhandler(403)
def error_403(error):  # pylint: disable=unused-argument
    """ Route for 403 error """
    return render_template('errors/403.html'), 403


@errors.app_errorhandler(500)
def error_500(error):  # pylint: disable=unused-argument
    """ Route for 500 error"""
    return render_template('errors/500.html'), 500
