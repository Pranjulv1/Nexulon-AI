import vertexai
from vertexai.preview.generative_models import GenerativeModel
import os
from dotenv import load_dotenv

load_dotenv()

project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
print(f"Checking models for project: {project_id}...")

vertexai.init(project=project_id, location="us-central1")

try:
    # Try to list common models
    print("\n✅ AVAILABLE MODELS:")
    for model_name in ["gemini-1.5-pro", "gemini-1.5-flash", "gemini-1.0-pro", "gemini-pro"]:
        try:
            model = GenerativeModel(model_name)
            print(f"  - {model_name} [OK]")
        except Exception:
            print(f"  - {model_name} [NOT AVAILABLE]")
            
except Exception as e:
    print(f"\n❌ CRITICAL ERROR: {e}")