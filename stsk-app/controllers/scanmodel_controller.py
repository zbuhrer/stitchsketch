# ./controllers/scanmodel_controller.py
import flet as ft
import requests
from services.scan_service import ScanService
from ui.widgets import ScanCard

    

class ScanModelController:
    def __init__(self, view):
        self.view = view
        self.processor_url = "http://stsk-processor:8000"

    def upload_image(self, job_id, image_path):
        url = f"{self.processor_url}/process/{job_id}"
        with open(image_path, "rb") as f:
            files = {"file": f}
            response = requests.post(url, files=files)
        return response.json()

    def get_job_status(self, job_id):
        url = f"{self.processor_url}/job/{job_id}"
        response = requests.get(url)
        return response.json()

    def load_scans(self):
        # This method should now return a list of processed jobs
        # You may need to query your database or the processor service
        pass
