Mason Today Web is a shitty version of the Mason Today project. It will be the conglomeration of 2 horrible programmings trying their damnedest to write functioning code.

Currently, the parscript's data is hosted at `masontoday.zosman.com`

Please refer to the requirements.txt for information on what packages to install to properly run the program.

We make soup. A lot of it.

This is currently licensed under the "wut" license. Plznosteal

Step 1 - xml parsing to create a massive dictionary of objects  
Step 2 - figure out how create an implement tag system  
Step 3 - Create a web page that list out all the events and change what are present and what aren't based on tag system  

# Setup instructions for local development

1) Create a `virtualenv` if you know what that is  
2) Install the project's dependencies by running `pip install -r requirements.txt`  
3) Start the Flask development server by running `./start.sh`  

# Documentation for the packages we use
* Schedule https://pypi.org/project/schedule/
* redis-py http://redis-py.readthedocs.io/en/latest/