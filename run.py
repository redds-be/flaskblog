#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Basic flask blog (tutorial)
"""

from flaskblog import create_app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
