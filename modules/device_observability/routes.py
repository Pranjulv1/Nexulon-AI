from fastapi import APIRouter, UploadFile, File
from shared.vertex import analyze_and_act_v3
from shared.voice import generate_voice_google
import base64

router = APIRouter()

@router.post("/ask")
async def ask_nexulon(file: UploadFile = File(...)):
    # 1. Read Audio
    audio_bytes = await file.read()
    
    # 2. Brain Process
    bot_text = analyze_and_act_v3(audio_bytes=audio_bytes)
    
    # 3. Voice Gen
    audio_path = generate_voice_google(bot_text)
    
    # 4. Return
    with open(audio_path, "rb") as f:
        audio_b64 = base64.b64encode(f.read()).decode("utf-8")
        
    return {"bot_text": bot_text, "audio_base64": audio_b64}