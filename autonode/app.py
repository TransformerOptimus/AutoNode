from fastapi import FastAPI
from fastapi_sqlalchemy import DBSessionMiddleware
from autonode.controllers.autonode import router as autonode_router
from autonode.config.settings import Settings

config = Settings()

app = FastAPI()

app.add_middleware(
    DBSessionMiddleware, db_url=config.DB_URL, engine_args=config.db_engine_args
)

app.include_router(autonode_router, prefix="/api/autonode")


@app.get("/health")
async def health_check():
    return {"status": "AutoNode is Running"}
