from sonar.custom_exceptions import SonarException
from sonar.data_access.sonar_data import SonarData
from sonar.entity.config_entity import DataIngestionConfig, TrainingPipelineConfig
from sonar.constant.database import COLLECTION_NAME
from sonar.logger import logging
import pandas as pd
from sklearn.model_selection import train_test_split

import sys
import os

class DataIngestion:
    
    def __init__(self,data_ingestion_config:DataIngestionConfig) -> None:
        try:
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise SonarException(e,sys)
    
    def export_data_into_feature_store(self):
        """
        Bringing data from MongoDB to feature store
        """
        try:
            logging.info("Starting exporting into feature store")
            sonar_data = SonarData()
            dataframe = sonar_data.export_data_as_dataframe(collection_name=self.data_ingestion_config.collection_name)
            feature_store_file_path = self.data_ingestion_config.feature_store_file_path
            dir_path = os.path.dirname(feature_store_file_path)
            os.makedirs(dir_path, exist_ok=True)
            dataframe.to_csv(feature_store_file_path,index=False,header=True)
            return dataframe
        except Exception as e:
            raise SonarException(e,sys)
        
    def split_data_as_train_test(self,dataframe):
        try:
            train_set,test_set = train_test_split(dataframe, test_size=self.data_ingestion_config.train_test_split_ratio)
            logging.info("Performed train test split on the dataframe")
            logging.info("Exited split_data_as_train_test method of Data_Ingestion class")
            dir_path = os.path.dirname(self.data_ingestion_config.training_file_path)
            os.makedirs(dir_path, exist_ok=True)
            logging.info(f"Exporting train and test file path.")
            train_set.to_csv(self.data_ingestion_config.training_file_path, index=False, header=True)
            test_set.to_csv(self.data_ingestion_config.testing_file_path, index=False, header=True)
            logging.info(f"Exported train and test file path.")
        except Exception as e:
            raise SonarException(e,sys)
    
    def initate_data_ingestion(self):
        try:
            dataframe = self.export_data_into_feature_store()
            self.split_data_as_train_test(dataframe=dataframe)
            logging.info("Done splitting train test")
        except Exception as e:
            logging.error(f"Error raised")
            raise SonarException(e,sys)

zero = TrainingPipelineConfig()
a= DataIngestionConfig(zero)
d = DataIngestion(a)
d.initate_data_ingestion()