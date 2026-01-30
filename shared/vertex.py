import vertexai
from vertexai.generative_models import GenerativeModel, Tool, Part, FunctionDeclaration
from core.config import settings
from shared.voice import generate_voice_google

# Import the Mission Control modules
from modules.device_observability.metrics import get_full_system_stats
from core.mission_data import send_command, read_mission_report

# Initialize Vertex AI
vertexai.init(project=settings.PROJECT_ID, location=settings.REGION)

# --- 1. DEFINE THE TOOLS (The Mission Control Panel) ---

# Tool 1: Manual Override (Force Stop/Start)
tool_control = FunctionDeclaration(
    name="manual_override",
    description="Manually terminate (kill) or start an application on the server.",
    parameters={
        "type": "object",
        "properties": {
            "action": {"type": "string", "enum": ["KILL", "START"]},
            "app_name": {"type": "string", "description": "Name of the process (e.g., chrome, notepad)"}
        },
        "required": ["action", "app_name"]
    },
)

# Tool 2: Mission Report (Read the Black Box)
tool_report = FunctionDeclaration(
    name="get_mission_report",
    description="Read the satellite logs to see past errors, auto-fixes, and system events.",
    parameters={
        "type": "object",
        "properties": {},
    },
)

# Tool 3: Live Status (Direct Sensor Check)
tool_status = FunctionDeclaration(
    name="get_live_status",
    description="Get real-time CPU and RAM balance status.",
    parameters={
        "type": "object",
        "properties": {},
    },
)

# Combine all tools into the toolkit
nexulon_tools = Tool(function_declarations=[tool_control, tool_report, tool_status])


# --- 2. THE BRAIN LOGIC (Nexulon) ---

def analyze_and_act_v3(audio_bytes: bytes = None, text_input: str = None) -> str:
    """
    Main Logic: Receives audio, decides which tool to use, and returns the result.
    """

    # Using 'gemini-2.5-flash' for maximum stability with tools
    model = GenerativeModel("gemini-2.5-flash", tools=[nexulon_tools])
    chat = model.start_chat()
    
    # System Prompt (Professional English - Mission Control Style)
    system_prompt = """You are Nexulon Mission Control. You are operating a critical satellite-grade server.
    
    PROTOCOL:
    1. Speak in concise, professional English (Military/Space-Ops style).
    2. If user says "Kill", "Stop", "Terminate" [App] -> Use 'manual_override(action="KILL")'.
    3. If user says "Show report", "What happened", "Logs" -> Use 'get_mission_report'.
    4. If user asks "Status", "System health", "Is everything okay?" -> Use 'get_live_status'.
    5. Confirm commands immediately. Do not offer advice, just execute or report.
    
    Example: "Command verified. Initiating termination sequence for Chrome."
    """
    
    # Prepare the input for Gemini
    input_parts = [system_prompt]
    if audio_bytes:
        input_parts.append(Part.from_data(data=audio_bytes, mime_type="audio/mp3"))
    if text_input:
        input_parts.append(text_input)

    # 1. Ask Gemini what to do
    try:
        response = chat.send_message(input_parts)
    except Exception as e:
        return f"Communication Error: {str(e)}"

    # 2. Check if Gemini wants to run a tool
    try:
        if not response.candidates: return "Signal lost. No response."
        function_call = response.candidates[0].content.parts[0].function_call
    except:
        return response.text 

    # 3. Execute the Tool
    if function_call:
        fname = function_call.name
        print(f"🛰️ Mission Control Executing: {fname}")
        api_response = ""
        
        if fname == "manual_override":
            action = function_call.args["action"]
            app = function_call.args["app_name"]
            
            # Send order to Satellite (satellite.py will execute it)
            send_command(mode="MANUAL", target_app=app, action=action)
            api_response = f"Command SENT. Satellite set to {action} {app} immediately."
            
        elif fname == "get_mission_report":
            # Read from the shared log file
            full_logs = read_mission_report()
            # Only give the last 3 events to keep it short
            recent_logs = full_logs[-3:] if full_logs else "No events recorded yet."
            api_response = f"Recent Mission Logs: {recent_logs}"

        elif fname == "get_live_status":
            # Direct sensor read
            stats = get_full_system_stats()
            api_response = f"Live Telemetry: CPU {stats['cpu']}%, RAM {stats['memory']}%."

        # 4. Final Summary (Tell the user what happened)
        final_response = chat.send_message(
            f"System Output: {api_response}. Summarize this for the operator in English."
        )
        return final_response.text

    # If no tool was needed, just chat
    return response.text