# Parking Citations Data Analysis

## Sections 
The repository contains the followings: 

1. run.sh: A shell script to: 
    1. Download the dataset from S3
    2. Install all Python requirements
    3. Train the data by calling train.py 
    4. Launch model server by calling api.py & model_core.py 
2. API Calls methods:
    1. api_client.py: a python script to call the model server
    2. curl example
    3. Postman collection
3. Notebook files
    1. model.ipynb: A notebook contains process to find the best training approach and model evaluation
    2. data_analysis.ipynb: A notebook contains EDA on raw data
    3. part_two.ipynb: A note book contains analysis related to the part two of the assessment  
4. Dockerfile: To build a linux image that runs the model (optional)

## How to run:

### Clone the repo
```
git clone parking_citations_analysis.git
```

### Option 1: Run locally:
#### Start a Python virtual env (optional)
In order to isolate your local python development environment for this project, you can take advantage of Python virtual environments [virtual environments](https://realpython.com/python-virtual-environments-a-primer/): 
```
> pip install virtualenv
> cd parking_citations_analysis/
> virtualenv venv
> source venv/bin/activate
```
You can leave the virtual environment in your termial by: 
```
> deactivate
```

#### Launch the server
The following shell script should download the required datasets (may take a few minutes), and train the data: 
```
> ./run.sh
```
Important note: If you do not have the dataset already downloaded in both forms of CSV, and SQLite DB, you need to set the following configuration flags to True in the script: 
```
#Should the dataset be downloaded?
download_data_enabled=1;

#Should the sqlite database be created?
create_sqlite_db_enabled=1;
```

If you want to re-train the model from the scratch, set the following configuration flat to True
(Please note that trainign the model may take hours.) :
```
#Should the model be trained? 
train_model_enabled=1;
```

If you get the following error when running the script: 
```
./run.sh: Permission denied
```
Add read/write/execution permissions to your file to everyone: 
```
chmod 777 run.sh
```

The script will launch a local Flask server for the model. 

If script runs with no issues, Flask should be running: 
```
INFO:werkzeug: * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
```
### Option 2: Docker
If you have Docker installed, build the docker image using the docker file:  
```
> cd parking_citations_analysis/
> docker build . -t citations
```
This takes a few minutes as the docker build process also downloads the dataset from S3 and creates a SQLite database copy out of it as well. 
Then you should be able to run the built container 
```
> docker run -it -p 5000:5000 citations 
```

### Call the model server with input data
For the pretrained model we only need to pass 4 columns: "Color", "Body Style", "Fine amount", "Plate Expiry Date"
You have three options to call the model server:


#### Option 1: A Python script (easiest)
There is also a quick python script (`api_client.py`) that uses Python's http.client library to call the API. You can modify the payload in code and run the script to call the model server. 

#### Option 2: CURL
Send your sample data from a separate terminal using curl:
```
curl --header "Content-Type: application/json" \
     --request POST \
     --data '{"Color": "WH", "Body Style": "PA", "Fine amount": 50.0,"Plate Expiry Date": 200304.0}' \
     http://localhost:5000/model
```
You should be able to see the response in form of a JSON object: 
```
{"popular_make_probability":55.23}
```

#### Option 3: Postman
If you have [Postman](https://www.postman.com/) installed, you can import the sample Postman collection in the repository where the API calls are pre-defined:
```
Parking-Citatations-Postman-Call.postman_collection.json
```

