############################################################
# Mason Today Web
############################################################

# Set the base image to Python
FROM python:3

# Copy project files to /mason-today-web
RUN mkdir /mason-today-web
WORKDIR /mason-today-web
ADD . /mason-today-web

# Install all required dependecies
RUN pip install -r requirements.txt
