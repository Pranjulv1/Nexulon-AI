import json
import os
import numpy as np

DATA_FILE = "system_stats.json"

def _load_history():
    if not os.path.exists(DATA_FILE): return []
    try:
        with open(DATA_FILE, "r") as f: return json.load(f)
    except: return []

def log_data(cpu):
    history = _load_history()
    history.append(cpu)
    if len(history) > 20: history.pop(0)
    with open(DATA_FILE, "w") as f: json.dump(history, f)

def predict_future():
    history = _load_history()
    
    # ⚡ FIX: If no data, give an instant "Online" status instead of making user wait
    if not history:
        return "System is online. initializing sensors. Current status appears stable."
    
    # If we have even 1 data point, we use it instantly
    if len(history) < 5:
        current = history[-1]
        return f"Sensors active. Current CPU load is {current}%. Establishing trend line..."
    
    # Full Brain Mode (Standard Logic)
    y = np.array(history)
    x = np.arange(len(y))
    slope, _ = np.polyfit(x, y, 1)
    current = history[-1]
    
    if slope > 1.0:
        return f"CRITICAL: CPU rising fast (Slope: {slope:.2f}). Current: {current}%."
    elif slope > 0.2:
        return f"Warning: CPU is increasing. Current: {current}%."
    elif slope < -0.2:
        return f"System load is decreasing. Current: {current}%."
    else:
        return f"System is stable at {current}%."