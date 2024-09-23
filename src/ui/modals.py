import flet as ft
from models.job import Job


class JobModal(ft.AlertDialog):
    def __init__(self, main_page):
        super().__init__(title=ft.Text("Create Job"))
        print(f"NewJobModal initialized")
        self.main_page = main_page
        self.semantics_label = "new job form pop-up modal"

        # form fields
        self.job_name = ft.TextField(label="Job Name", hint_text="New Job", value="")
        self.job_description = ft.TextField(label="Job Description", hint_text="New Job Description", multiline=True)
        self.submit_button = ft.ElevatedButton(text="Create Job", on_click=self.submit_job)

        self.content = ft.Column([
            self.job_name,
            self.job_description,
            self.submit_button
        ])

    def submit_job(self):
        job_name = self.job_name.value
        job_description = self.job_description.value
        print(f"Job creation simulated: {job_name}, {job_description}")

        # create job object
        # Job.create_job(self, name = job_name, created_by="Dev")
