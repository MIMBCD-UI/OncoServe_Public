# Use an official Python runtime as a parent image
FROM python:3.6-stretch

# Copy the requirements file for the python packages
ADD requirements.txt requirements.txt

# Install any needed packages specified in requirements.txt
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y --no-install-recommends \
    dcmtk \
    freetds-dev \
    freetds-bin \
    && rm -rf /var/lib/apt/lists/*

# Install the python requirements for my code
RUN pip install -r requirements.txt

# Set the entrypoint for the container
COPY docker_scripts/entrypoint.sh entrypoint.sh

# Set the working directory to /OncoServe
WORKDIR /OncoServe

# Define environment variable
ENV NAME OncoServe

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Specify what to execute when the container starts
ENTRYPOINT ["/entrypoint.sh"]
CMD ["bash"]