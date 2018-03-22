"""
mason-today-web/parscript.py

Run the Flask application to serve json.
"""
# Future imports
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

# Python std lib imports
import json

# App imports
from .parscript import load_data

# Third party imports
from flask import Flask, Response

app = Flask(__name__)

@app.route("/")
def display_data():
    resp = Response(json.dumps(load_data(), ensure_ascii=False))
    resp.headers['Content-Type'] = 'application/json; charset=utf-8'
    return resp
