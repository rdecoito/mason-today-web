# app imports
from parscript import load_data
from getconnectedscript import load_getconn_data
import redisactions as f

# python imports
import json


# attempts to update both dbs and returns true if successful
def updatebothdbs():
    livesuccess = f.livedbfill(json.dumps(load_data(), ensure_ascii=False))
    gcsuccess = f.gcdbfill(json.dumps(load_getconn_data(), ensure_ascii=False))
    print "DBs updated.\n25Live: " + str(livesuccess) \
          + "\nGC: " + str(gcsuccess)
    return livesuccess and gcsuccess


def testprint():
    print "Schedule action completed!"
