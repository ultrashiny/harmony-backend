import os
import uvicorn
from fastapi import FastAPI
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware

from app.db.mongodb import close_mongo_connection, connect_to_mongo

app = FastAPI()
load_dotenv()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

mongo = os.getenv("MONGO_URL")
db = os.getenv("DB")

@app.on_event("startup")
async def startup():
    connect_to_mongo(mongo, db)

@app.on_event("shutdown")
async def shutdown():
    close_mongo_connection()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)