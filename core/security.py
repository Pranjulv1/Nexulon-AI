from fastapi import Security, HTTPException, status
from fastapi.security.api_key import APIKeyHeader
import os

API_KEY_NAME = "x-api-key"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

async def get_api_key(api_key_header: str = Security(api_key_header)):
    # Load the key you just shared from .env
    CORRECT_KEY = os.getenv("NEXULON_API_KEY")
    
    if api_key_header == CORRECT_KEY:
        return api_key_header
    
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="🔒 Access Denied: Invalid Key"
    )