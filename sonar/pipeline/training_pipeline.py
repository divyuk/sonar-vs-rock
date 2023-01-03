from sonar.entity.config_entity import TrainingPipelineConfig, DataIngestionConfig, DataValidationConfig, DataTransformationConfig, ModelTrainerConfig, ModelEvaluationConfig, ModelPusherConfig
from sonar.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact, DataTransformationArtifact, ModelTrainerArtifact, ModelEvaluationArtifact, ModelPusherArtifact
from sonar.components.data_ingestion import DataIngestion
from sonar .components.data_validation import DataValidation
from sonar.components.data_transformation import DataTransformation
from sonar.components.model_trainer import ModelTrainer
from sonar.components.model_evaluation import ModelEvaluation
from sonar.components.model_pusher import ModelPusher
from sonar.custom_exceptions import SonarException
from sonar.logger import logging
import sys
class TrainPipeline:
    is_pipeline_running = False
    def __init__(self) -> None:
        self.training_pipeline_config = TrainingPipelineConfig()
    
    def start_data_ingestion(self)->DataIngestionArtifact:
        try:
            self.data_ingestion_config = DataIngestionConfig(training_pipeline_config=self.training_pipeline_config)
            logging.info("Starting data ingestion")
            data_ingestion = DataIngestion(data_ingestion_config=self.data_ingestion_config)
            data_ingestion_artifact = data_ingestion.initate_data_ingestion()
            logging.info(f"Data ingestion completed and artifact: {data_ingestion_artifact}")
            return data_ingestion_artifact
        except Exception as e:
            raise SonarException(e,sys)
    
    def start_data_validaton(self,data_ingestion_artifact:DataIngestionArtifact)->DataValidationArtifact:
        try:
            data_validation_config = DataValidationConfig(training_pipeline_config=self.training_pipeline_config)
            data_validation = DataValidation(data_ingestion_artifact=data_ingestion_artifact,
            data_validation_config = data_validation_config
            )
            data_validation_artifact = data_validation.initiate_data_validation()
            return data_validation_artifact
        except Exception as e:
            raise SonarException(e,sys)
    
    def start_data_transformation(self,data_validation_artifact:DataValidationArtifact)->DataTransformationArtifact:
        try:
            data_transformation_config = DataTransformationConfig(training_pipeline_config=self.training_pipeline_config)
            data_transformation = DataTransformation(data_validation_artifact=data_validation_artifact,
            data_transformation_config=data_transformation_config
            )
            data_transformation_artifact =  data_transformation.initiate_data_transformation()
            return data_transformation_artifact
        except Exception as e:
            raise SonarException(e,sys)    
    
    def start_model_trainer(self,data_transformation_artifact:DataTransformationArtifact)->ModelTrainerArtifact:
        try:
            model_trainer_config = ModelTrainerConfig(training_pipeline_config=self.training_pipeline_config)
            model_trainer = ModelTrainer(model_trainer_config, data_transformation_artifact)
            model_trainer_artifact = model_trainer.initate_model_trainer()
            return model_trainer_artifact
        except Exception as e:
            raise SonarException(e,sys)
    
    def start_model_evaluation(self,data_validation_artifact:DataValidationArtifact,
                                 model_trainer_artifact:ModelTrainerArtifact)->ModelEvaluationArtifact:
        try:
            model_eval_config = ModelEvaluationConfig(self.training_pipeline_config)
            model_eval = ModelEvaluation(model_eval_config, data_validation_artifact, model_trainer_artifact)
            model_eval_artifact = model_eval.initiate_model_evaluation()
            return model_eval_artifact
        except Exception as e:
            raise SonarException(e,sys)
    
    def start_model_pusher(self,model_eval_artifact:ModelEvaluationArtifact):
        try:
            model_pusher_config = ModelPusherConfig(training_pipeline_config=self.training_pipeline_config)
            model_pusher = ModelPusher(model_pusher_config, model_eval_artifact)
            model_pusher_artifact = model_pusher.initiate_model_pusher()
            return model_pusher_artifact
        except  Exception as e:
            raise  SonarException(e,sys)
    
    def run_pipeline(self):
        try:
            TrainPipeline.is_pipeline_running = True
            data_ingestion_artifact:DataIngestionArtifact = self.start_data_ingestion()
            data_validation_artifact:DataValidationArtifact=self.start_data_validaton(data_ingestion_artifact=data_ingestion_artifact)
            data_transformation_artifact: DataTransformationArtifact = self.start_data_transformation(data_validation_artifact=data_validation_artifact)
            model_trainer_artifact:ModelTrainerArtifact = self.start_model_trainer(data_transformation_artifact)
            model_eval_artifact:ModelEvaluationArtifact = self.start_model_evaluation(data_validation_artifact, model_trainer_artifact)
            if not model_eval_artifact.is_model_accepted:
                raise Exception("Trained model is not better than the best model")
            model_pusher_artifact:ModelPusherArtifact = self.start_model_pusher(model_eval_artifact)
            TrainPipeline.is_pipeline_running=False
        except Exception as e:
            TrainPipeline.is_pipeline_running=False
            raise SonarException(e,sys)