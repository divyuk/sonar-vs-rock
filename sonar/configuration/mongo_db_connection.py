import pymongo
import os
from sonar.constant.database import DATABASE_NAME,COLLECTION_NAME
from sonar.logger import logging
from dotenv import load_dotenv
import certifi
import pandas as pd
load_dotenv()
MONGO_DB_URL = os.getenv("MONGODB_URL_KEY")
certificate = certifi.where()

class MongoDbClient:

    def __init__(self,database_name=DATABASE_NAME) -> None:
        try:
            self.client = pymongo.MongoClient(MONGO_DB_URL,tlsCAFile=certificate)
            self.database = self.client[database_name]
            self.database_name = database_name
            logging.info("Database connected")
        except Exception as e:
            raise e

        
if __name__ == "__main__":
    m = MongoDbClient()