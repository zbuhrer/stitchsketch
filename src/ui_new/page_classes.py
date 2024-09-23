import random
import flet as ft
from modals import JobModal
from widgets import JobCard, NewJobBtn
from models.job import db_session, Job

class BasePage(ft.Page):
    def __init__(self, title: str):
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
        self.create_job_button = ft.ElevatedButton(text="New Job", on_click=self.open_modal)
        self.newjobmodal = JobModal(self)

        self.job_grid = ft.GridView(
            runs_count=3,
            horizontal=True,
            expand=True,
            run_spacing=5,
        )

        self.leftcolumn.controls.append(self.job_grid)
        self.rightcolumn.controls.append(self.create_job_button)

    def open_modal(self, e):
        self.newjobmodal.open = True
        self.update()

class SettingsPage(BasePage):
    def __init__(self):
        super().__init__("Settings")

class JobDetailsPage(BasePage):
    def __init__(self):
        super().__init__("Job Details")

class AnalyticsPage(BasePage):
    def __init__(self):
        super().__init__("Analytics")

class ScanModelPage(BasePage):
    def __init__(self):
        super().__init__("3D Scanning & Modeling")
