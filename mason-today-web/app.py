"""
"""
from flask import Flask
from flask import Response
from parscript import load_data
import json

app = Flask(__name__)

@app.route("/")
def display_data():
    resp = Response(json.dumps(load_data(), ensure_ascii=False).encode('utf-8'))
    resp.headers['Content-Type'] = 'application/json; charset=utf-8'
    return resp
