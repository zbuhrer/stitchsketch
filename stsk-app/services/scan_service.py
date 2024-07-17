# ./services/scan_service.py
import os

class ScanService:
    def __init__(self, base_directory='./scans'):
        self.base_directory = base_directory

    def get_scans(self):
        scans = []
        for job_id in os.listdir(self.base_directory):
            job_path = os.path.join(self.base_directory, job_id)
            if os.path.isdir(job_path):
                for scan_file in os.listdir(job_path):
                    if scan_file.endswith('.mp4'):
                        scans.append({
                            'job_id': job_id,
                            'scan_id': os.path.splitext(scan_file)[0],
                            'file_path': os.path.join(job_path, scan_file)
                        })
                        print(f"Found file: {os.path.join(job_path, scan_file)}")
        return scans
