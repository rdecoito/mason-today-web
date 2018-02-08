#!/bin/sh
export FLASK_APP=mason-today/app.py
export FLASK_DEBUG=1
flask run --host=0.0.0.0 --port=8000
