import time
import math
import os

def create_load():
    print(f"🔥 STRESS TEST STARTING (PID: {os.getpid()})")
    print("   Attempting to raise CPU usage...")
    
    end_time = time.time() + 20  # Run for 20 seconds
    
    # Mathematical heavy lifting to spike CPU
    while time.time() < end_time:
        [math.sqrt(i) for i in range(1000000)]
        
    print("✅ STRESS TEST FINISHED. Cooling down...")

if __name__ == "__main__":
    create_load()