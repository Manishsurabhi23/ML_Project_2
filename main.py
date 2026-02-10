from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.components.data_validation import DataValidation
from networksecurity.components.data_transformation import DataTransformation
from networksecurity.exception.exception import CustomException
from networksecurity.logging.logger import logging
from networksecurity.entity.config_entity import DataIngestionConfig, DataValidationConfig, DataTransformationConfig
from networksecurity.entity.config_entity import TrainingPipelineConfig
from networksecurity.constant import training_pipeline

import sys
if __name__ == '__main__':
    try:
        training_pipeline_config = TrainingPipelineConfig()
        
        #data ingestion
        data_ingestion_config = DataIngestionConfig(training_pipeline_config)
        data_ingestion = DataIngestion(data_ingestion_config)
        logging.info("initiate the data ingestion")
        data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
        logging.info(f"data ingestion artifact: {data_ingestion_artifact}")
        logging.info("completed the data ingestion")
        
        #data validation
        data_validation_config = DataValidationConfig(training_pipeline_config)
        data_validation = DataValidation(data_ingestion_artifact, data_validation_config)
        logging.info("initiate the data validation")
        data_validation_artifact = data_validation.initiate_data_validation()
        logging.info(f"data validation artifact: {data_validation_artifact}")
        logging.info("completed the data validation")

        #data transformation
        data_transformation_config = DataTransformationConfig(training_pipeline_config)
        data_transformation = DataTransformation(data_validation_artifact, data_transformation_config)
        logging.info("initiate the data transformation")
        data_transformation_artifact = data_transformation.initiate_data_transformation()
        logging.info(f"data transformation artifact: {data_transformation_artifact}")
        logging.info("completed the data transformation")
    except Exception as e:
        raise CustomException(e,sys)