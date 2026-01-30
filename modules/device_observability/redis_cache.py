import redis
import json
import os
import time

try:
    r = redis.Redis.from_url(os.getenv("REDIS_URL"), decode_responses=True)
except Exception as e:
    print(f"Redis Connection Error: {e}")
    r = None

def save(metrics):
    if not r: return
    metrics["time"] = int(time.time())
    r.set("latest_metrics", json.dumps(metrics), ex=20)

def load():
    if not r: return None
    data = r.get("latest_metrics")
    return json.loads(data) if data else None