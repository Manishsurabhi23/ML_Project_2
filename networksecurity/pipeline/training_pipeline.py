import os
import sys
from networksecurity.exception.exception import CustomException
from networksecurity.logging.logger import logging

from networksecurity.components.data_transformation import DataTransformation
from networksecurity.components.data_validation import DataValidation
from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.components.model_trainer import ModelTrainer

from networksecurity.entity.config_entity import DataIngestionConfig, DataValidationConfig, DataTransformationConfig, ModelTrainerConfig,TrainingPipelineConfig
from networksecurity.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact, DataTransformationArtifact, ModelTrainerArtifact

class TrainingPipeline:
    def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        try:
            self.training_pipeline_config=training_pipeline_config
        except Exception as e:
            raise CustomException(e,sys)
    
    def start_data_ingestion(self):
        try:
            self.data_ingestion_config = DataIngestionConfig(self.training_pipeline_config)
            data_ingestion = DataIngestion(data_ingestion_config=self.data_ingestion_config)
            logging.info("initiate the data ingestion")
            data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
            logging.info(f"data ingestion artifact: {data_ingestion_artifact}")
            logging.info("completed the data ingestion")
            return data_ingestion_artifact
        except Exception as e:
            raise CustomException(e,sys)
    
    def start_data_validation(self,data_ingestion_artifact:DataIngestionArtifact):
        try:
            self.data_validation_config = DataValidationConfig(self.training_pipeline_config)
            data_validation = DataValidation(data_validation_config=self.data_validation_config, data_ingestion_artifact=data_ingestion_artifact)
            logging.info("initiate the data validation")
            data_validation_artifact = data_validation.initiate_data_validation()
            logging.info(f"data validation artifact: {data_validation_artifact}")
            logging.info("completed the data validation")
            return data_validation_artifact
        except Exception as e:
            raise CustomException(e,sys)
    
    def start_data_transformation(self, data_validation_artifact: DataValidationArtifact):
        try:
            self.data_transformation_config = DataTransformationConfig(self.training_pipeline_config)
            data_transformation = DataTransformation(
                data_transformation_config=self.data_transformation_config,
                data_validation_artifact=data_validation_artifact
            )
            logging.info("initiate the data transformation")
            data_transformation_artifact = data_transformation.initiate_data_transformation()
            logging.info(f"data transformation artifact: {data_transformation_artifact}")
            logging.info("completed the data transformation")
            return data_transformation_artifact
        except Exception as e:
            raise CustomException(e, sys)
    
    def start_model_trainer(self, data_transformation_artifact: DataTransformationArtifact):
        try:
            self.model_trainer_config = ModelTrainerConfig(self.training_pipeline_config)
            model_trainer = ModelTrainer(
                model_trainer_config=self.model_trainer_config,
                data_transformation_artifact=data_transformation_artifact
            )
            logging.info("initiate the model training")
            model_trainer_artifact = model_trainer.initiate_model_trainer()
            logging.info(f"model trainer artifact: {model_trainer_artifact}")
            logging.info("completed the model training")
            return model_trainer_artifact
        except Exception as e:
            raise CustomException(e, sys)
    def run_pipeline(self):
        try:
            data_ingestion_artifact = self.start_data_ingestion()
            data_validation_artifact = self.start_data_validation(data_ingestion_artifact=data_ingestion_artifact)
            data_transformation_artifact = self.start_data_transformation(data_validation_artifact=data_validation_artifact)
            model_trainer_artifact = self.start_model_trainer(data_transformation_artifact=data_transformation_artifact)
            return model_trainer_artifact
        except Exception as e:
            raise CustomException(e,sys)