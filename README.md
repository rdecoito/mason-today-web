Mason Today Web is a shitty version of the Mason Today project. It will be the conglomeration of 2 horrible programmings trying their damnedest to write functioning code.

Currently, the parscript's data is hosted at `masontoday.gmu.io`

Please refer to the requirements.txt for information on what packages to install to properly run the program.

We make soup. A lot of it.

This is currently licensed under the "wut" license. Plznosteal

Step 1 - xml parsing to create a massive dictionary of objects
Step 2 - figure out how create an implement tag system
Step 3 - Create a web page that list out all the events and change what are present and what aren't based on tag system  

# Setup instructions for local development

1) Have python 2 installed  
2) Create a `virtualenv` if you know what that is  
3) Install the project's dependencies by running `pip install -r requirements.txt`  
4) Install redis-server with `sudo apt install redis-server`  
5) Start the Flask development server by running `./start.sh`  

NOTE: redis-server is easy to exploit, as described in the redis quick start documentation below. Make sure you firewall the port your redis server is running on (if you open your server to outside IPs) to protect the database
NOTE 2: I'm not 100% sure, but I believe you may need to run the redis-server by typing `redis-server` into the terminal. Don't forget that you can use `redis-cli [command] [key]` to check to see if your database changes have been recorded (or to modify your db manually)

# Documentation for the packages we use

* Schedule https://pypi.org/project/schedule/
* redis-py http://redis-py.readthedocs.io/en/latest/
* redis quick start https://redis.io/topics/quickstart

# MasonToday Documentation

#### Modules
The masontoday functions are currently separated in a few modules:
* `parscript` parses the data from the 25Live XML
* `getconnectedscript` parses the data from the GetConnected XML
* `redisactions` holds the methods for interacting with the redisdb
* `appmethods` holds the methods for interacting with the app
* `__init__` initialises the server and sets up the URL Routing

#### App Structure
The app has three main components:
1) The Flask server [set up in \_\_init\_\_]  
    * Including the URL Routing (with the use of `@app.route("/")`)  
2) The Redis DB [set up in redisactions]  
    * Routed through localhost port 6379 (this can be changed)  
3) The scheduler [set up in appmethods]  
