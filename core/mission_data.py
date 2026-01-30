import json
import os
from datetime import datetime

# Files to store status and logs
COMMAND_FILE = "command_link.json"
LOG_FILE = "mission_log.json"

def init_mission_files():
    """Files create karta hai agar nahi hain."""
    if not os.path.exists(COMMAND_FILE):
        # Default mode: AUTO (Satellite Mode)
        with open(COMMAND_FILE, "w") as f:
            json.dump({"mode": "AUTO", "target_app": None, "action": None}, f)
            
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, "w") as f:
            json.dump([], f)

def get_command():
    """Satellite check karti hai ki user ne koi order diya hai kya?"""
    init_mission_files()
    try:
        with open(COMMAND_FILE, "r") as f:
            return json.load(f)
    except:
        return {"mode": "AUTO"}

def send_command(mode, target_app=None, action=None):
    """User (Aap) Satellite ko order bhejte hain."""
    with open(COMMAND_FILE, "w") as f:
        json.dump({"mode": mode, "target_app": target_app, "action": action}, f)

def log_event(event_type, details):
    """Har action ko record karta hai."""
    init_mission_files()
    entry = {
        "time": str(datetime.now().strftime("%H:%M:%S")),
        "type": event_type,
        "details": details
    }
    
    # Read old logs, add new, save last 50
    with open(LOG_FILE, "r+") as f:
        try:
            logs = json.load(f)
        except: logs = []
        
        logs.append(entry)
        if len(logs) > 50: logs.pop(0)
        
        f.seek(0)
        json.dump(logs, f, indent=4)
        f.truncate()

def read_mission_report():
    """User ke liye full report nikalta hai."""
    with open(LOG_FILE, "r") as f:
        return json.load(f)