import subprocess
import time
import requests
from concurrent.futures import ThreadPoolExecutor
from dotenv import load_dotenv
import os

load_dotenv()

services = [
    {"name": "API Gateway", "command": ["python", "src/api_gateway.py"], "url": f"http://localhost:{os.getenv('API_GATEWAY_PORT')}/health"},
    {"name": "Image Processing", "command": ["python", "src/image_processing_service.py"], "url": f"http://localhost:{os.getenv('IMAGE_PROCESSING_PORT')}/health"},
    {"name": "Reconstruction", "command": ["python", "src/reconstruction_service.py"], "url": f"http://localhost:{os.getenv('RECONSTRUCTION_PORT')}/health"},
    {"name": "Visualization", "command": ["python", "src/visualization_service.py"], "url": f"http://localhost:{os.getenv('VISUALIZATION_PORT')}/health"},
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
        
        # Check health of all services
        results = list(executor.map(check_service_health, services))

    if all(results):
        print("All services are up and running.")
    else:
        print("Some services failed to start. Check the logs for more information.")

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