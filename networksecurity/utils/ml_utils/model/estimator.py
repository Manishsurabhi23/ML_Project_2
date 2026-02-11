import os,sys

from networksecurity.exception.exception import CustomException
from networksecurity.logging.logger import logging

class NetworkModel:
    def __init__(self,preprocessor,model):
        try:
            self.preprocessor = preprocessor #preprocessor is the data transformation object
            self.model=model
        except Exception as e:
            raise CustomException(e,sys)
    def predict(self,X):
        try:
            logging.info("Entering predict method of NetworkModel class")
            logging.info("Preprocessing the input data")
            X_transform=self.preprocessor.transform(X)
            logging.info("Making predictions using the trained model")
            return self.model.predict(X_transform)
        except Exception as e:
            raise CustomException(e,sys)