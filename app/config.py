import os
from dotenv import load_dotenv

# Load .env or .env.test depending on mode
TESTING = os.getenv("TESTING") == "true"
load_dotenv(dotenv_path=".env.test" if TESTING else ".env")

# MongoDB
ATLAS_URI = os.getenv("ATLAS_URI")
DB = os.getenv("DB")
COLLECTION = os.getenv("COLLECTION")

# API Keys
SERPER_API_KEY = os.getenv("SERPER_API_KEY")

# AI Configs
USE_GEMINI = bool(os.getenv("GCP_PROJECT_ID"))
GCP_PROJECT_ID = os.getenv("GCP_PROJECT_ID")

# App Config
DEBUG = os.getenv("DEBUG", "false").lower() == "true"

# CORS settings
