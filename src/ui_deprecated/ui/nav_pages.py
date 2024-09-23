# ./ui/page_classes.py
import random
import flet as ft

from ui.modals import JobModal
from ui.widgets import JobCard, NewJobBtn

from models.database import db_session
from models.job import Job


class BasePage(ft.Column):
    def __init__(self, title: str):
        super().__init__()
        self.expand = True
        self.leftcolumn = ft.Column([])
        self.rightcolumn = ft.Column([])
        self.title = title

        self.controls = [
            ft.Row(
                controls=[ft.Text(title, theme_style=ft.TextThemeStyle.TITLE_LARGE)],
                alignment=ft.MainAxisAlignment.CENTER
            ),
            ft.Row(
                expand=True,
                controls=[
                    self.leftcolumn,
                    self.rightcolumn,
                ],
            )
        ]

class DashboardPage(BasePage):
    def __init__(self):
        super().__init__("Job Dashboard")
        self.create_job_button = ft.ElevatedButton(text="New Job")
        self.newjobmodal = JobModal(self)

        self.job_grid = ft.GridView(
            runs_count=3,
            horizontal=True,
            expand=True,
            run_spacing=5,
        )

        self.leftcolumn.controls=[self.job_grid]
        self.leftcolumn.expand=True
        self.rightcolumn.controls=[self.create_job_button]

        self._build_columns()

    def _build_columns(self):
        print(f"Populating job grid.")
        self.create_job_button.on_click = self.open_modal
        print(f"Create Job Button on_click method: {self.create_job_button.on_click}")

        jobs = db_session.query(Job).all()

        for job in jobs:
            print(f"Job {job.id}")
            self.job_grid.controls.append(JobCard(job))

    def open_modal(self):
        self.newjobmodal.open = True
        self.update_async

class SettingsPage(BasePage):
    def __init__(self):
        super().__init__("Settings")
        # Add settings-specific controls here

class JobDetailsPage(BasePage):
    def __init__(self):
        super().__init__("Job Details")
        # Add job details-specific controls here

class AnalyticsPage(BasePage):
    def __init__(self):
        super().__init__("Analytics")
        # Add analytics-specific controls here

class ScanModelPage(BasePage):
    def __init__(self):
        super().__init__("3D Scanning & Modeling")
