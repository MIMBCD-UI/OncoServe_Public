# Use an official Python runtime as a parent image
FROM python:2.7-slim

# Set the working directory to /OncoServe
WORKDIR /OncoServe

# Copy the current directory contents into the container at /OncoServe
ADD . /OncoServe

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt
RUN pip install -r OncoNet/requirements.txt
RUN pip install -r OncoData/requirements.txt
RUN sudo apt-get install dcmtk


# Make port 5000 available to the world outside this container
EXPOSE 5000
EXPOSE 80

# Define environment variable
ENV NAME World

# Run app.py when the container launches
CMD ["python", "/OncoServe/interface.py"]
