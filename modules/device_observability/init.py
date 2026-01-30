from fastapi import Depends
from core.security import get_api_key
from .routes import router

def register(app):
    print("✅ Registering device_observability module (🔒 SECURE MODE)")
    
    # This line forces the password check for every request
    app.include_router(
        router, 
        prefix="/device", 
        tags=["Device Observability"],
        dependencies=[Depends(get_api_key)]
    )