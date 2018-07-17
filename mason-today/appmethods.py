# app imports
from parscript import load_data
from getconnectedscript import load_getconn_data
import redisactions as f

# python imports
import json
import datetime
import time

# other imports
import redis
import schedule


# attempts to update both dbs and logs the result
def updatebothdbs():
    livesuccess = f.livedbfill(json.dumps(load_data(), ensure_ascii=False))
    gcsuccess = f.gcdbfill(json.dumps(load_getconn_data(), ensure_ascii=False))
    successLog = str(datetime.datetime.now()) \
        + "\n\nAttempted to update cache." \
        + "\n25Live: " + str(livesuccess) \
        + "\nGC: " + str(gcsuccess)

    f.appendtoupdatelog(successLog)
    return successLog


def testprint():
    print "Schedule action completed!"


# setting up cacheing
schedule.every().day.at("02:00").do(updatebothdbs)


def runscheduleloop():
    runScheduler = True
    while runScheduler:
        schedule.run_pending()
        time.sleep(1800)
