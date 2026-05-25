import subprocess
import sys
import os
import time
import requests
import webbrowser

print("🤖 Starting Aadya Voicebot...")

# Step 1 - Kill any old processes
os.system("taskkill /F /IM python.exe 2>nul")
time.sleep(2)

# Step 2 - Start the bot in background
bot_process = subprocess.Popen(
    [sys.executable, "src/main.py", "start"],
    creationflags=subprocess.CREATE_NEW_CONSOLE
)
print("✅ Bot started! Waiting 5 seconds...")
time.sleep(5)

# Step 3 - Start token server in background
server_process = subprocess.Popen(
    [sys.executable, "token_server.py"],
    creationflags=subprocess.CREATE_NEW_CONSOLE
)
print("✅ Token server started! Waiting 3 seconds...")
time.sleep(3)

# Step 4 - Get room URL and open browser
print("🔗 Getting connection URL...")
for attempt in range(5):
    try:
        response = requests.get("http://localhost:8000/connect", timeout=5)
        data = response.json()
        room = data["room"]
        url = data["url"]
        print(f"✅ Room: {room}")
        print(f"✅ URL: {url}")

        # Step 5 - Connect bot directly to this room
        print("🎤 Connecting Aadya to room...")
        time.sleep(2)
        connect_process = subprocess.Popen(
            [sys.executable, "src/main.py", "connect", "--room", room],
            creationflags=subprocess.CREATE_NEW_CONSOLE
        )

        time.sleep(3)
        print("🌐 Opening browser...")
        webbrowser.open(url)
        print("\n✅ Everything is running!")
        print("Speak into your mic to talk to Aadya!")
        break
    except Exception as e:
        print(f"Attempt {attempt + 1} failed: {e}")
        time.sleep(2)

input("\nPress Enter to stop everything...")
bot_process.terminate()
server_process.terminate()
connect_process.terminate()
print("Stopped!")