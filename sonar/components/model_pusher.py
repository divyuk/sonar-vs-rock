from sonar.custom_exceptions import SonarException
from sonar.entity.artifact_entity import ModelPusherArtifact,ModelEvaluationArtifact
from sonar.entity.config_entity import ModelPusherConfig
from sonar.logger import logging
import os, sys, shutil

class ModelPusher:
    
    def __init__(self,
                model_pusher_config:ModelPusherConfig,
                model_eval_artifact:ModelEvaluationArtifact) -> None:
        try:
            self.model_pusher_config = model_pusher_config
            self.model_eval_artifact = model_eval_artifact
        except Exception as e:
            raise SonarException(e,sys)
        
    def initiate_model_pusher(self,)->ModelPusherArtifact:
        try:
            trained_model_path = self.model_eval_artifact.trained_model_path
            #Creating model pusher dir to save model
            logging.info("Creating Model Pusher dir and saving the model")
            model_file_path = self.model_pusher_config.model_file_path
            os.makedirs(os.path.dirname(model_file_path),exist_ok=True)
            shutil.copy(src=trained_model_path, dst=model_file_path)
            
            #saved model dir
            logging.info("Creating a saved Dir to save the final model")
            saved_model_path = self.model_pusher_config.saved_model_path
            os.makedirs(os.path.dirname(saved_model_path),exist_ok=True)
            shutil.copy(src=trained_model_path, dst=saved_model_path)
            
            #prepare artifact
            model_pusher_artifact = ModelPusherArtifact(saved_model_path=saved_model_path, model_file_path=model_file_path)
            return model_pusher_artifact
        
        except Exception as e:
            raise SonarException(e,sys)     