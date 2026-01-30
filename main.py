from fastapi import FastAPI
from modules.device_observability.routes import router as device_router
import uvicorn

app = FastAPI(title="Nexulon AI V3")

# Include the device routes
app.include_router(device_router, prefix="/device")

# ✅ FIX: Add a root route so the browser shows something
@app.get("/")
def read_root():
    return {
        "status": "online",
        "system": "Nexulon V3 Neuro-Core",
        "message": "System is active. Use /docs to view the API."
    }

if __name__ == "__main__":
    print("🚀 Nexulon V3 Neuro-Core Starting...")
    uvicorn.run(app, host="127.0.0.1", port=8000)