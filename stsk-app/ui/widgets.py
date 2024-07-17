# ./ui/widgets.py
import flet as ft
from flet.canvas import Canvas

from models.job import Job

        
class ScanCard(ft.Card):
    def __init__(self, scan):
        super().__init__()
        self.scan = scan
        
        if isinstance(self.scan, dict):
            self.scan_jobid = self.scan.get("job_id", "Unknown")
            self.scan_scanid = self.scan.get("scan_id", "Unknown")
        elif isinstance(self.scan, list) and len(self.scan) >= 2:
            self.scan_jobid = self.scan[0]
            self.scan_scanid = self.scan[1]
        else:
            self.scan_jobid = "Unknown"
            self.scan_scanid = "Unknown"

        self.content = ft.Column([
            ft.Text(value=f"Job ID: {self.scan_jobid}"),
            ft.Text(value=f"Scan ID: {self.scan_scanid}"),
            ft.ElevatedButton(text="Process")
        ])




class LiveCameraFeed(ft.WebView):
    def __init__(self, url):
        super().__init__(url=url)
        self._canvas = Canvas()

class NewJobBtn(ft.FloatingActionButton):
    def __init__(self):
        super().__init__(icon=ft.icons.ADD, text="Job")

class NavRailBtn(ft.NavigationRailDestination):
    def __init__(self, label, icon, selected_icon):
        super().__init__()
        # self.label=None
        # self.icon=None
        # self.selected_icon=None
        return 

class NavRail(ft.NavigationRail):
    def __init__(self, selected_index, on_change):
        super().__init__(
            label_type=ft.NavigationRailLabelType.NONE,
            extended=False,
            min_width=100,
            min_extended_width=400,
            group_alignment=-0.9,
            )
        print(f"{self.selected_index}, {self.label_type}, {self.extended}, {self.on_change}")
        return 

class FilePickerButton(ft.ElevatedButton):
    def __init__(self, text, on_click):
        super().__init__(text=text, on_click=on_click)

class ProgressDisplay(ft.Column):
    def __init__(self):
        super().__init__()
        self.progress_bar = ft.ProgressBar(width=400, value=0)
        self.progress_text = ft.Text("0% Complete")
        self.controls = [self.progress_bar, self.progress_text]

    def update_progress(self, progress):
        self.progress_bar.value = progress / 100
        self.progress_text.value = f"{progress:.2f}% Complete"
        self.update()

class PointCloudCanvas(ft.Container):
    def __init__(self, width, height):
        self.canvas = Canvas(width=width, height=height)
        super().__init__(
            content=self.canvas,
            border=ft.border.all(1, ft.colors.GREY_400),
            border_radius=10,
            padding=10
        )

    def paint_pointcloud(self, pointcloud_data):
        # Implement pointcloud rendering logic here
        pass

class JobTable(ft.DataTable):
    def __init__(self, jobs: Job):
        super().__init__()
        self.columns = [
            ft.DataColumn(label=ft.Text("ID")),
            ft.DataColumn(label=ft.Text("Name")),
            ft.DataColumn(label=ft.Text("Date Entered")),
            ft.DataColumn(label=ft.Text("Date Modified")),
            ft.DataColumn(label=ft.Text("Modified By")),
            ft.DataColumn(label=ft.Text("Created By")),
        ]
        self.rowcache = []
        self._buildtable(jobs)

    def _buildtable(self, jobs):
        for job in jobs:
            self.rowcache.append([
                ft.DataRow([ft.Text(job.id)]),
                ft.DataRow([ft.Text(job.name)]),
                ft.DataRow([ft.Text(job.date_entered.strftime("%Y-%m-%d"))]),
                ft.DataRow([ft.Text(job.date_modified.strftime("%Y-%m-%d"))]),
                ft.DataRow([ft.Text(job.modified_user_id)]),
                ft.DataRow([ft.Text(job.created_by)])
            ])
        self.rows = self.rowcache
