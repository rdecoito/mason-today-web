import requests
from bs4 import BeautifulSoup
from parscript import cleanup, convertTime
import feedparser

# TODO: ADD "getconnected" ATTRIBUTE TO LOAD_DATA DICTLIST

def splitAndConvertTime(strin):
    strin = strin.replace(" ", "")
    strin = strin.split("-")
    returnlist = ["",""]
    returnlist[1] = convertTime(strin[1])
    if not (strin[0][-2:] == "am" or strin[0][-2:] == "AM") and not (strin[0][-2:] == "pm" or strin[0][-2:] == "PM"):
        if (strin[1][-2:] == "am"):
            returnlist[0] = convertTime(strin[0] + "am")
        else:
            returnlist[0] = convertTime(strin[0] + "pm")
    else:
        returnlist[0] = convertTime(strin[0])
    return returnlist

def load_getconn_data():
    feedtext = requests.get("https://getconnected.gmu.edu/events/events.rss").text
    feedtext = cleanup(feedtext)

    # this calls the RSS feed parser from !feedparser
    feed = feedparser.parse(feedtext)

    dictlist = []

    for entry in feed.entries:
        uniqueid = entry.id[-7:]
        # print uniqueid

        title = entry.title
        # print title
        
        sumdetsoup = BeautifulSoup(entry.summary_detail["value"].encode("utf-8"), "html.parser")
        
        location = [sumdetsoup.div.span.text]
        # print location

        description = sumdetsoup.find_all("div")[1].text
        # print description

        
        datetime = sumdetsoup.b.text
        # print datetime

        # this handles events which start and end on the same day
        if (datetime.count("(") == 1):
            datesplit = datetime.split(", ")
            weekday = datesplit[0]
            temp = datesplit[1].split(" ")
            monthday = temp[1]
            month = temp[0]
            year = datesplit[2][:5]

            # uses helper function to get the start and end time
            parsedtimelist = splitAndConvertTime(datesplit[2][6:-1])
            timestart = parsedtimelist[0]
            timestop = parsedtimelist[1]

            dictlist.append({"id":uniqueid, "title":title, "dayofweek":weekday, "dayofmonth":monthday, "month":month, 
                            "year":year, "timestart":timestart, "timestop":timestop, "location":location, "description":description})
        
        # this handles events which start on one day and end on another
        else:
            datesplit = datetime.split(" - ")

            # getting the information for the start day/time
            tempsplits = datesplit[0].split(", ")
            weekday = tempsplits[0]
            month = tempsplits[1].split(" ")[0]
            monthday = tempsplits[1].split(" ")[1]
            year = tempsplits[2].split(" ")[0]
            timestart = datesplit[0].split("(")[1][:-1]
            timestart = convertTime(timestart)

            # getting the information for the end day/time
            tempsplits = datesplit[1].split(", ")
            endweekday = tempsplits[0]
            endmonth = tempsplits[1].split(" ")[0]
            endmonthday = tempsplits[1].split(" ")[1]
            endyear = tempsplits[2].split(" ")[0]
            timestop = datesplit[1].split("(")[1][:-1]
            timestop = convertTime(timestop)

            dictlist.append({"id":uniqueid, "title":title, "dayofweek":weekday, "dayofmonth":monthday, "month":month, 
                            "year":year, "timestart":timestart, "timestop":timestop, "location":location, "description":description,
                            "enddayofweek":endweekday, "enddayofmonth":endmonthday, "endmonth":endmonth, "endyear":endyear})
    return dictlist
    
# dictlist.append({"id":uniqueid, "title":entry_title, "dayofweek":weekday, "dayofmonth":monthday, "month":month, "year":year, "timestart":timestart, "timestop":timestop, "location":location, "description":description})
# This was intended to figure out what objects are in each entry and what appears only sometimes
# The results are:
# Every event has:
# -------summary
# -------published_parsed
# -------links
# -------author
# -------summary
# -------guidislink
# -------title_detail
# -------link
# -------authors
# -------title
# -------author_detail
# -------id
# -------published
# Some events have:
# -------tags
