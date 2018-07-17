# flask imports
from flask import Flask
from flask import Response
from flask import render_template

# app imports
from appmethods import updatebothdbs
from redisactions import redisdb

# python imports
import json

# other imports
import redis
import schedule
import time

# setting up flask instance
app = Flask(__name__)

# setting up cacheing
schedule.every().day.at("02:00").do(updatebothdbs)
# schedule.every(5).seconds.do(updatebothdbs)


@app.route("/")
def display_default():
    resp = render_template('welcomepage.html')
    return resp


@app.route("/api/25live")
def display_data():
    resp = Response(redisdb.get("livedict"))  # .encode('utf-8'))
    resp.headers['Content-Type'] = 'application/json; charset=utf-8'
    return resp


@app.route("/api/getconnected")
def display_GC_data():
    resp = Response(redisdb.get("gcdict"))  # .encode('utf-8'))
    resp.headers['Content-Type'] = 'application/json; charset=utf-8'
    return resp

# this needs to be uncommented in order for the scheduler to work
# but it's being weird cause it's hogging the thread
# while True:
    # schedule.run_pending()
    # time.sleep(5)
