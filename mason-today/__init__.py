# flask imports
from flask import Flask
from flask import Response
from flask import render_template

# app imports
from parscript import load_data
from getconnectedscript import load_getconn_data

# python imports
import json

app = Flask(__name__)


@app.route("/")
def display_default():
    resp = render_template('welcomepage.html')
    return resp


@app.route("/api/25live")
def display_data():
    resp = Response(json.dumps(load_data(), ensure_ascii=False)
                    .encode('utf-8'))
    resp.headers['Content-Type'] = 'application/json; charset=utf-8'
    return resp


@app.route("/api/getconnected")
def display_GC_data():
    resp = Response(json.dumps(load_getconn_data(), ensure_ascii=False)
                    .encode('utf-8'))
    resp.headers['Content-Type'] = 'application/json; charset=utf-8'
    return resp
