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

class ScanModelPage(BasePage):
    def __init__(self):
        super().__init__("3D Scanning & Modeling")
        self.controller = ScanModelController(self)

        self.gallery = ft.GridView(
            expand=1,
            runs_count=5,
            max_extent=150,
            child_aspect_ratio=1.0,
            spacing=10,
            run_spacing=10,
            )

        self.progress_display = ft.Column([
            ft.ProgressBar(visible=False),
            ft.Text()
        ])

        self.leftcolumn = ft.Column([
            self.gallery,
            self.progress_display,
        ])

    def did_mount(self):
        self.load_scans()

    def load_scans(self):
        self.scans = self.controller.load_scans()
        print(f"scans: {self.scans}")
        self.gallery.controls.clear()
        for scan in self.scans:
            scan_card = ScanCard(scan)
            self.gallery.controls.append(scan_card)
        self.update()
        


        # self.controller = ScanModelController(self)
        # self.file_picker = ft.FilePicker(on_result=self.controller.on_file_selected)
        # self.upload_button = FilePickerButton(
        #     "Select Video File", on_click=lambda _: self.file_picker.pick_files(allow_multiple=False))
        # self.file_name = ft.Text("No file selected")
        # self.forward_interval = ft.TextField(label="Forward Interval", input_filter=ft.NumbersOnlyInputFilter(), value="4")
        # self.reverse_interval = ft.TextField(label="Reverse Interval", input_filter=ft.NumbersOnlyInputFilter(), value="3")
        # self.process_button = ft.ElevatedButton("Process Video", on_click=self.controller.process_video)
        # self.progress_display = ProgressDisplay()
        # self.pointcloud_canvas = PointCloudCanvas(width=300, height=200)
        # self.controlpanel = [
        #     ft.Row([self.upload_button, self.file_name]),
        #     self.file_picker,
        #     self.process_button,
        #     self.progress_display,]

        # self.leftcolumn.controls = self.controlpanel
        # self.rightcolumn.controls = [self.forward_interval, self.reverse_interval, self.pointcloud_canvas]