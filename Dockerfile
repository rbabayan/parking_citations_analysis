FROM ubuntu:latest

RUN apt-get update -y
RUN apt-get install -y python3-pip python3-dev build-essential curl wget 
RUN apt-get install libmysqlclient-dev -y
RUN apt-get install sqlite3 -y

RUN ln -s /usr/bin/python3 /usr/bin/python & \
    ln -s /usr/bin/pip3 /usr/bin/pip
    
COPY . /app

WORKDIR /app

# Let's download the file during build instead of runtime
RUN wget -O dataset.csv https://s3-us-west-2.amazonaws.com/pcadsassessment/parking_citations.corrupted.csv

# Also, let's create the SQLite database from the dataset now
RUN ./csv_to_sqlite.sh

ENTRYPOINT ./run.sh
