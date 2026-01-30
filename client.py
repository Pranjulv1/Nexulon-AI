import requests
import base64
import os

INPUT_AUDIO = "test.mp3"
API_URL = "http://127.0.0.1:8000/device/ask"

def send_request():
    if not os.path.exists(INPUT_AUDIO):
        print("❌ Error: test.mp3 missing. Run record.py first.")
        return

    print(f"📡 Sending to Nexulon...")
    with open(INPUT_AUDIO, "rb") as f:
        try:
            response = requests.post(API_URL, files={"file": (INPUT_AUDIO, f, "audio/mp3")})
            if response.status_code == 200:
                data = response.json()
                print(f"\n💬 AI: {data['bot_text']}")
                with open("response.mp3", "wb") as f_out:
                    f_out.write(base64.b64decode(data['audio_base64']))
                os.system("start response.mp3") 
            else:
                print(f"❌ Error: {response.text}")
        except Exception as e:
            print(f"❌ Connection Error: {e}")

if __name__ == "__main__":
    send_request()