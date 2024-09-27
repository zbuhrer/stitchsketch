import flet as ft

from widgets import JobCard, NewJobBtn

from models.job import Job
from models.database import db_session

class DashboardPage(ft.Column):
    def __init__(self):
        super().__init__()
        print(f"initializing DashBoardPage")
        self.create_job_button = ft.ElevatedButton(text="New Job", on_click=lambda _: print(f"New Job Button Clicked"))
        self.job_grid = ft.Column()

        self.controls = [self.job_grid]
        self.expand = True

    def load_jobs(self):
        print(f"Loading jobs")
        jobs = db_session.query(Job).all()
        x = 0
        for job in jobs:
            print(f"Job: {job.id} - {job.name}, {job.status}")
            x += 1
            self.job_grid.controls.append(JobCard(job))
        print(f"Total job count: {x}")


class SettingsPage(ft.Column):
    def __init__(self):
        print(f"initializing SettingsPage")
        super().__init__()
