from fastapi import FastAPI

def create_app():
    return FastAPI(title="NexulonAI", description="Voice-enabled Observability Agent")