import pandas as pd
from datetime import datetime, timedelta

def get_condensed_data_every(collection, timeframe, interval):
    if timeframe is None:
        timeframe = 24
    if interval is None:
        interval = '5T'
    # Retrieve data from MongoDB
    end_time = datetime.now()
    start_time = end_time - timedelta(hours=int(timeframe))
    pipeline = [
        {
            '$match': {
                'timestamp': {'$gte': start_time, '$lte': end_time}
            }
        },
        {
            '$project': {
                '_id': 0,
                'timestamp': 1,
                'percentage': 1
            }
        }
    ]
    data = list(collection.aggregate(pipeline))
    if len(data) is 0:
        return data
    # Create a DataFrame from the retrieved data
    df = pd.DataFrame(data)

    # Convert the 'timestamp' column to datetime type
    df['timestamp'] = pd.to_datetime(df['timestamp'])

    # Set 'timestamp' column as the DataFrame's index
    df.set_index('timestamp', inplace=True)

    # Resample the data into 5-minute intervals and calculate the mean value
    df_resampled = df.resample(interval).mean()
    resampled_list = df_resampled.reset_index().to_dict('records')

    data_to_return = []
    # Print the resampled data
    for data in resampled_list:
        timestamp = data['timestamp'].to_pydatetime()
        percentage = data['percentage']
        data_to_return.append({'timestamp': timestamp, 'percentage': percentage})

    return data_to_return
