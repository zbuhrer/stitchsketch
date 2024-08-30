import subprocess
import time
import requests
from concurrent.futures import ThreadPoolExecutor
from dotenv import load_dotenv
import os

load_dotenv()

services = [
    {"name": "API Gateway", "command": ["python", "src/api_gateway.py"], "url": f"http://localhost:5005/health"},
    {"name": "UI", "command": ["flet run --web --port 3005 ui.py"], "url": ""},
]

def start_service(service):
    print(f"Starting {service['name']}...")
    return subprocess.Popen(service['command'], env=os.environ.copy())

def check_service_health(service):
    retries = 5
    while retries > 0:
        try:
            response = requests.get(service['url'], timeout=2)
            if response.status_code == 200:
                print(f"{service['name']} is up and running.")
                return True
        except requests.RequestException:
            pass
        retries -= 1
        time.sleep(2)
    print(f"Failed to start {service['name']}.")
    return False

async def main():
    processes = []
    with ThreadPoolExecutor() as executor:
        # Start all services
        processes = list(executor.map(start_service, services))

        # Check health of API Gateway service only
        results = [check_service_health(services[0])]
        if len(results) > 0 and all(results):
            print("API Gateway is up and running.")
        else:
            print("Failed to start API Gateway.")

    # Keep the script running
    try:
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        print("Stopping all services...")
        for process in processes:
            process.terminate()
        for process in processes:
            process.wait()
        print("All services stopped.")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
