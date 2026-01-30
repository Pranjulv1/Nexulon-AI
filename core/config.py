import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
    REGION = os.getenv("GOOGLE_CLOUD_REGION", "us-central1")
    # Path to memory file, sitting in the root directory
    MEMORY_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "neuro_memory.json")

settings = Settings()