from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app=FastAPI()

@app.get("/")
def root():
    return {"APP":"StockFlow MVP"}

@app.get("/health")
def health_check():
    return {"status":"OK"}
