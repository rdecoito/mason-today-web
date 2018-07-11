# third party imports
import redis
from __init__ import redisdb

# I'm thinking we store a couple things
# first: a key-value where the value is the dictlist
# second: a k-v for a list of errored events

# use rpush(key, value) to append a dblist (rpushx() to check if it exists)
# use del(key) to remove a k-v

# so everytime we run parscript or gcscript we want to run a dbfill()
# function. and every time we find an error we want to run a dberrorfill()
# function.

# this will update the live dictlist and the cachedate
# returns true if the dictlist is not empty, false otherwise
def gcdbfill(dictlist):
    try:
        redisdb.set("gcdict", dictlist)
    except e:
        return False

    return redisdb.get("gcdict") is not None

# saves new dictlist in place of previous 25Live dictlist
# returns true if the dictlist is not empty, false otherwise
def livedbfill(dictlist):
    try:
        redisdb.set("livedict", dictlist)
    except e:
        return False
        
    return redisdb.get("livedict") is not None

# saves the last time the cache was updated
# return true if the cachedate is not empty, false otherwise
def setlastcachedate(cache, date):
    try:
        redisdb.set(cache, date)
    except e:
        return False
