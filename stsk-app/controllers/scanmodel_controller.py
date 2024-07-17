# ./controllers/scanmodel_controller.py
import flet as ft
import os
from services.scan_service import ScanService
from ui.widgets import ScanCard


class ScanModelController:
    def __init__(self, view):
        self.view = view
        self.scan_service = ScanService()

    def load_scans(self):
        scans = self.scan_service.get_scans()
        # Ensure scans is a list of dictionaries
        return [
            {
                "job_id": scan["job_id"],
                "scan_id": scan["scan_id"],
                "file_path": scan["file_path"]
            } for scan in scans
        ]