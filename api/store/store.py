from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from os import getenv

MONGO_URI = api_key = getenv('MONGO_URI')

class MongoDBManager:
    def __init__(self):
        self.client = MongoClient(MONGO_URI, server_api=ServerApi('1'))
        try:
            self.client.admin.command('ping')
            print("Pinged your deployment. You successfully connected to MongoDB!")
        except Exception as e:
            print(e)
        self.db = self.client["iot-project"]
    
store_client = MongoDBManager()