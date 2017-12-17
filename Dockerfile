FROM bamos/openface:latest

# Expose the port  be used by the flask app
EXPOSE 5000

# Create a user and start using it.
RUN useradd -ms /bin/bash lobby
USER lobby

# Create a working directory and add all files to it.
WORKDIR /home/lobby/app
ADD . .

RUN pip install --ignore-installed -r requirements.txt

ENTRYPOINT ["python", "/home/lobby/app/faces.py"]

