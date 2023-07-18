from datetime import datetime
import pytz

class Reading():
    def __init__(self, min_value, max_value, value, percentage, plant_metadata, sensor_metadata):

        # Convert the UTC datetime to CEST timezone
        utc_now = datetime.now(pytz.utc)
        cest_timezone = pytz.timezone('Europe/Paris')
        self.timestamp = utc_now.astimezone(cest_timezone)

        self.sensor_metadata = sensor_metadata
        self.min_value = min_value
        self.max_value = max_value
        self.value = value
        self.percentage = percentage
        self.plant_metadata = plant_metadata

    def to_dict(self):
        return {
            'timestamp': self.timestamp,
            'min_value': self.min_value,
            'max_value': self.max_value,
            'value': self.value,
            'percentage': self.percentage,
            'plant_metadata': self.plant_metadata,
            'sensor_metadata': self.sensor_metadata
        }

    def __repr__(self):
        return f'<Reading {self.id!r}>'