import urequests

# chipset;sensor
SENSOR_METADATA = 'raspberry pi pico;grove moisture sensor'
# name; characteristics
PLANT_MEDATADA = 'monstera;close to the window'

def send_humidity_values(min_value, max_value, value, percentage):
    url = 'http://localhost:5000/data'  # Replace with the appropriate URL of your Flask app

    data = {
        'sensor_metadata': SENSOR_METADATA,
        'min_value': min_value,
        'max_value': max_value,
        'value': value,
        'percentage': percentage,
        'plant_metadata': PLANT_MEDATADA
    }

    try:
        response = urequests.post(url, json=data)
        response.raise_for_status()
        print('Humidity values sent successfully!')
    except urequests.exceptions.RequestException as err:
        print(f'Error sending humidity values: {err}')