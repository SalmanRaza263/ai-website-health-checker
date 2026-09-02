version: '3.8'

services:
  backend:
    build: .
    ports:
      - "8000:8000"
    environment:
      - SUPABASE_URL=${SUPABASE_URL}
      - SUPABASE_ANON_KEY=${SUPABASE_ANON_KEY}
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      - redis

  redis:
    image: redis:alpine
    ports:
      - "6379:6379"

  celery-worker:
    build: .
    command: celery -A app.workers.scan_worker worker --loglevel=info
    environment:
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      - redis
      - backend