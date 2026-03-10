import sys
import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from database.db import init_db

# Adjust sys.path for local imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from backend.routes import router as api_router

app = FastAPI(title="GenLab AI Auto Calling Assistant")

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize DB
@app.on_event("startup")
def startup_event():
    init_db()

# Include Routes
app.include_router(api_router, prefix="/api")

# Mount Static Files (Frontend)
app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
