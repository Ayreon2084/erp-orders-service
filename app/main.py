"""Main FastAPI application entry point."""
import uvicorn
from fastapi import FastAPI

from app.api.v1.routers import api_v1_router


app = FastAPI(
    title="ERP Service API",
    description="ERP system",
    version="1.0.0"
)

app.include_router(api_v1_router, prefix="/api/v1")


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
