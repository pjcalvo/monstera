# load env variables
from dotenv import load_dotenv
load_dotenv()

from flask import Flask, request, render_template, abort
from datetime import datetime
from store.store import store_client
from models.reading import Reading
from pymongo import DESCENDING

app = Flask(__name__)

# database support
readings = store_client.db['readings']

@app.route('/data', methods=['POST'])
def store_data():
    reading = Reading(**request.json)
    try:
        readings.insert_one(reading.to_dict())
        return 'Data stored successfully'
    except Exception as ex:
        abort(500, f'Error storing data: {str(ex)}')

@app.route('/', methods=['GET'])
def homepage():
    latest_reading = readings.find_one(sort=[('timestamp', DESCENDING)])
    if latest_reading is not None:
        return render_template('reading.html', **latest_reading)
    else:
        return render_template('no_readings.html')
    
@app.route('/historic', methods=['GET'])
def historic():    
    data = list(readings.find({}, {'_id': 0, 'timestamp': 1, 'percentage': 1}))
    # Pass the data to the template for rendering
    if len(data) > 0:
        return render_template('histogram.html', data=data)
    else:
        return render_template('no_readings.html')    

# on demand running
if __name__ == '__main__':
    app.run()
