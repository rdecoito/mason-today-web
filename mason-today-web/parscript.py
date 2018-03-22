"""
mason-today-web/parscript.py

Scrape data from GMU 25Live and parse it into a dictionary to serve.
"""
# Future imports
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
# Third party imports
from bs4 import BeautifulSoup
import requests

def clean_response(response):
    """
    Clean up some of the useless html leftovers to characters we can actually use
    """
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
        ("\n\n", "\n")
    ]

    for replacement in replacements:
        response.replace(replacement[0], replacement[1])
    return response[0:len(response) - 1]

def convert_time(time_string):
    """
    Splice the event times.
    """
    # Checks to see if the time presented is pm
    if (time_string[-2:] == "pm"):
        # If the time is pm, then the 12:00 hour is noon and shouldn't get 12 added to it
        if not ((time_string[0] == "1") and (time_string[1] == "2")):
            # This try block works with the exception handler to add 12 to any pm times
            try:
                time_string = time_string.replace(time_string[0:2], str(int(time_string[0:2]) + 12), 1)
            except:
                time_string = time_string.replace(time_string[0], str(int(time_string[0]) + 12), 1)
        # This if/else reliably converts the time to minutes. accepts either "hour:minute" or simply "hour"
        if ":" in time_string:
            try:
                return ((int(time_string[0:2])) * 60) + int(time_string[3:5])
            except:
                return ((int(time_string[0])) * 60) + int(time_string[2:4])
        else:
            try:
                return (int(time_string[0:2])) * 60
            except:
                return (int(time_string[0])) * 60
    # Checks if the time presented is am, and executes identical code from the pm block, just without adding 12
    elif (time_string[-2:] == "am"):
        if ":" in time_string:
            try:
                return (int(time_string[0:2]) * 60) + int(time_string[3:5])
            except:
                return (int(time_string[0]) * 60) + int(time_string[2:4])
        else:
            try:
                return int(time_string[0:2]) * 60
            except:
                return int(time_string[0]) * 60
    else:
        raise ValueError("This is weird and please don't happen")

def load_data():
    """
    Parses the XML from 25Live. Returns a dict of all the events.
    """
    not_provided = "Not Provided"
    dictlist = []
    days_of_week = {
        "Sunday": 0,
        "Monday": 1,
        "Tuesday": 2,
        "Wednesday": 3,
        "Thursday": 4,
        "Friday": 5,
        "Saturday": 6,
    }

    soup = BeautifulSoup(requests.get("http://25livepub.collegenet.com/calendars/events_all.xml").text, "lxml")
    # Creates a list of all the entry tags from the xml
    entries = soup.findAll('entry')

    for entry in entries:
        error = []

        entry_content = entry.content.text
        entry_id = entry.id.text

        # each piece of content may is seperated by a newline
        entry_details = entry_content.split("\n")

        """
        init_event

        In entry details list normally the conditions go as follow

        [0] is the location
        [1] is the date
        [2] is the description

        either conditions follows
        [0] is date 

        [0] is location
        [1] is date 

        [0] is date
        [1] is description

        sometimes the location or description is not given; however, the
        location always goes before date and the description always follows
        the date. The date is always present. See examples above

        (A) if the location is not given then the date must be index [0]
        (B) if the length of the list = 1 and date is index [0] --> location not given & description is not given              
        (C) if the length of the list = 2 and date is index [0] --> location not given but description is given at [1]         		
        (D) if the location is given then the date must be index [1]       
        (E) if the length of the list = 2 and date is index [1] --> location is given at [0] but description is not given      
        (F) if the length of the list = 3 and date is index [1] --> location is given at [0] and description is given at [2]   

        the two if statements finds the date time_string. The date time_string always starts with 
        Monday Tuesday Wednesday Thursday Friday Saturday Sunday or Ongoing and the date 
        is always on either [0] or [1]
        """
        # see (A) above
        try:
            print(entry_details[0].split(",")[0])
            if entry_details[0].split(",")[0] in days_of_week:
                # See (B)
                if len(entry_details) == 1:
                    location = not_provided
                    date = entry_details[0]
                    description = not_provided
                # See (C)
                elif len(entry_details) == 2:
                    location = not_provided
                    date = entry_details[0]
                    description = entry_details[1]
                # This extra case was made because one entry had the description split into two by a
                # newline so it registered as two descriptions making the length = 3
                elif len(entry_details) == 3:
                    location = not_provided
                    date = entry_details[0]
                    description = entry_details[1] + " " + entry_details[2]
                # this will print if the code has failed to account for something in detailes, but it works as of December 26th 2017
                else:
                    raise ValueError("failed to account for detail in entry_details when date element is index 0 on entry_details list")
            # see (D) above
            elif entry_details[1].split(",")[0] in days_of_week:
                # See (E)
                if len(entry_details) == 2:
                    location = entry_details[0]
                    date = entry_details[1]
                    description = not_provided
                # See (F)
                elif len(entry_details) == 3:
                    location = entry_details[0]
                    date = entry_details[1]
                    description = entry_details[2]
                # This extra case was made because one entry had the description split into two by a
                # newline so it registered as two descriptions making the length = 3
                elif len(entry_details) == 4:
                    location = entry_details[0]
                    date = entry_details[1]
                    description = entry_details[2] + " " + entry_details[3]
                # This will print if the code has failed to account for something in detailes
                else:
                    raise ValueError("failed to account for detail in entry_details when date element is index 1 on entry_details list")
            # This will print if the above if statements failed to find the date block
            else:
                raise ValueError("failed to find and account for date element in entry_details list")
        except ValueError as e:
            error.append(str(e))

        """
        get_id
        """
        try:
            entry_id = entry_id[-9:]
        except:
            entry_id = "Error with getting ID"

        """
        location
        """
        try:
            if location != not_provided:
                location = location[:-1]
                location += ", "
            if "Fairfax Campus" in location:
                location = location.split(", Fairfax Campus, ")
                del location[-1]
            elif "Arlington Campus" in location:
                location = location.split(", Arlington Campus, ")
                del location[-1]
            else:
                location = [location]
        except Exception:
            error.append("Error with location")

        """
        time/date splicing
        """
        try:
            date = date.split(",")
            day = date[0]
            time = date[3][1:]
            date = date[1][1:] + "," + date[2]
            date = date.split(" ")
            month = date[0]
            monthday = date[1][:(len(date[1]) - 1)]
            year = date[2]
        except Exception:
            error.append("Error with time/date splicing")

        """
        time reformatting
        """
        try:
            time = time.replace(" ", "")
            time = time.split("-")
            try:
                timestop = convert_time(time[1])
            except ValueError:
                raise ValueError(str(time))
            if timestop == None:
                raise ValueError(str(time))
            if not (time[0][-2:] == "am") and not (time[0][-2:] == "pm"):
                if (time[1][-2:] == "am"):
                    timestart = convert_time(time[0] + "am")
                else:
                    timestart = convert_time(time[0] + "pm")
            else:
                timestart = convert_time(time[0])
        except Exception:
            error.append("Error with time reformatting")

        """
        Final prep and amendment
        """
        if (error == []):
            dictlist.append({
                "id": entry_id,
                "title": entry.title.text,
                "dayofweek": day,
                "dayofmonth": monthday,
                "month": month,
                "year": year,
                "timestart": timestart,
                "timestop": timestop,
                "location": location,
                "description": description
            })
        else:
            dictlist.append({"id": entry_id, "error": error})
    return dictlist
