from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI(
    title=os.getenv("APP_NAME", "AI Website Health Checker"),
    version=os.getenv("API_VERSION", "v1"),
    description="AI-powered website health checker with security, performance, SEO, and accessibility analysis"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "AI Website Health Checker API", "status": "running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# Import routes
from app.api.v1 import scan, report
app.include_router(scan.router, prefix="/api/v1")
app.include_router(report.router, prefix="/api/v1")