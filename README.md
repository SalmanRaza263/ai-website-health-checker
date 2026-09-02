# Backend - AI Website Health Checker

## Setup

```bash
# Create virtual environment
python -m venv venv

# Activate
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run server
uvicorn app.main:app --reload