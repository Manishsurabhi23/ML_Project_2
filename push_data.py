import pymongo
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv

import os
import sys
import certifi
import json

import pandas as pd
import numpy as np

from networksecurity.logging.logger import logging 
from networksecurity.exception.exception import CustomException

# Load environment variables from .env file
load_dotenv()

# Get MongoDB URI from environment variable
MONGO_DB_URL = os.getenv("MONGO_DB_URL")

ca = certifi.where()  # certificate authorities 

class NetworkDataExtract():
    def __init__(self):
        try:
            pass
        except Exception as e:
            raise CustomException(e, sys)
        
    def csv_to_json_convertor(self, file_path):
        try:
            data = pd.read_csv(file_path)
            data.reset_index(drop=True, inplace=True)
            records = list(json.loads(data.T.to_json()).values())
            logging.info(f"Converted CSV to JSON: {len(records)} records")
            return records
        except Exception as e:
            logging.error(f"Error converting CSV to JSON: {str(e)}")
            raise CustomException(e, sys)
    
    def insert_data_mongodb(self, records, database, collection):
        try:
            self.records = records
            self.mongo_client = MongoClient(MONGO_DB_URL, tlsCAFile=ca)
            self.database = self.mongo_client[database]
            self.collection = self.database[collection]
            self.collection.insert_many(self.records)
            logging.info(f"Inserted {len(self.records)} records into MongoDB: {database}.{collection}")
            return len(self.records)
        except Exception as e:
            logging.error(f"Error inserting data to MongoDB: {str(e)}")
            raise CustomException(e, sys)
        
if __name__ == '__main__':
    try:
        FILE_PATH = "Network_Data/phisingData.csv"
        DATABASE = "MANISH-AI"
        COLLECTION = 'NetworkData'
        
        networkobj = NetworkDataExtract()
        records = networkobj.csv_to_json_convertor(FILE_PATH)
        no_of_records = networkobj.insert_data_mongodb(records, DATABASE, COLLECTION)
        
        print(f"Success! {no_of_records} records inserted into MongoDB")
        
    except Exception as e:
        logging.error(f"Process failed: {str(e)}")
        raise CustomException(e, sys)