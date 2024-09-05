# ./ui/page_classes.py
import flet as ft
from .widgets import ScanCard


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
        super().__init__("Dashboard")
        # Add dashboard-specific controls here

        self.rightcolumn.controls = []

    def _buildtable(self):
        self.jobtable = ft.DataTable()
        self.jobtable.columns = [
        ft.DataColumn(label=ft.Text("ID")),
            ft.DataColumn(label=ft.Text("Name")),
            ft.DataColumn(label=ft.Text("Date Entered")),
            ft.DataColumn(label=ft.Text("Date Modified")),
            ft.DataColumn(label=ft.Text("Modified By")),
            ft.DataColumn(label=ft.Text("Created By")),
            ]
        return self.jobtable


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
