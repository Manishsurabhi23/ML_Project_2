import yaml
from networksecurity.exception.exception import CustomException
from networksecurity.logging.logger import logging
import sys
import os
import pickle
import numpy as np
import pandas as pd

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