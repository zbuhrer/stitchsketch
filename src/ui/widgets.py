# ./ui/widgets.py
import flet as ft
from flet.canvas import Canvas

from models.job import Job

class JobCard(ft.Card):
    def __init__(self, job: Job):
        super().__init__(
            content=ft.Column(
                [
                    ft.Text(f"{job.name}", weight=ft.FontWeight.BOLD),
                    ft.Text(f"Status: {job.status}"),
                    ft.Text(f"Created By: {job.created_by}"),
                    ft.Text(f"Modified On: {job.modified_on}")
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            )
        )

class CustomAppBar(ft.AppBar):
    def __init__(self):
        self.refresh_button = ft.IconButton(ft.icons.REFRESH, on_click=lambda e: print("Refresh Clicked"))
        self.newtask_button = ft.IconButton(ft.icons.ADD_TASK, on_click=lambda e: print("Add Task Clicked"))
        self.dashboard_navoption = ft.PopupMenuItem(text="Dashboard")
        self.settings_navoption = ft.PopupMenuItem(text="Settings")
        super().__init__(
            leading=ft.Icon(ft.icons.FORKLIFT),
            leading_width=40,
            title=ft.Text("StitchSketch"),
            center_title=False,
            bgcolor=ft.colors.SURFACE_VARIANT,
            actions=[
                self.refresh_button,
                self.newtask_button,
                ft.PopupMenuButton(
                    items=[
                        self.dashboard_navoption,
                        ft.PopupMenuItem(),  # divider
                        self.settings_navoption,
                        ft.PopupMenuItem(),  # divider
                    ]
                ),
            ],
        )
