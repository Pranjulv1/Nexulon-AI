import psutil
import os
import shutil

def kill_process(process_name):
    """
    Kills a process by its name (e.g., 'notepad.exe').
    Returns True if successful, False if failed.
    """
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            # Check if name matches (case insensitive)
            if process_name.lower() in proc.info['name'].lower():
                proc.kill()
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False

def get_top_resource_hogs(resource_type="cpu"):
    """
    Returns the name of the process using the most CPU or RAM.
    """
    highest_usage = 0
    top_process = "None"
    
    for proc in psutil.process_iter(['name', 'cpu_percent', 'memory_percent']):
        try:
            if resource_type == "cpu":
                usage = proc.info['cpu_percent']
            else:
                usage = proc.info['memory_percent']
                
            if usage > highest_usage:
                highest_usage = usage
                top_process = proc.info['name']
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
            
    return f"{top_process} ({highest_usage}%)"

def clean_temp_files():
    """
    Safe Cleanup: Tries to delete files in the User's Temp folder.
    Ignores files that are currently in use.
    """
    temp_folder = os.environ.get('TEMP')
    if not temp_folder:
        return "Temp folder not found."
    
    deleted_count = 0
    bytes_freed = 0
    
    # List files in Temp directory
    try:
        for filename in os.listdir(temp_folder):
            file_path = os.path.join(temp_folder, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                    deleted_count += 1
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
                    deleted_count += 1
            except Exception:
                # If file is in use (Access Denied), just skip it.
                continue
    except Exception as e:
        return f"Cleanup Error: {e}"

    return f"Cleanup Complete. Removed {deleted_count} temporary items."