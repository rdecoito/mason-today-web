# print "and we begin"

# third party imports
from bs4 import BeautifulSoup
import requests


# this function cleans up some of the useless html leftovers to characters we can actually use
def cleanup(dirtystring):
    replacements = [
        ("&amp;", "&"),
        ("&nbsp;", " "),
        ("&ndash;", "-"),
        ("&lt;", "<"),
        ("&gt;", ">"),
        ("<br/>", "\n"),
        ("Publish event on the Calendar?: TRUE \n", ""),
        ("Performing any medical procedures?: FALSE \n", ""),
        ("Parking Needed?: FALSE \n", ""),
        ("\n\n\n", "\n"),
        ("\n\n", "\n"),
        ("&rsquo;", "'")
    ]

    for replacement in replacements:
        dirtystring = dirtystring.replace(replacement[0], replacement[1])

    return dirtystring[:-1]
    
# Simple event quality test
def qualityTest(desc):
    # none, bad, okay, good
    length = len(desc)

    if desc == "Not Provided":
        return "none"
    elif length < 10:
        return "bad"
    elif length < 40:
        return "okay"
    elif length < 80:
        return "good"
    elif length < 100:
        return "verygood"
    else: 
        return "excellent"

# convertTime accepts strings in the form of ""
def convertTime(stri):  # this function is used for splicing the event times.
    if (stri[-2:] == "pm" or stri[-2:] == "PM"):  # checks to see if the time presented is pm
        if not ((stri[0] == "1") and (stri[1] == "2")):  # if the time is pm, then the 12:00 hour is noon and shouldn't get 12 added to it
                try:  # this try block works with the exception handler to add 12 to any pm times
                    stri = stri.replace(stri[0:2], str(int(stri[0:2]) + 12), 1)
                    # print "I did the first one " + stri
                except Exception:
                    stri = stri.replace(stri[0], str(int(stri[0]) + 12), 1)
                    # print "I did the NOT first one " + stri
        if ":" in stri:  # this if/else reliably converts the time to minutes. accepts either "hour:minute" or simply "hour"
            try:
                return ((int(stri[0:2])) * 60) + int(stri[3:5])
            except Exception:
                return ((int(stri[0])) * 60) + int(stri[2:4])
        else:
            try:
                return (int(stri[0:2])) * 60
            except Exception:
                return (int(stri[0])) * 60
    elif (stri[-2:] == "am" or stri[-2:] == "AM"):  # checks if the time presented is am, and executes identical code from the pm block, just without adding 12
        if ":" in stri:
            try:
                return (int(stri[0:2]) * 60) + int(stri[3:5])
            except Exception:
                return (int(stri[0]) * 60) + int(stri[2:4])
        else:
            try:
                return int(stri[0:2]) * 60
            except Exception:
                return int(stri[0]) * 60
    else:
        raise Exception("Issue with time dilation. Input string: " + stri)

def filter_data_into_days(dictlist):
    new_dictlist = {}
    date_reference = ""
    for event in dictlist:
        if "error" in event: 
            continue
        
        event_date = event["dayofmonth"] + "/" +  str(month_to_number(event["month"])) + "/" + event["year"]
        if event_date in new_dictlist:
            new_dictlist[event_date].append(event)
        else: 
            new_dictlist[event_date] = [event]
    return new_dictlist
            

def month_to_number(month):
    month_dict = {
        "January": 1,
        "Febuary": 2,
        "March": 3,
        "April": 4,
        "May": 5,
        "June": 6,
        "July": 7,
        "August": 8,
        "September": 9,
        "October": 10,
        "November": 11,
        "December": 12
    }
    try: 
        out = month_dict[month]
        return out
    except: 
        raise Exception("Invalid month to convert to number")

