# Use an official Python runtime as a parent image
FROM python:3.9

# Set the working directory in the container to /app
WORKDIR /app

# Add the current directory contents into the container at /app
ADD ./src/requirements.txt /app/requirements.txt

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

ADD ./src /app

EXPOSE 11434

# Run app.py when the container launches (use CMD instead if you want to pass 
CMD ["python", "app.py"]

