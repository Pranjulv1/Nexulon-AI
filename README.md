# 🛰️ Nexulon-AI: The Autonomous SRE Agent

> **A Tier-3 AI Agent for Self-Healing Infrastructure Operations.**
> *Uses a Split-Brain Architecture to combine Generative AI reasoning with real-time system telemetry.*

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![AI](https://img.shields.io/badge/AI-Google%20Vertex%20AI%20(Gemini%202.5%20Flash)-orange)
![FastAPI](https://img.shields.io/badge/Framework-FastAPI-green)
![Status](https://img.shields.io/badge/System-Autonomous-red)

---

## 📖 Executive Summary
**Nexulon-AI** is not a chatbot. It is an autonomous **System Reliability Engineer (SRE)** that lives inside your server.

Unlike traditional scripts that just alert you when things break, Nexulon actively fixes them. It utilizes a **"Split-Brain" Architecture** where a background "Satellite" process handles real-time sensors and auto-remediation (the Body), while a Gemini-powered API handles complex reasoning and voice commands (the Brain).

If your CPU spikes to 95% at 3 AM, Nexulon doesn't wake you up—it analyzes the trend, identifies the rogue process, terminates it, and logs the incident for you to review in the morning.

---

## 🏗️ Architecture: The "Split-Brain" Design

The system is decoupled into two independent, asynchronous processes to ensure fail-safe operations.



### 1. 🧠 The Brain (Mission Control)
* **Role:** Cognitive Reasoning & Interface.
* **Tech:** FastAPI, Vertex AI (Gemini 2.5 Flash).
* **Function:**
    * Listens for voice commands (e.g., "Kill Chrome", "Analyze logs").
    * Translates natural language into structured JSON commands.
    * Queries the "Black Box" database for historical context.

### 2. 🛰️ The Satellite (The Body)
* **Role:** Real-time Telemetry & Execution.
* **Tech:** Python `psutil`, Low-level OS automation.
* **Function:**
    * **Heartbeat:** Monitors CPU, RAM, and Disk I/O every 1000ms.
    * **Auto-Heal:** Automatically triggers cleanup scripts when the system enters the "Yellow Zone" (70-90% load).
    * **Kill Switch:** Executes "Red Zone" protocols to terminate resource hogs before a crash occurs.

---

## ⚡ Key Capabilities

| Feature | Description |
| :--- | :--- |
| **🤖 Autonomous Self-Healing** | Automatically detects high load and cleans temp files/caches without user input. |
| **🗣️ Voice Command Interface** | Control your server using professional natural language commands. *"System is lagging, initiate cleanup."* |
| **📦 The "Black Box" Recorder** | An immutable JSON log (`mission_log.json`) records every sensor spike and autonomous action for audit. |
| **🛡️ Tool-Use (Function Calling)** | The AI can natively execute Python functions: `kill_process`, `search_web`, `read_file`. |

---

## 🛠️ Technical Stack

* **Core Logic:** Python 3.10+
* **LLM Engine:** Google Vertex AI (Gemini 2.5 Flash)
* **API Framework:** FastAPI (Uvicorn)
* **System Interface:** `psutil`, `subprocess`, `os`
* **Inter-Process Communication:** Asynchronous JSON Streams

---

## 🚀 Installation & Setup

### 1. Install Dependencies
First, clone the repository and install the required Python libraries using pip.

```bash
git clone [https://github.com/Pranjulv1/nexulon-ai.git](https://github.com/Pranjulv1/nexulon-ai.git)
cd nexulon-ai
```
```bash
pip install -r requirements.txt
```

---

### 2. Google Cloud Setup

This project uses Google Vertex AI (Gemini 2.5 Flash). To run the AI "Brain," you must authenticate your local machine with Google Cloud.

* **Create a Project:** Go to the [Google Cloud Console](https://console.cloud.google.com/) and create a new project.
* **Enable API:** Search for "Vertex AI API" and enable it.
* **Authenticate:** Install the [Google Cloud CLI](https://cloud.google.com/sdk/docs/install) and run:
```bash
gcloud auth application-default login
```

---
### 🎮 How to Operate

To run the full autonomous system, you need to open 3 separate Terminal windows to simulate the "Split-Brain" architecture.
### Terminal 1: Launch the Satellite (The Body)
*Runs in the background to monitor hardware and auto-heal.*
```bash
python satellite.py
```
*Output: 🛰️ Nexulon-AI Satellite: Online & Monitoring...*

### Terminal 2: Launch the Brain (The API)
*Starts the AI server to process intelligence.*
```bash
python main.py
```
*Output: Uvicorn running on http://127.0.0.1:8000*

### Terminal 3: The Operator (You)
*This terminal is used to send commands. It is a 2-step process:*

**Step 1: Record your command**
```bash
python record.py
```
*Speak now (e.g., "Kill Chrome"). Recording stops automatically after 5 seconds.*

**Step 2: Send to Mission Control**
```bash
python client.py
```
*The AI analyzes your audio, executes the command, and speaks the result back to you.*
