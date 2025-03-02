from fastapi import FastAPI
from src.routers import predict, train

app = FastAPI()

app.include_router(predict.router, prefix="/predict", tags=["Predictions"])
app.include_router(train.router, prefix="/train", tags=["Model Training"])
