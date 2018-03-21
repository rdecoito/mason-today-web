# Mason Today Web

Mason Today Web is the backend API of the Mason Today project. 

Currently, the parscript's data is hosted at `masontoday.zosman.com`

Please refer to the requirements.txt for information on what packages to
install to properly run the program.

Step 1 - xml parsing to create a massive dictionary of objects  
Step 2 - figure out how create an implement tag system  
Step 3 - Create a web page that list out all the events and change what are
present and what aren't based on tag system  

## Setup instructions for local development

1) Create a `virtualenv`:

```sh
pip install virtualenv
virtualenv -p python3 venv-mason-today-web
source venv-mason-today-web/bin/activate
```

2) Install the project's dependencies by running:

```sh
pip install -r requirements.txt
```

3) Start the Flask development server by running:

```sh
./start.sh
```

## Project Goal

The goal of this project is to create a what's happening on mason today that is specialized for an individual where tags allow them to see events that interest and relate to them.

---
Version Goals:

Version 0.1
The first objective of this project is to create a list of events happening on mason by utilizing 25Live's available feeds. This will be written in Python and utilise a publicly available library for parsing information from the feed.
