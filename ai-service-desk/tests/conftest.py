# tests/conftest.py

import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from fastapi.testclient import TestClient

# Project root (ai-service-desk/)
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Add project root to Python path
sys.path.insert(0, str(PROJECT_ROOT))

# Explicitly load .env from the project root
load_dotenv(PROJECT_ROOT / ".env")

# Import AFTER loading the environment
from app.main import app

client = TestClient(app)