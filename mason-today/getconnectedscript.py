import requests
from bs4 import BeautifulSoup
from parscript import cleanup, doTheTime
import feedparser

# TODO: ADD "getconnected" ATTRIBUTE TO LOAD_DATA DICTLIST


# woah = cleanup(requests.get("https://getconnected.gmu.edu/events/events.rss").text)
# soup = BeautifulSoup(woah, "lxml")
# print soup.prettify
def load_getconn_data():
    feedtext = requests.get("https://getconnected.gmu.edu/events/events.rss").text
    feedtext = cleanup(feedtext)
    

    feed = feedparser.parse(feedtext) # this calls the RSS feed parser from !feedparser

    # print feed, "\n\n\n"
    # ctr = 0
    dictlist = []

    for entry in feed.entries:
        # print"==================================="
        uniqueid = entry.id[-7:]
        # print uniqueid

        title = entry.title
        # print title
        
        sumdetsoup = BeautifulSoup(entry.summary_detail["value"].encode("ascii", "replace"), "html.parser")
        
        location = [sumdetsoup.div.span.text]
        # print location

        description = sumdetsoup.find_all("div")[1].text
        # print description

        
        datetime = sumdetsoup.b.text
        # print datetime
        
        if (datetime.count("(") == 1):
            datesplit = datetime.split(", ")
            weekday = datesplit[0]
            month = datesplit[1].split(" ")
            monthday = month[1]
            month = month[0]
            year = datesplit[2][:5]
            parsedtimelist = doTheTime(datesplit[2][6:-1])
            timestart = parsedtimelist[0]
            timestop = parsedtimelist[1]
            # print {"id":uniqueid, "title":title, "dayofweek":weekday, "dayofmonth":monthday, "month":month, "year":year, "timestart":timestart, "timestop":timestop, "location":location, "description":description}
            dictlist.append({"id":uniqueid, "title":title, "dayofweek":weekday, "dayofmonth":monthday, "month":month, "year":year, "timestart":timestart, "timestop":timestop, "location":location, "description":description})
    return dictlist

    
    #print "\n\n", sumdetsoup.prettify()
    #print"==================================="

#dictlist.append({"id":uniqueid, "title":entry_title, "dayofweek":weekday, "dayofmonth":monthday, "month":month, "year":year, "timestart":timestart, "timestop":timestop, "location":location, "description":description})
#This was intended to figure out what objects are in each entry and what appears only sometimes
#The results are:
####Every event has:
#-------summary
#-------published_parsed
#-------links
#-------author
#-------summary
#-------guidislink
#-------title_detail
#-------link
#-------authors
#-------title
#-------author_detail
#-------id
#-------published
####Some events have:
#-------tags
