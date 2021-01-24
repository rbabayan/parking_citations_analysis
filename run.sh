#!/bin/bash

###########################
# global config variables #
###########################
#URL of where to download the dataset from:
data_url="https://s3-us-west-2.amazonaws.com/pcadsassessment/parking_citations.corrupted.csv";

#Should the dataset be downloaded?
download_data_enabled=0;

#Should the sqlite database be created?
create_sqlite_db_enabled=0;

#Should the model be trained?
train_model_enabled=0;

###########################
#   downloading dataset   #
###########################
echo
echo "Downloading dataset from S3....";
case $download_data_enabled in
  (1)   wget -O "dataset.csv" $data_url;;
  (0)   echo "Data download skipped due to download_data_enabled set to false!";;
esac

###########################
# installing requirements #
###########################
echo
echo "Installing required Python packages"
pip install -r requirements.txt

###########################
#    installing sqlite    #
###########################
echo
echo "Installing SQLITE if Linux...";
unameOut="$(uname -s)"
case "${unameOut}" in
    Linux*) sudo apt-get install sqlite3;;
esac

###########################
#    create sqlite db     #
###########################
case $create_sqlite_db_enabled in
  (1)   ./csv_to_sqlite.sh;;
  (0)   echo "SQLite db creation skipped due to create_sqlite_db_enabled set to false!";;
esac

###########################
#      training data      #
###########################
echo
echo "Training model..."
case $train_model_enabled in
  (1)   python train.py;;
  (0)   echo "Data training skipped due to train_model_enabled set to false!";;
esac

###########################
#     running server      #
###########################
echo
echo "Starting the model server..."
python api.py
