from sonar.custom_exceptions import SonarException
from sonar.entity.artifact_entity import DataTransformationArtifact, ModelTrainerArtifact
from sonar.entity.config_entity import ModelTrainerConfig
from sonar.utils.main_utils import load_numpy_array_data, load_object, save_object
from sonar.ml.metric.classification_metric import get_classification_score
from sonar.ml.model.estimator import SonarModel 
from sklearn.neighbors import KNeighborsClassifier
from sonar.logger import logging
import os, sys
class ModelTrainer:
    
    def __init__(self,model_trainer_config:ModelTrainerConfig,data_transformation_artifact:DataTransformationArtifact) -> None:
        try:
            self.model_trainer_config=model_trainer_config
            self.data_transformation_artifact=data_transformation_artifact
        except Exception as e:
            raise SonarException(e,sys)
        
    def train_model(self, x_train, y_train):
        try:
            model = KNeighborsClassifier(n_neighbors=1)
            model.fit(x_train, y_train)
            return model
        except Exception as e:
            raise e
        
    def initiate_model_trainer(self)->ModelTrainerArtifact:
        try:
            logging.info("Getting the file path from data transformed data path")
            train_file_path = self.data_transformation_artifact.transformed_train_file_path
            test_file_path = self.data_transformation_artifact.transformed_test_file_path
            
            #loading training array and testing array
            logging.info("Loading the numpy array in memory")
            train_arr = load_numpy_array_data(train_file_path)
            test_arr = load_numpy_array_data(test_file_path)
            
            # The train and test split
            logging.info("Performing the train|test split")
            x_train, y_train, x_test, y_test = (
                train_arr[:, :-1],
                train_arr[:, -1],
                test_arr[:, :-1],
                test_arr[:, -1],
            )
            logging.info("Training the model")
            model = self.train_model(x_train=x_train , y_train=y_train)
            y_train_pred = model.predict(x_train)
            
            logging.info("Get the classification score")
            classification_train_metric = get_classification_score(y_true=y_train, y_pred=y_train_pred)
            logging.info("Checking the report...")
            if classification_train_metric.f1_score<=self.model_trainer_config.expected_accuracy:
                logging.info("Trained model is not good to provide expected accuracy")
                raise Exception("Trained model is not good to provide expected accuracy")

            logging.info("Predicting on y_test")
            y_test_pred = model.predict(x_test)
            classification_test_metric = get_classification_score(y_true=y_test, y_pred=y_test_pred)
            
            # logging.info("Checking for overfitting and underfitting")
            # #Overfitting and Underfitting
            # logging.info(abs(classification_train_metric.f1_score-classification_test_metric.f1_score))
            # diff = abs(classification_train_metric.f1_score-classification_test_metric.f1_score)
            # if diff>self.model_trainer_config.overfitting_underfitting_threshold:
            #     raise Exception("Model is not good try to do more experimentation.")

            logging.info("Loading the object in the memory. This is pickle for input feature fitted on Robust Scaler and PCA")
            preprocessor = load_object(file_path=self.data_transformation_artifact.transformed_object_file_path)

            model_dir_path = os.path.dirname(self.model_trainer_config.trained_model_file_path)
            logging.info("Saving the sonar trained model")
            os.makedirs(model_dir_path,exist_ok=True)
            sonar_model = SonarModel(preprocessor=preprocessor,model=model)
            save_object(self.model_trainer_config.trained_model_file_path, obj=sonar_model)

            # Model trainer artifact
            logging.info("Model Trainer Artifact")
            model_trainer_artifact = ModelTrainerArtifact(trained_model_file_path=self.model_trainer_config.trained_model_file_path, 
            train_metric_artifact=classification_train_metric,
            test_metric_artifact=classification_test_metric)
            logging.info(f"Model trainer artifact: {model_trainer_artifact}")
            return model_trainer_artifact
        
        except Exception as e:
            SonarException(e,sys)
        