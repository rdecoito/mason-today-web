from flask import Flask
from flask import Response
from parscript import load_data
from getconnectedscript import load_getconn_data
import json

app = Flask(__name__)

@app.route("/25Live")
def display_data():
    resp = Response(json.dumps(load_data(), ensure_ascii=False).encode('utf-8'))
    resp.headers['Content-Type'] = 'application/json; charset=utf-8'
    return resp

@app.route("/getconn")
def display_GC_data():
	resp = Response(json.dumps(load_getconn_data(), ensure_ascii=False).encode('utf-8'))
	resp.headers['Content-Type'] = 'application/json; charset=utf-8'
	return resp
