import sys
import os
import certifi
import numpy as np 
import pandas as pd

from networksecurity.utils.main_utils.utils import load_object
ca = certifi.where()

from dotenv import load_dotenv
load_dotenv()

mongo_db_url = os.getenv("MONGO_DB_URL")
import pymongo
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, File, UploadFile, Request
from fastapi.templating import Jinja2Templates
from uvicorn import run as app_run
from fastapi.responses import Response, JSONResponse, RedirectResponse
from networksecurity.pipeline.training_pipeline import TrainingPipeline  
from networksecurity.entity.config_entity import TrainingPipelineConfig   
from networksecurity.exception.exception import CustomException
from networksecurity.logging.logger import logging
from networksecurity.utils.ml_utils.model.estimator import NetworkModel


from networksecurity.constant.training_pipeline import DATA_INGESTION_COLLECTION_NAME
from networksecurity.constant.training_pipeline import DATA_INGESTION_DATABASE_NAME
client = pymongo.MongoClient(mongo_db_url, tlsCAFile=ca)

database = client[DATA_INGESTION_DATABASE_NAME]
collection = database[DATA_INGESTION_COLLECTION_NAME]

app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

templates = Jinja2Templates(directory="./templates")

@app.get("/",tags=["authentication"])
async def index():
    return RedirectResponse(url="/docs")


@app.post("/train", tags=["training"])
async def train_route(request: Request):
    try:
        train_pipeline = TrainingPipeline()
        train_pipeline.run_pipeline()
        return Response("training successful!!")
    except Exception as e:
        raise CustomException(e, sys)
    
@app.post("/predict")
async def predict_route(request: Request, file: UploadFile = File(...)):
    try:
        # Create output directory if it doesn't exist
        os.makedirs("predicted_output", exist_ok=True)
        
        # Read CSV properly
        contents = await file.read()
        from io import BytesIO
        df = pd.read_csv(BytesIO(contents))
        
        logging.info(f"Loaded dataframe with shape: {df.shape}")
        logging.info(f"Columns: {df.columns.tolist()}")
        
        # Load models
        preprocessor = load_object("final_models/preprocessor.pkl")
        final_model = load_object("final_models/model.pkl")
        network_model = NetworkModel(preprocessor=preprocessor, model=final_model)
        
        # Make predictions
        logging.info("Making predictions...")
        y_pred = network_model.predict(df)
        df["predicted_label"] = y_pred
        
        logging.info(f"Predictions shape: {y_pred.shape}")
        logging.info(f"Sample predictions: {y_pred[:5]}")
        
        # Save output
        output_path = "predicted_output/output.csv"
        df.to_csv(output_path, index=False)
        
        # Generate HTML table with proper styling
        table_html = df.to_html(
            classes="table table-striped table-bordered table-hover",
            index=False,
            border=0
        )
        
        logging.info(f"Table HTML length: {len(table_html)}")
        
        # Return response
        return templates.TemplateResponse(
            "table.html", 
            {
                "request": request, 
                "table": table_html  # Changed from table_html to table
            }
        )

    except Exception as e:
        logging.error(f"Prediction error: {str(e)}")
        import traceback
        traceback.print_exc()
        raise CustomException(e, sys)

if __name__ == "__main__":
    try:
        app_run(app, host="localhost", port=8000)
    except Exception as e:
        raise CustomException(e, sys)
