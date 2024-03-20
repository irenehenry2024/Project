#use an official python runtime as a parent image
FROM python:3.8

#Set environment variables for python
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

#Set the working directory in the container
WORKDIR /app

#Copy the requirements file into the container at /app
COPY requirements.txt