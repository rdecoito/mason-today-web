from flask import Flask
from flask import Response
from parscript import load_data
from getconnectedscript import load_getconn_data
import json

app = Flask(__name__)

@app.route("/")
def display_default():
	resp = Response(("Welcome to the masontoday API! Go to https://git.gmu.edu/srct/mason-today-web <br/><br/>"
					+ "Feel free to go to /api/25live/ or /api/getconnected/ to find our api!").encode('utf-8'))
	return resp

@app.route("/api/25live")
def display_data():
    resp = Response(json.dumps(load_data(), ensure_ascii=False).encode('utf-8'))
    resp.headers['Content-Type'] = 'application/json; charset=utf-8'
    return resp


@app.route("/api/getconnected")
def display_GC_data():
	resp = Response(json.dumps(load_getconn_data(), ensure_ascii=False).encode('utf-8'))
	resp.headers['Content-Type'] = 'application/json; charset=utf-8'
	return resp
