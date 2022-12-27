from sonar.custom_exceptions import SonarException
from sonar.entity.artifact_entity import DataTransformationArtifact,DataValidationArtifact
from sonar.entity.config_entity import DataTransformationConfig
from sonar.logger import logging
from sklearn.preprocessing import RobustScaler
from sklearn.decomposition import PCA
from sklearn.pipeline import Pipeline
from sonar.constant.training_pipeline import TARGET_COLUMN
from sonar.ml.model.estimator import TargetValueMapping
from sonar.utils.main_utils import save_numpy_array_data, save_object
import sys
import numpy as np
import pandas as pd
class DataTransformation:
    def __init__(self,data_validation_artifact:DataValidationArtifact,
                 data_transformation_config:DataTransformationConfig) -> None:
        self.data_validation_artifact = data_validation_artifact
        self.data_transformation_config = data_transformation_config
        
    @staticmethod
    def read_data(file_path) -> pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise SonarException(e, sys)

    @classmethod
    def get_data_transformer_object(cls)->Pipeline:
        try:
            robust_scaler = RobustScaler()
            pca = PCA(n_components=20,random_state=42)
            preprocessor = Pipeline(
                steps=[
                    ("RobustScaler", robust_scaler), #keep every feature in same range and handle outlier
                    ("PCA" , pca)
                    ]
            )
            return preprocessor 
        except Exception as e:
            raise SonarException(e,sys)

    def initiate_data_transformation(self)->DataTransformationArtifact:
        try:
            logging.info("Reading the train data from validation artifact")
            train_df = DataTransformation.read_data(self.data_validation_artifact.valid_train_file_path)
            logging.info("Reading the test data from validation artifact")
            test_df = DataTransformation.read_data(self.data_validation_artifact.valid_test_file_path)
            logging.info("Getting the data Transformer object")
            preprocessor = DataTransformation.get_data_transformer_object()
            
            logging.info("Dropping the Target column from the training and test dataframe and replacing it with numerical label ")
            #training dataframe
            input_feature_train_df = train_df.drop(columns=[TARGET_COLUMN], axis=1)
            target_feature_train_df = train_df[TARGET_COLUMN]
            target_feature_train_df = target_feature_train_df.replace( TargetValueMapping().to_dict())
            
            #testing dataframe
            input_feature_test_df = test_df.drop(columns=[TARGET_COLUMN], axis=1)
            target_feature_test_df = test_df[TARGET_COLUMN]
            target_feature_test_df = target_feature_test_df.replace(TargetValueMapping().to_dict())
            
            logging.info("Using Preprocessor object to fit on the training data and using it transform on train as well as test data")
            
            preprocessor_object = preprocessor.fit(input_feature_train_df)
            transformed_input_train_feature = preprocessor_object.transform(input_feature_train_df)
            transformed_input_test_feature =preprocessor_object.transform(input_feature_test_df)
            #concating the arrays
            train_arr = np.c_[transformed_input_train_feature, np.array(target_feature_train_df) ]
            test_arr = np.c_[ transformed_input_test_feature, np.array(target_feature_test_df) ]

            #save numpy array data
            logging.info("Saving numpy as array data")
            save_numpy_array_data( self.data_transformation_config.transformed_train_file_path, array=train_arr, )
            save_numpy_array_data( self.data_transformation_config.transformed_test_file_path,array=test_arr,)
            save_object( self.data_transformation_config.transformed_object_file_path, preprocessor_object,)

            #preparing artifact
            logging.info("Preparing the artifact..")
            data_transformation_artifact = DataTransformationArtifact(
                transformed_object_file_path=self.data_transformation_config.transformed_object_file_path,
                transformed_train_file_path=self.data_transformation_config.transformed_train_file_path,
                transformed_test_file_path=self.data_transformation_config.transformed_test_file_path,
            )
            logging.info(f"Data transformation artifact: {data_transformation_artifact}")
            return data_transformation_artifact
        
        except Exception as e:
            raise SonarException(e,sys)