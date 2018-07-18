# app imports
from parscript import load_data
from getconnectedscript import load_gc_data
import redisactions as f

# python imports
import json
import datetime
import time

# other imports
import redis
import schedule


# attempts to update both dbs and logs the result
def update_both_dbs():
    livesuccess = f.live_db_fill(json.dumps(load_data(), ensure_ascii=False))
    gcsuccess = f.gc_db_fill(json.dumps(load_gc_data(), ensure_ascii=False))
    successLog = str(datetime.datetime.now()) \
        + "\n\nAttempted to update cache." \
        + "\n25Live: " + str(livesuccess) \
        + "\nGC: " + str(gcsuccess)

    f.append_to_update_log(successLog)
    return successLog


# setting up cacheing
# this must be done after the update_both_dbs def
schedule.every().day.at("02:00").do(update_both_dbs)


def run_schedule_loop():
    runScheduler = True
    while runScheduler:
        schedule.run_pending()
        time.sleep(1800)
