import requests
import webbrowser

try:
    response = requests.get("http://localhost:8000/connect")
    data = response.json()
    print(f"\nRoom: {data['room']}")
    print(f"URL: {data['playground_url']}")
    print("\nOpening browser...")
    webbrowser.open(data['playground_url'])
    print("Press Enter after you connect in the browser...")
    input()
except Exception as e:
    print(f"Error: {e}")
    print("Make sure token_server.py is running first!")