from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from contextlib import asynccontextmanager

from app.api.api_router import api_router
from app.database import database
from app.middleware.logging_middleware import CustomLoggingMiddleware

@asynccontextmanager
async def lifespan(app_: FastAPI):
    await database.init_database()
    yield
    await database.dispose()

app = FastAPI(
    lifespan=lifespan,
)
app.include_router(api_router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(CustomLoggingMiddleware)

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)