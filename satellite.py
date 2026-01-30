import time
import psutil
from modules.device_observability.metrics import get_full_system_stats
from modules.device_observability.automations import kill_process, get_top_resource_hogs, clean_temp_files
from core.mission_data import get_command, log_event, send_command

def maintain_balance(cpu, ram):
    """
    Satellite Stability Logic:
    Ye function decide karta hai ki system ko kaise bachana hai.
    """
    # 1. READ COMMANDS: Kya User ne koi specific order diya hai?
    cmd = get_command()
    
    # AGAR USER NE KAHA: "ISKO ROKO" (Manual Override)
    if cmd["action"] == "KILL" and cmd["target_app"]:
        print(f"⚠️ COMMAND RECEIVED: Terminating {cmd['target_app']}...")
        success = kill_process(cmd["target_app"])
        result = "Success" if success else "Failed"
        log_event("MANUAL_COMMAND", f"User ordered kill on {cmd['target_app']}: {result}")
        # Command poora hone ke baad wapas AUTO mode me aao
        send_command("AUTO")
        return

    # AGAR MODE 'AUTO' HAI TO KHUD DIMAG LAGAO
    if cmd["mode"] == "AUTO":
        # LEVEL 1: WARNING / BALANCE (Yellow Zone)
        if cpu > 70 and cpu < 90:
            print(f"⚖️ Balancing Load (CPU: {cpu}%)... Cleaning Temp & Optimizing.")
            clean_temp_files() # Halka action
            log_event("BALANCE", f"High load ({cpu}%). Performed cleanup optimization.")

        # LEVEL 2: CRITICAL FIX (Red Zone)
        elif cpu >= 90:
            print(f"🚨 CRITICAL OVERLOAD ({cpu}%). Engaging Auto-Fix Protocols.")
            # Sabse heavy app dhundo
            hogs = get_top_resource_hogs("cpu") 
            # (Real scenario me hum parse karke top app nikalenge, abhi ke liye log kar rahe hain)
            # Example logic:
            # top_app = parse_hogs(hogs)
            # kill_process(top_app)
            
            log_event("AUTO_FIX", f"System critical. Detected heavy apps: {hogs}. Initiated countermeasures.")

def start_satellite():
    print("🛰️ Nexulon Satellite: Online & Monitoring...")
    print("   (System Balancing Active | Auto-Fix Enabled)")
    
    while True:
        try:
            # 1. Sense (Data Dekho)
            stats = get_full_system_stats()
            cpu = stats['cpu']
            ram = stats['memory']
            
            # 2. Think & Act (Balance banao ya Fix karo)
            maintain_balance(cpu, ram)
            
            # 3. Heartbeat Print
            status = "STABLE" if cpu < 70 else "BALANCING" if cpu < 90 else "CRITICAL"
            print(f"❤️ System: {status} | CPU: {cpu}% | RAM: {ram}%   ", end="\r")
            
            # Har 1 second me check karo (Real-time)
            time.sleep(1)
            
        except Exception as e:
            print(f"Satellite Error: {e}")
            time.sleep(1)

if __name__ == "__main__":
    start_satellite()