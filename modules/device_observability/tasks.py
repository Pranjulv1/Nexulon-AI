import time
from .redis_cache import save
from .metrics import get_full_system_stats  # <--- Import the real scanner

def run_deep_diagnostic(scan_id: str):
    print(f"🕵️ [Background] Starting Real Deep Scan ID: {scan_id}...")
    
    # 1. Simulate the time it takes to scan files
    time.sleep(3) 
    print(f"   ... Checking RAM & Disk ...")
    
    # 2. Get REAL Data
    stats = get_full_system_stats()
    
    # 3. Determine Health Score based on real data
    # (Simple logic: Start at 100, subtract points for high usage)
    score = 100
    if stats["cpu"] > 80: score -= 20
    if stats["memory"] > 80: score -= 20
    if stats["disk"] > 90: score -= 30
    
    report = {
        "scan_id": scan_id,
        "status": "Complete",
        "health_score": score,
        "metrics": stats,  # Real numbers
        "timestamp": int(time.time())
    }

    save(report)
    print(f"✅ [Background] Real Scan Finished! System Health: {score}/100")