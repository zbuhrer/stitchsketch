# ./ui/widgets.py
import flet as ft

from models.models import Job


class ToasterMessage(ft.SnackBar):
    def __init__(self, goodorbad, message):
        self.goodorbad = goodorbad
        self.message = message
        super().__init__(content=(ft.Container(ft.Text(f"{self.goodorbad}{self.message}"))))

class JobGrid(ft.GridView):
    def __init__(self):
        super().__init__(
            expand=1,
            run_spacing=3,
            runs_count=1,
            max_extent=200,
            child_aspect_ratio=1.0,
            spacing=5,
            )
    def add_job_cards(self, jobs, on_click):
        self.controls = []
        self.jobs = jobs
        self.on_click = on_click
        for self.job in self.jobs:
            mini_job_card = MiniJobCard(self.job)
            self.controls.append(mini_job_card)

class MiniJobCard(ft.Container):
    def __init__(self, job: Job):
        self.job = job
        self.customer_widget = ft.ElevatedButton(f"{job.customer_id}")
        self.customer_widget.on_click = self.on_customer_click
        super().__init__(
            content=ft.Card(ft.Column(
                [
                    ft.Text(f"{job.name}", weight=ft.FontWeight.BOLD),
                    ft.Text(f"Status: {job.status}"),
                    self.customer_widget,
                    ft.Text(f"Created By: {job.created_by}"),
                    ft.Text(f"Modified On: {job.modified_on}"),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            )
        ))

    def on_customer_click(self, e, job):
        print(f"load customer info for {job.customer_id} into 'customer' object")

class JobCard(ft.Card):
    def __init__(self, job: Job):
        self.job = job
        super().__init__(
            content=ft.Column(
                [
                    ft.Text(f"{job.name}", weight=ft.FontWeight.BOLD),
                    ft.Container(ft.Text(f"{job.status}")),
                    ft.Text(f"Created By: {job.created_by}"),
                    ft.Text(f"Modified On: {job.modified_on}"),
                    ft.IconButton(ft.icons.INFO_OUTLINE, on_click=self.show_details),
                    ft.PopupMenuButton(
                                        items=[
                                            ft.PopupMenuItem(text="View Invoices", on_click=lambda e: self.view_invoices(self.job)),
                                            ft.PopupMenuItem(text="Assign Task", on_click=lambda e: self.assign_task(self.job)),
                                            ft.PopupMenuItem(text="Edit Job", on_click=lambda e: self.edit_job(self.job))
                                        ],
                                        icon=ft.icons.MORE_VERT,
                    )]))
    def show_details(self, job):
        return
    def view_invoices(self, job):
        return
    def assign_task(self, job):
        return
    def edit_job(self, job):
        return

border_radius = 52,
bgcolor = "#970000",
shadow = [
    ft.BoxShadow(
        offset = ft.Offset(-24, -24),
        blur_radius = 49,
        color = "#800000",
        blur_style = ft.ShadowBlurStyle.NORMAL,
    ),
    ft.BoxShadow(
        offset = ft.Offset(24, 24),
        blur_radius = 49,
        color = "#ad0000",
        blur_style = ft.ShadowBlurStyle.NORMAL,
    ),
],

class CustomAppBar(ft.AppBar):
    def __init__(self):
        self.refresh_button = ft.IconButton(ft.icons.REFRESH, on_click=lambda e: print("Refresh Clicked"))
        self.newtask_button = ft.IconButton(ft.icons.ADD_TASK, on_click=lambda e: print("Add Task Clicked"))

        self.dashboard_navoption = ft.PopupMenuItem(text="Dashboard")
        self.settings_navoption = ft.PopupMenuItem(text="Settings")
        self.testing_navoption = ft.PopupMenuItem(text="Testing")

        super().__init__(
            leading=ft.Icon(ft.icons.WORKSPACE_PREMIUM),
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
                        self.testing_navoption,
                        ft.PopupMenuItem(),
                    ]
                ),
            ],
        )
