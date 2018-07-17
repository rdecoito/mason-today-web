# python imports
import datetime

# other imports
import redis

# I'm thinking we store a couple things
# first: a key-value where the value is the dictlist
# second: a k-v for a list of errored events

# use rpush(key, value) to append a dblist (rpushx() to check if it exists)
# use del(key) to remove a k-v

# so everytime we run parscript or gcscript we want to run a dbfill()
# function. and every time we find an error we want to run a dberrorfill()
# function.

# setting up redis database
redisdb = redis.from_url("redis://localhost:6379/0", db=0)

# this will update the live dictlist and the cachedate
# returns true if the dictlist is not empty, false otherwise
def gcdbfill(dictlist):
    success = redisdb.set("gcdict", dictlist)

    log = str(datetime.datetime.now())
    redisdb.set("gccachedate", log)
    success = redisdb.get("gccachedate") == log and success

    return redisdb.get("gcdict") is not None and success


# saves new dictlist in place of previous 25Live dictlist
# returns true if the dictlist is not empty, false otherwise
def livedbfill(dictlist):
    success = redisdb.set("livedict", dictlist)

    log = str(datetime.datetime.now())
    redisdb.set("livecachedate", log)
    success = redisdb.get("livecachedate") == log and success

    return redisdb.get("livedict") is not None and success


# appends the log string to the head of our update long
# returns true if the head is the newest update
def appendtoupdatelog(logstring):
    redisdb.lpush("dbupdatelog", logstring)

    return redisdb.lrange("dbupdatelog", 0, 0) == logstring
