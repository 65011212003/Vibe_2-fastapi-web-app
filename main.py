from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn

# Import routers
from app.routers import pages, api, auth

# Create FastAPI instance
app = FastAPI(
    title="FastAPI Web App",
    description="A simple web application built with FastAPI",
    version="0.1.0"
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Include routers
app.include_router(pages.router)
app.include_router(api.router, prefix="/api")
app.include_router(auth.router, prefix="/auth")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True) 