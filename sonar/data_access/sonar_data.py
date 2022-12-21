from sonar.configuration.mongo_db_connection import MongoDbClient
from sonar.constant.database import DATABASE_NAME
from sonar.custom_exceptions import SonarException
import sys
import pandas as pd
import numpy as np
from sonar.logger import logging
from typing import Optional

class SonarData:
    def __init__(self) -> None:
        """
        This is connection with mongo

        Raises:
            SonarException: raises Sonar Exception.
        """
        try:
            self.mongo_client = MongoDbClient(database_name=DATABASE_NAME)
            
        except Exception as e:
            raise SonarException("Unable to connect with the database", sys)
        
    def export_data_as_dataframe(self,collection_name:Optional[str]):
        """
        Export Collection and puts in dataFrame.
        """
        try:
            if DATABASE_NAME is None:
                collection = self.mongo_client.database[collection_name]
            else:
                collection = self.mongo_client.database[collection_name]
                
            df = pd.DataFrame(list(collection.find()))
            if "_id" in df.columns.to_list():
                df = df.drop(columns=["_id"],axis=1)
            df.replace({"na",np.nan},inplace=True)
            return df   
        except Exception as e:
            logging.error("Error raised")
            raise SonarException(e,sys)
        
# s =SonarData()
# df = s.export_data_as_dataframe("rockmine","sonardb")
# print(df.head(2))