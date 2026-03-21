from fastapi import FastAPI
from routes.interview import router

app = FastAPI()

app.include_router(router)

@app.get("/")
def home():
    return {"message": "Hello World"}