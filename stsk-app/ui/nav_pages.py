# ./ui/page_classes.py
import flet as ft
from .widgets import ScanCard
from controllers.scanmodel_controller import ScanModelController


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

class ScanModelPage(Page):
    def __init__(self):
        super().__init__()
        self.controller = ScanModelController(self)

        self.gallery = ft.GridView(
            expand=1,
            runs_count=5,
            max_extent=150,
            child_aspect_ratio=1.0,
            spacing=10,
            run_spacing=10,
        )

        self.point_cloud_viewer = PointCloudViewer(width=800, height=600)

        self.content = Row([
            Column([self.gallery], expand=1),
            Column([self.point_cloud_viewer], expand=2)
        ])

    def did_mount(self):
        self.load_scans()

    def load_scans(self):
        self.scans = self.controller.load_scans()
        self.gallery.controls.clear()
        for scan in self.scans:
            scan_card = ScanCard(scan, on_click=self.on_scan_selected)
            self.gallery.controls.append(scan_card)
        self.update()

    def on_scan_selected(self, scan):
        # Assume scan has a 'file_path' attribute that points to the pointcloud directory
        self.point_cloud_viewer.load_pointcloud(scan.file_path)