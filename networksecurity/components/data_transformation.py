import sys
import os
import numpy as np
import pandas as pd
from sklearn.impute import KNNImputer
from sklearn.pipeline import Pipeline
from networksecurity.constant.training_pipeline import TARGET_COLUMN
from networksecurity.constant.training_pipeline import DATA_TRANSFORMATION_IMPUTER_PARAMS
from networksecurity.entity.artifact_entity import DataTransformationArtifact,DataValidationArtifact
from networksecurity.entity.config_entity import DataTransformationConfig
from networksecurity.exception.exception import CustomException
from networksecurity.logging.logger import logging
from networksecurity.utils.main_utils.utils import save_numpy_array_data,save_object 

class DataTransformation:
    def __init__(self,data_validation_artifact:DataValidationArtifact,
                 data_transformation_config:DataTransformationConfig):
        try:
            self.data_validation_artifact:DataValidationArtifact=data_validation_artifact
            self.data_transformation_config:DataTransformationConfig=data_transformation_config
        except Exception as e:
            raise CustomException(e,sys)
    @staticmethod
    def read_data(file_path:str)->pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise CustomException(e,sys)
    
    def get_data_transformer_object(self)->Pipeline:
        """
        Docstring for get_data_transformer_object
        
        :param self: Description
        :return: Description
        :rtype: Pipeline
        This function creates and returns a data transformation pipeline.
        parameters comes from constant file and it is used to create 
        the KNN imputer object trainiing_pipeline
        """ 
        try:
            logging.info("entering get_data_transformer_object method of DataTransformation class")
            knn_imputer=KNNImputer(**DATA_TRANSFORMATION_IMPUTER_PARAMS) #** -> key value pair
            processor:Pipeline=Pipeline(steps=[("KNNImputer",knn_imputer)])
            logging.info("Created data transformation object")
            return processor
        except Exception as e:
            raise CustomException(e,sys)
        
    def initiate_data_transformation(self)->DataTransformationArtifact:
        try:
            logging.info("Starting data transformation")
            train_df:pd.DataFrame=self.read_data(self.data_validation_artifact.valid_train_file_path)
            test_df:pd.DataFrame=self.read_data(self.data_validation_artifact.valid_test_file_path)
            logging.info("Read train and test data for data transformation")
            # processor:Pipeline=self.get_data_transformer_object()
            target_column:str=TARGET_COLUMN
            
            #training dataframe
            input_feature_train_df:pd.DataFrame=train_df.drop(columns=[target_column],axis=1)
            target_feature_train_df:pd.DataFrame=train_df[target_column]
            target_feature_train_df = target_feature_train_df.replace(-1,0)
            
            #test dataframe
            input_feature_test_df:pd.DataFrame=test_df.drop(columns=[target_column],axis=1)
            target_feature_test_df:pd.DataFrame=test_df[target_column]
            target_feature_test_df = target_feature_test_df.replace(-1,0)

            #knn imputer
            preprocessor:Pipeline=self.get_data_transformer_object()
            preprocessor_obj = preprocessor.fit(input_feature_train_df)
            transformed_input_train_feature = preprocessor_obj.transform(input_feature_train_df)
            transformed_input_test_feature = preprocessor_obj.transform(input_feature_test_df)
            logging.info("Applied data transformation (knn imputer) on train and test data")

            train_arr = np.c_[transformed_input_train_feature, np.array(target_feature_train_df)]
            test_arr = np.c_[transformed_input_test_feature, np.array(target_feature_test_df)]
            logging.info("Combined input features and target feature into numpy array for train and test data")

            #save numpy array
            save_numpy_array_data(file_path=self.data_transformation_config.transformed_train_file_path, array=train_arr)
            save_numpy_array_data(file_path=self.data_transformation_config.transformed_test_file_path, array=test_arr)
            save_object(file_path=self.data_transformation_config.transformed_object_file_path, obj=preprocessor_obj)
            logging.info("Saved transformed train and test data as numpy arrays")

            #preparing artifacts
            data_transformation_artifacts = DataTransformationArtifact(
                transformed_train_file_path=self.data_transformation_config.transformed_train_file_path,
                transformed_test_file_path=self.data_transformation_config.transformed_test_file_path,
                transformed_object_file_path=self.data_transformation_config.transformed_object_file_path #preprocessor
            )
            logging.info("Created data transformation artifacts")
            return data_transformation_artifacts
        except Exception as e:
            raise CustomException(e,sys)