import json
import sqlite3
from pathlib import Path
from typing import Dict, Any, List
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

# Requirement 4: Open database and static folder using paths based on location of main.py
BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "data" / "nids_deploy.db"
STATIC_DIR = BASE_DIR / "static"

app = FastAPI(
    title="NIDS Dashboard",
    description="Exploratory Data Analysis Dashboard for AI-Powered Network Intrusion Detection System",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_db():
    if not DB_PATH.exists():
        raise HTTPException(
            status_code=503,
            detail="Deployment database (data/nids_deploy.db) not found. Run the ETL pipeline to generate it."
        )
    # Open SQLite in read-only mode for safety and concurrent access
    conn = sqlite3.connect(f"file:{DB_PATH.as_posix()}?mode=ro", uri=True)
    conn.row_factory = sqlite3.Row
    return conn


@app.get("/api/health")
def health():
    return {
        "status": "online",
