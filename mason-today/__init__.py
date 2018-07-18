# flask imports
from flask import Flask
from flask import Response
from flask import render_template

# app imports
from appmethods import update_both_dbs, run_schedule_loop
from redisactions import redisdb

# python imports
import json
import thread

# other imports
import redis


# setting up flask instance
app = Flask(__name__)


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


@app.route("/api/lastupdate")
def get_last_update():
    resp = Response(redisdb.lindex("dbupdatelog", 0).replace("\n", "</br>"))
    return resp


try:
    thread.start_new_thread(run_schedule_loop, ())
    print "started thread!"
except:
    print "===================================================" \
        + "Unable to start scheduling thread" \
        + "==================================================="
