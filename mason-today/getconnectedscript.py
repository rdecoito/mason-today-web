import requests
from bs4 import BeautifulSoup
from parscript import cleanup, doTheTime
import feedparser

#TODO: ADD "getconnected" ATTRIBUTE TO LOAD_DATA DICTLIST


#woah = cleanup(requests.get("https://getconnected.gmu.edu/events/events.rss").text)
#soup = BeautifulSoup(woah, "lxml")
#print soup.prettify
feedtext = requests.get("https://getconnected.gmu.edu/events/events.rss").text
feedtext = cleanup(feedtext)
feedtext = feedtext.replace("&rsquo;", "'")

feed = feedparser.parse(feedtext)#this calls the RSS feed parser from !feedparser

#print feed, "\n\n\n"
#ctr = 0
dictlist = []

for entry in feed.entries:
	# templist = {}
	#print entry.summary_detail.value
	# templist["summary_detail"] = entry.summary_detail

	'''print "----------------------------------"
	print "1) ", entry.published_parsed, "\n"
	templist["published_parsed"] = entry.published_parsed

	print entry.links, "\n"
	templist["links"] = entry.links
	
	print "3) ", entry.author, "\n"
	templist["author"] = entry.author
	
	print entry.summary, "\n"
	templist["summary"] = entry.summary
	
	print "5) ", entry.guidislink, "\n"
	templist["guidislink"] = entry.guidislink
	
	print entry.title_detail, "\n"
	templist["title_detail"] = entry.title_detail
	
	print "6) ", entry.link, "\n"
	templist["link"] = entry.link
	
	print entry.authors, "\n"
	templist["authors"] = entry.authors
	
	print "7) ", entry.title, "\n"
	templist["title"] = entry.title
	
	print entry.author_detail, "\n"
	templist["author_detail"] = entry.author_detail
	
	print "9) ", entry.id, "\n"
	templist["id"] = entry.id
	
	print entry.published, "\n"
	templist["published"] = entry.published
	print"-----------------------------------"'''
	


	#print"==================================="
	uniqueid = entry.id[-7:]
	#print uniqueid

	title = entry.title
	#print title
	
	sumdetsoup = BeautifulSoup(entry.summary_detail["value"].encode("ascii", "replace"), "html.parser")
	
	location = [sumdetsoup.div.span.text]
	#print location

	description = sumdetsoup.find_all("div")[1].p.text
	#print description

	
	datetime = sumdetsoup.b.text
	#print datetime
	
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
		dictlist.append({"id":uniqueid, "title":title, "dayofweek":weekday, "dayofmonth":monthday, "month":month, "year":year, "timestart":timestart, "timestop":timestop, "location":location, "description":description})		

print dictlist

	
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


'''for key in feed.entries[0].keys():
	everyone.append(key)
some = []

for entry in feed.entries:
	#print "----------------------------------"
	for key in entry.keys():
		if not key in everyone:
			some.append(key)
		for key in everyone:
			if not (key in entry.keys()):
				everyone.remove(key)
				some.append(key)
	#print"-----------------------------------"
	#ctr += 1
print "Everyone: \n", everyone
print "Some: \n", some'''
