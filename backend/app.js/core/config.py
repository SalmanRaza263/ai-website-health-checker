import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    APP_NAME = os.getenv("APP_NAME", "AI Website Health Checker")
    APP_ENV = os.getenv("APP_ENV", "development")
    DEBUG = os.getenv("DEBUG", "True").lower() == "true"
    SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key")
    API_VERSION = os.getenv("API_VERSION", "v1")
    
    SUPABASE_URL = os.getenv("SUPABASE_URL")
    SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")
    
    REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0")
    CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND", "redis://localhost:6379/0")
    
    NMAP_PATH = os.getenv("NMAP_PATH", "/usr/bin/nmap")
    RATE_LIMIT_PER_MINUTE = int(os.getenv("RATE_LIMIT_PER_MINUTE", "10"))
    MAX_SCAN_TIME = int(os.getenv("MAX_SCAN_TIME", "300"))

config = Config()