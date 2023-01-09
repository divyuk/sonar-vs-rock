from typing import Union
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from sonar.pipeline.training_pipeline import TrainPipeline
from fastapi import Response, Request
from uvicorn import run as app_run
from sonar.constant.training_pipeline import SAVED_MODEL_DIR
from sonar.constant.application import APP_HOST, APP_PORT
from sonar.utils.main_utils import load_object
from starlette.responses import RedirectResponse
from sonar.ml.model.estimator import ModelResolver,TargetValueMapping
import sys
import pandas as pd

app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", tags=["authentication"])
async def index():
    return RedirectResponse(url="/docs")


@app.get("/train")
async def train_route():
    try:

        train_pipeline = TrainPipeline()
        if train_pipeline.is_pipeline_running:
            return Response("Training pipeline is already running.")
        train_pipeline.run_pipeline()
        return Response("Training successful !!")
    except Exception as e:
        return Response(f"Error Occurred! {e}")



@app.post("/predict")
async def predict_route(request: Request,file: UploadFile = File(...)):
    try:
        #get data from user csv file
        #conver csv file to dataframe
        df = pd.read_csv(file.file)
        model_resolver = ModelResolver(model_dir=SAVED_MODEL_DIR)
        if not model_resolver.is_model_exists():
            return Response("Model is not available")
        
        best_model_path = model_resolver.get_best_model_path()
        model = load_object(file_path=best_model_path)
        y_pred = model.predict(df)
        df['predicted_column'] = y_pred
        df['predicted_column'].replace(TargetValueMapping().reverse_mapping(),inplace=True)
        print( "DANGER ☠ MINE!!" if df['predicted_column'][0] == 'M' else "Rock" )
        # return df['predicted_column']
        return "☠ MINE!!" if df['predicted_column'][0] == 'M' else "Rock"  
        #decide how to return file to user.
        
    except Exception as e:
        raise Response(f"Error Occured! {e}")



if __name__=="__main__":    
    app_run(app, host=APP_HOST, port=APP_PORT)