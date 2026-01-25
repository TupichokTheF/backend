from fastapi import FastAPI
import uvicorn
from contextlib import asynccontextmanager

from app.api.main import api_router
from app.database import database

@asynccontextmanager
async def lifespan(app_: FastAPI):
    await database.init_database()
    yield
    await database.dispose()

app = FastAPI(
    lifespan=lifespan
)
app.include_router(api_router)


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)