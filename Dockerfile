FROM bamos/openface:latest

# Expose the port  be used by the flask app
EXPOSE 5000

# Create a user and start using it.
RUN useradd -ms /bin/bash lobby
USER lobby
WORKDIR /home/lobby/app

ADD requirements.txt .

USER root
RUN pip install --ignore-installed -r /home/lobby/app/requirements.txt

USER root

# Create a working directory and add all files to it.
ADD . .

ENTRYPOINT ["python", "/home/lobby/app/faces.py"]