def load_data():
    """
    Parses the XML from Mason and mines 2 BTC.
    Returns a dict of all the events.
    """
    dictlist = []
    DaysOfWeek = {
        "Sunday": 0,
        "Monday": 1,
        "Tuesday": 2,
        "Wednesday": 3,
        "Thursday": 4,
        "Friday": 5,
        "Saturday": 6,
    }

    notProvide = "Not Provided"

    soup = BeautifulSoup(cleanup(requests.get("http://25livepub.collegenet.com/calendars/events_all.xml").text), "lxml")
    # creates a list of all the entry tags from the xml
    entries = soup.findAll('entry')
    # indexs an entry in the list of entries

    for entry in entries:
        error = []
        try:
            uniqueid = entry.id.text
            uniqueid = uniqueid[-9:]
        except Exception:
            uniqueid = "Error with getting ID"

        # pulls up an entries in the list of entries, finds the title tag and .text deletes all xml tags and returns just the text as a string
        try:
            entry_title = entry.title.text

            entry_content = entry.content.text

            # makes it easy to find as things may be unevenly spaced
            entry_content = entry_content.replace("\n\n\n", "\n")
            entry_content = entry_content.replace("\n\n", "\n")

            # check clearcontent function
            entry_content = cleanup(entry_content)  # we might just get rid of this one

            # each piece of content may is seperated by a newline, entry_detailes creates a list
            entry_detailes = entry_content.split("\n")
        except Exception as e:
            error.append(str(e))
            dictlist.append({"id": uniqueid, "error": error})
            continue

        # in entry detailes list normally the conditions go as follow
        # [0] is the location
        # [1] is the date
        # [2] is the description

        # either conditions follows
        # [0] is date

        # [0] is location
        # [1] is date

        # [0] is date
        # [1] is description

        # sometimes the location or description is not given; however, the location always goes before date and
        # the description always follows the date. The date is always present. See examples above

        # (A) if the location is not given then the date must be index [0]
        # (B) if the length of the list = 1 and date is index [0] --> location not given & description is not given
        # (C) if the length of the list = 2 and date is index [0] --> location not given but description is given at [1]

        # (D) if the location is given then the date must be index [1]
        # (E) if the length of the list = 2 and date is index [1] --> location is given at [0] but description is not given
        # (F) if the length of the list = 3 and date is index [1] --> location is given at [0] and description is given at [2]

        # the two if statements finds the date string. The date string always starts with
        # Monday Tuesday Wednesday Thursday Friday Saturday Sunday or Ongoing and the date
        # is always on either [0] or [1]

        # see (A) above
        try:
            if entry_detailes[0].split(",")[0] in DaysOfWeek:
                # See (B)
                if len(entry_detailes) == 1:
                    location = notProvide
                    date = entry_detailes[0]
                    description = notProvide
                # see (C)
                elif len(entry_detailes) == 2:
                    location = notProvide
                    date = entry_detailes[0]
                    description = entry_detailes[1]
                # This extra case was made because one entry had the description split into two by a
                # newline so it registered as two descriptions making the length = 3
                elif len(entry_detailes) == 3:
                    location = notProvide
                    date = entry_detailes[0]
                    description = entry_detailes[1] + " " + entry_detailes[2]
                # this will print if the code has failed to account for something in detailes, but it works as of December 26th 2017
                else:
                    raise Exception("failed to account for detail in entry_detailes when date element is index 0 on entry_detailes list")

            # see (D) above
            elif entry_detailes[1].split(",")[0] in DaysOfWeek:
                # See (E)
                if len(entry_detailes) == 2:
                    location = entry_detailes[0]
                    date = entry_detailes[1]
                    description = notProvide
                # See (F)
                elif len(entry_detailes) == 3:
                    location = entry_detailes[0]
                    date = entry_detailes[1]
                    description = entry_detailes[2]
                # This extra case was made because one entry had the description split into two by a
                # newline so it registered as two descriptions making the length = 3
                elif len(entry_detailes) == 4:
                    location = entry_detailes[0]
                    date = entry_detailes[1]
                    description = entry_detailes[2] + " " + entry_detailes[3]
                # this will print if the code has failed to account for something in detailes
                else:
                    raise Exception("failed to account for detail in entry_detailes when date element is index 1 on entry_detailes list")
            # this will print if the above if statements failed to find the date block
            else:
                raise Exception("failed to find and account for date element in entry_detailes list")
        except Exception as e:
            error.append(str(e))

        try:
            if location != notProvide:
                location = location[:-1]
                location += ", "
            if "Fairfax Campus" in location:
                location = location.split(", Fairfax Campus, ")
                campus = "Fairfax"
                del location[-1]
            elif "Arlington Campus" in location:
                location = location.split(", Arlington Campus, ")
                campus = "Arlington"
                del location[-1]
            else:
                location = [location]
        except Exception:
            error.append("Location Error: " + str(e))

        try:
            date = date.split(",")
            day = date[0]
            time = date[3][1:]
            date = date[1][1:] + "," + date[2]
            date = date.split(" ")
            month = date[0]
            monthday = date[1][:(len(date[1]) - 1)]
            year = date[2]
        except Exception as e:
            error.append("Date Error: " + str(e))

        try:
            time = time.replace(" ", "")
            time = time.split("-")

            timestop = convertTime(time[1])

            if timestop is None:
                raise Exception(str(time))
            if not (time[0][-2:] == "am") and not (time[0][-2:] == "pm"):
                if (time[1][-2:] == "am"):
                    timestart = convertTime(time[0] + "am")
                else:
                    timestart = convertTime(time[0] + "pm")
            else:
                timestart = convertTime(time[0])
        except Exception as e:
            error.append("Time Dilation Error: " + str(e))

        # print "-----------------------------------------------------------------------------"
        # print location
        # print day
        # print month
        # print monthday
        # print year
        # print timestart
        # print timestop
        # print description
        # print "----------------------------------------------------------------------------"

        if (error == []):
            quality = qualityTest(description)
            dictlist.append({"id": uniqueid, "quality": quality, "title": entry_title, "dayofweek": day, "dayofmonth": monthday, "month": month,
             "year": year, "timestart": timestart, "timestop": timestop, "location": location, "description": description})
        else:
            dictlist.append({"id": uniqueid, "error": error})
    
    return filter_data_into_days(dictlist)

# everything in the house is fuzzy, stupid dogs were acting like pollinators, if that's how you even spell it
load_data()