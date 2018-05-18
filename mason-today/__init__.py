# flask imports
from flask import Flask
from flask import Response
from flask import render_template

# app imports
from parscript import load_data
from getconnectedscript import load_getconn_data

# python imports
import json

# other imports
import redis
from redisactions import *

# setting up flask instance
app = Flask(__name__)

# setting up redis database
redisdb = redis.from_url("redis://localhost:6379/0", db=0)

@app.route("/")
def display_default():
    resp = render_template('welcomepage.html')
    return resp


@app.route("/api/25live")
def display_data():
    livedbfill(json.dumps(load_data(), ensure_ascii=False))
    resp = Response(redisdb.get("livedict")) # .encode('utf-8'))
    resp.headers['Content-Type'] = 'application/json; charset=utf-8'
    return resp


@app.route("/api/getconnected")
def display_GC_data():
    gcdbfill(json.dumps(load_getconn_data(), ensure_ascii=False))
    resp = Response(redisdb.get("gcdict")) # .encode('utf-8'))
    resp.headers['Content-Type'] = 'application/json; charset=utf-8'
    return resp
