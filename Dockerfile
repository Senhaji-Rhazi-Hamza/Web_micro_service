# Use an official Python runtime as a parent image
FROM python:3.7.1-slim

# Set the working directory to /server
WORKDIR /server

# Copy the current directory contents into the container at /server
COPY . /server

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 8300

# Define environment variable
ENV NAME World

# Run app.py when the container launches
CMD ["python3", "src/server.py"]
