import json
import os
from datetime import datetime
from core.config import settings

def init_memory():
    """Creates the memory file if it doesn't exist."""
    if not os.path.exists(settings.MEMORY_FILE):
        with open(settings.MEMORY_FILE, "w") as f:
            json.dump({"experiences": [], "system_health_log": []}, f)

def remember_event(problem, solution, outcome):
    """Stores a successful fix in long-term memory."""
    init_memory()
    with open(settings.MEMORY_FILE, "r+") as f:
        data = json.load(f)
        entry = {
            "timestamp": str(datetime.now()),
            "problem": problem,
            "solution": solution,
            "outcome": outcome
        }
        data["experiences"].append(entry)
        f.seek(0)
        json.dump(data, f, indent=4)

def recall_experience(problem_keyword):
    """Checks if we have faced this before."""
    if not os.path.exists(settings.MEMORY_FILE): return None
    
    with open(settings.MEMORY_FILE, "r") as f:
        data = json.load(f)
        for exp in data["experiences"]:
            if problem_keyword.lower() in exp["problem"].lower():
                return f"MEMORY RECALL: I previously fixed this issue using '{exp['solution']}' with outcome: {exp['outcome']}."
    return None

def log_health_snapshot(stats):
    """Continuously logs health for the 'Ask Anything' feature."""
    init_memory()
    with open(settings.MEMORY_FILE, "r+") as f:
        data = json.load(f)
        if len(data["system_health_log"]) > 50:
            data["system_health_log"].pop(0)
        data["system_health_log"].append({
            "time": str(datetime.now()),
            "stats": stats
        })
        f.seek(0)
        json.dump(data, f)

def get_recent_logs():
    """Returns the last 5 logs for context."""
    if not os.path.exists(settings.MEMORY_FILE): return "No history available."
    with open(settings.MEMORY_FILE, "r") as f:
        data = json.load(f)
    return str(data["system_health_log"][-5:])