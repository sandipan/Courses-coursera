# Fetch ubuntu 18.04 LTS docker image
FROM ubuntu:20.04

# Install Python on your ubuntu image.
RUN \
  apt-get update && \
  apt-get install -y python3 python3-pip

# Make directories for storing your files.
RUN mkdir /grader

# The commands below copy files into the Docker image.
# Main grader file
COPY grader.py /grader/grader.py
# Helper functions
COPY util.py /grader/util.py

COPY feedback.json /shared/feedback.json

# Important: Docker images are run without root access on our platforms. Its important to setup permissions accordingly.
# Executable permissions: Required to execute grader.py
# Read/write permissions: Required to copy over the submission from shared/submission
RUN chmod a+rwx -R /grader/

# Setup the command that will be invoked when your docker image is run.
ENTRYPOINT ["grader/grader.py"]