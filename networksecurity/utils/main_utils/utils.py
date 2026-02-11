import yaml
from networksecurity.exception.exception import CustomException
from networksecurity.logging.logger import logging
import sys
import os
import pickle
import numpy as np
import pandas as pd
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import f1_score, precision_score, recall_score

def read_yaml_file(file_path:str)->dict:
    """
    Docstring for read_yaml_file
    
    :param file_path: Description
    :type file_path: str
    :return: Description
    :rtype: dict
    this function reads a yaml file and returns the content as a 
    dictionary. It also handles exceptions and logs the process.
    """
    try:
        with open(file_path,'rb') as yaml_file:
            return yaml.safe_load(yaml_file)
    except Exception as e:
        raise CustomException(e,sys)

def write_yaml_file(file_path: str, content: object, replace: bool = False) -> None:
    """
    Docstring for write_yaml_file
    
    :param file_path: Description
    :type file_path: str
    :param content: Description
    :type content: object
    :param replace: Description
    :type replace: bool
    This function writes a Python object to a YAML file. 
    If the replace flag is set to True, it will overwrite 
    the existing file. It also handles exceptions and 
    logs the process.
    """
    try:
        if replace:
            if os.path.exists(file_path):
                os.remove(file_path)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w") as file:
            yaml.dump(content, file)
    except Exception as e:
        raise CustomException(e, sys)
    
def save_numpy_array_data(file_path: str, array: np.array) -> None:
    """
    Docstring for save_numpy_array_data
    
    :param file_path: Description
    :type file_path: str
    :param array: Description
    :type array: np.array
    This function saves a numpy array to a file. 
    It creates the directory if it does not exist and 
    handles exceptions while logging the process.
    """ 
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        with open(file_path, "wb") as file_obj:
            np.save(file_obj, array)
    except Exception as e:
        raise CustomException(e, sys)
    
def load_numpy_array_data(file_path: str) -> np.array:
    """
    Docstring for load_numpy_array_data
    
    :param file_path: Description
    :type file_path: str
    :return: Description
    :rtype: np.array
    This function loads a numpy array from a file. 
    It handles exceptions and logs the process.
    """ 
    try:
        with open(file_path, "rb") as file_obj:
            return np.load(file_obj)
    except Exception as e:
        raise CustomException(e, sys)
    
def save_object(file_path: str, obj: object) -> None:
    """
    Docstring for save_object
    
    :param file_path: Description
    :type file_path: str
    :param obj: Description
    :type obj: object
    This function saves a Python object to a file using pickle. 

    It creates the directory if it does not exist and handles 
    exceptions while logging the process.
    """ 
    try:
        logging.info(f"Saving object to file: {file_path}")
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        with open(file_path, "wb") as file_obj:
            pickle.dump(obj, file_obj)
        logging.info(f"Object saved successfully to file: {file_path}")
    except Exception as e:
        raise CustomException(e, sys)
    
def load_object(file_path: str) -> object:
    """
    Docstring for load_object
    
    :param file_path: Description
    :type file_path: str
    :return: Description
    :rtype: object
    This function loads a Python object from a file using pickle. 
    It handles exceptions and logs the process.
    """ 
    try:
        logging.info(f"Loading object from file: {file_path}")
        with open(file_path, "rb") as file_obj:
            obj = pickle.load(file_obj)
        logging.info(f"Object loaded successfully from file: {file_path}")
        return obj
    except Exception as e:
        raise CustomException(e, sys)
    
def evaluate_models(x_train,y_train,x_test,y_test,models,params):
    try:
        model_report:dict={}
        for model_name,model in models.items():
            logging.info(f"Evaluating model: {model_name}")
            param=params[model_name]
            gs=GridSearchCV(model,param,cv=5)
            gs.fit(x_train,y_train)
            model.set_params(**gs.best_params_)
            model.fit(x_train,y_train)
            y_train_pred=model.predict(x_train)
            y_test_pred=model.predict(x_test)
            train_model_f1_score=f1_score(y_train,y_train_pred)
            train_model_precision_score=precision_score(y_train,y_train_pred)
            train_model_recall_score=recall_score(y_train,y_train_pred)
            test_model_f1_score=f1_score(y_test,y_test_pred)
            test_model_precision_score=precision_score(y_test,y_test_pred)
            test_model_recall_score=recall_score(y_test,y_test_pred)
            logging.info(f"Best parameters for model {model_name}: {gs.best_params_}. With train f1 score: {train_model_f1_score}, train precision score: {train_model_precision_score}, train recall score: {train_model_recall_score} and test f1 score: {test_model_f1_score}, test precision score: {test_model_precision_score}, test recall score: {test_model_recall_score}")
            model_report[model_name]=test_model_f1_score
        return model_report
    
    except Exception as e:
        raise CustomException(e,sys)