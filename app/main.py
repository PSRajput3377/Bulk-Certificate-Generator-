from fastapi import FastAPI

from .database import Base, engine
from .api.routes import router

app = FastAPI(
    title="Bulk Certificate Generator",
    description="API for bulk certificate generation",
    version="1.0.0",
)

Base.metadata.create_all(bind=engine)

app.include_router(router)


@app.get("/")
def root():
    return {
        "message": "Bulk Certificate Generator API is running"
    }