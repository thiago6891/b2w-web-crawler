# Use an official Python runtime as parent image
FROM python:3.5-slim

# Set the working directory to /web_app
WORKDIR /web_app

# Copy the current directory contents into the container at /web_app
ADD . /web_app

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 80

# Run web_app.py when the container launches
CMD ["python3", "web_app.py"]