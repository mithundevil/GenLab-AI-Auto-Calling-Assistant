from pyngrok import ngrok
import time
import sys

def start_tunnel(port=8000):
    try:
        print(f"--- Starting ngrok tunnel on port {port} ---")
        public_url = ngrok.connect(port).public_url
        print(f"\n* PUBLIC URL: {public_url}")
        print(f"* TWILIO WEBHOOK: {public_url}/voice")
        print("\nKeep this script running to maintain the tunnel.")
        print("Press Ctrl+C to stop.")
        
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\nStopping ngrok tunnel...")
        ngrok.disconnect(public_url)
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    start_tunnel()
