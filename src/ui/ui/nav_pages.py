# ./ui/page_classes.py
import random
import flet as ft

from ui.modals import FormModal
from ui.widgets import NewJobBtn, ScanCard, JobCard

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
    def __init__(self, modal = False):
        super().__init__("Job Dashboard")

        self.job_grid = ft.GridView(
            runs_count=3,
            horizontal=True,
            expand=True,
            run_spacing=5,
        )
        self.leftcolumn.controls=[self.job_grid]
        self._populate_grid_view()

    def _populate_grid_view(self):
        print(f"Populating job grid.")

        jobs = db_session.query(Job).all()

        for job in jobs:
            print(f"Job {job.id}")
            self.job_grid.controls.append(JobCard(job))

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
