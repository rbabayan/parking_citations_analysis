from flask import Flask, request, jsonify
import logging
import os
import model_core

#fire up Flask
app = Flask(__name__)

#fire up logging framework and log to std output
log = logging.getLogger("assessment")
logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))

@app.route('/model', methods = ['POST'])
def model_api():
    input_data = request.json

    #log incoming data in standard output
    log.info("New input request received by API:")
    log.info(str(input_data))
    
    #send data to the prediction model
    try:
        prediction = model_core.get_prediction(log, input_data)
    except Exception as e:
        log.error('ERROR: model crashed for the given input')
        log.error(str(e))
        prediction = -1
    
    if prediction > 0: 
        result = {
            'popular_make_probability': prediction
        }
        return jsonify(result), 200
    
    return 'Error occurred. See server logs...', 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)