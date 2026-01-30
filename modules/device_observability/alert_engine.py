from .thresholds import THRESHOLDS

def check(metrics):
    alerts = []
    # Check CPU
    if metrics.get("cpu", 0) > THRESHOLDS["cpu"]:
        alerts.append("High CPU usage")
    
    # Can extend for memory/disk here if metrics provided
    return alerts