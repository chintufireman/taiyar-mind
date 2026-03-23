from fastapi import FastAPI
from routes.interview import router
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(router)




@app.get("/")
def home():
    return {"message": "Hello World"}