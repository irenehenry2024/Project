#use an official python runtime as a parent image
FROM python:3.8

#Set environment variables for python
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

#Set the working directory in the container
WORKDIR /app

#Copy the requirements file into the container at /app
COPY requirements.txt /app/

#Install any needed packages specified in requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

#Copy the current directory contents into the container at /app
COPY . /app/

#collect static files (if applicable, adjust based on your Django project)
# RUN python manage.py collectstatic --noinput