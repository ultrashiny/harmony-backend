from beanie import init_beanie
import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
from apps.user.models import User
from apps.profile.models import Profile

from apps.api import router
from apps.config import settings



app = FastAPI(
    title=settings.APP_NAME,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def app_init():
    app.mongodb_client = AsyncIOMotorClient(settings.DB_URL)
    app.mongodb = app.mongodb_client[settings.DB_NAME]

    await init_beanie(
        database=app.mongodb,
        document_models=[
            User,
            Profile
        ]
    )

@app.on_event("shutdown")
async def shutdown():
    app.mongodb_client.close()

app.include_router(router, prefix="/api")

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG_MODE,
        timeout_keep_alive=100,
        timeout_graceful_shutdown=150
    )