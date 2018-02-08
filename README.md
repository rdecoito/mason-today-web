# Mason Today

Mason Today Web is a shitty version of the Mason Today project. It will be the conglomeration of 2 horrible programmings trying their damnedest to write functioning code.

Currently, the API is hosted at `masontoday.zosman.com`.

We make soup. A lot of it.

This is currently licensed under the "wut" license. Plznosteal

Step 1 - xml parsing to create a massive dictionary of objects  
Step 2 - figure out how create an implement tag system  
Step 3 - Create a web page that list out all the events and change what are present and what aren't based on tag system  

# Setup instructions for local development

Mason Today currently supports developers on Linux and macOS systems. Here's our
walk-through of steps we will take:

1. Install `git` on your system.
2. Clone the whats-open codebase.
3. Get whats-open up and running with the method of your choice.

## 1) Install `git` on your system.

`git` is the version control system used for SRCT projects.

### On Linux Based Systems

**with apt:**

Open a terminal and run the following command:

    sudo apt update

This retrieves links to the most up-to-date and secure versions of your packages.

Next, with:

    sudo apt install git

you install `git` onto your system.

**with pacman:**

    pacman -S git

### On macOS

We recommend that you use the third party Homebrew package manager for macOS,
which allows you to install packages from your terminal just as easily as you
could on a Linux based system. You could use another package manager (or not
use one at all), but Homebrew is highly reccomended.

To get homebrew, run the following command in a terminal:

    /usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)

**Note**: You do NOT need to use `sudo` when running any Homebrew commands, and
it likely won't work if you do.

Next, to make sure Homebrew is up to date, run:

    brew update

Finally we can install git with:

    brew install git

## 2) Clone the mason-today-web codebase

Now, we're going to clone down a copy of the mason-today-web codebase from [git.gmu.edu](https://git.gmu.edu/srct/mason-today-web),
the SRCT code respository with SSH.

**a)** Configure your ssh keys by following the directions at:

[git.gmu.edu/help/ssh/README](http://git.gmu.edu/help/ssh/README).

**b)** Now, on your computer, navigate to the directory in which you want to download the project (ie. perhaps one called `development/SRCT`), and run

    git clone git@git.gmu.edu:srct/mason-today-web.git

## 3) Get mason-today-web up and running

Now that we have `git` setup and cloned down the code you can

    cd mason-today-web/

and get to working on setting up a development environment! There are two options
to go about doing this: `Docker` and `Manual Setup`.

### Docker

We can automate the setup process through [Docker](https://www.docker.com/what-docker)
containers! This allows us to quickly get started and standardize development
environments across machines.

Installing Docker on your system:

 - For macOS: https://docs.docker.com/docker-for-mac/
 - For Windows: https://docs.docker.com/docker-for-windows/
 - For your specific \*nix distro: https://docs.docker.com/engine/installation/

Additionally, you will need to install docker-compose: https://docs.docker.com/compose/install/

Next inside the `mason-today-web/` root directory run:

    docker build . -t 'mason-today-web'

This builds the docker image that we will deploy to the swarm in a stack.

Initialize your swarm:

    docker swarm init

And finally,

    docker stack deploy mason-today_stack -c docker-compose.yml

You should see that the server is running by going to http://localhost:80
in your browser. Any changes you make to your local file system will be mirrored in the server.

### Manual Setup

Manual Setup involves all of the same steps as Docker, but just done manually.

First, install python, pip, and virtualenv on your system.
  * `python` is the programming language used for Django, the web framework used by whats-open.
  * `pip` is the python package manager.
  * `virtualenv` allows you to isolate pip packages within virtual environments

Open a terminal and run the following command:

    sudo apt update

Next, with:

    sudo apt install python3 python3-dev python3-pip
    sudo pip3 install virtualenv

you install `python`, `pip`, and `virtualenv`.

## The Virtual Enviornment

Virtual environments are used to keep separate project packages from the main
computer, so you can use different versions of packages across different
projects and ease deployment server setup.

It's often recommended to create a special directory to store all of your
virtual environments together (ie. development/virtualenv/), though they can be
placed wherever is most convenient.

Then in your virtual environment directory run:

    virtualenv -p python3 mason-today
    source mason-today/bin/activate

to create your virtual environment and activate it. If you ever need to exit
your virtual environment, simply run:

    deactivate

Now, the packages you need to install for Go are in in the top level of the
project's directory structure(mason-today-web/).

Next with,

    pip install -r requirements.txt

you setup the project.

# Running the local web server

Now that everything is set-up you can run the server on your computer.

    `./start.sh`

Go to http://127.0.0.1:8000/ in your browser and you should see the website.

With that, everything should be good to go!

# Modifying and Deploying Code

With the means of testing the website, you can really start contributing.

If you're new to Flask and don't know where to start, I highly recommend
giving the [tutorial](http://flask.pocoo.org/docs/0.12/tutorial/)
a try.

## CONTRIBUTING.md

This document goes into detail about how to contribute to the repo, including
guidelines for commit messages and details on the workflow of the project.

## Opening issues

There are templates for issue descriptions located on the new issue page. I will
close issues with poor descriptions or who do not follow the standard.

## Coding style

You should adhere to the style of the repo code. Consistency is key! PEP8
guidelines are strongly recommended but not enforced at the time. Please comment your code, I will not accept commits that contain uncommented code.

## Getting Help

I encourage you to join the [#masontoday-fwaque channel](https://srct.slack.com/messages/masontoday-fwaque/details/) in SRCT's [Slack Group](https://srct.slack.com)
if you have any questions on setup or would like to contribute.

