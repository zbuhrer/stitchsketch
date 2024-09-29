import flet as ft
from models.job import Job, db_session


class JobModal(ft.AlertDialog):
    def __init__(self, dashboard_page: ft.Column, app):
        super().__init__(title=ft.Text("Create Job"))
        self.semantics_label = "new job form pop-up modal"
        self.modal = True

        # form fields
        self.job_name = ft.TextField(label="Job Name", hint_text="New Job", value="")
        self.job_description = ft.TextField(label="Job Description", hint_text="New Job Description", multiline=True)
        self.submit_button = ft.ElevatedButton(text="Create Job", on_click=lambda _: self.submit_job(dashboard_page, app))

        self.content = ft.Column([
            self.job_name,
            self.job_description,
            self.submit_button
        ])

    def submit_job(self, dashboard_page, app):
        job_name = self.job_name.value
        job_description = self.job_description.value
        print(f"Job creation simulated: {job_name}, {job_description}")
        self.open = False
        self.update()
        dashboard_page.update()

        # create job object
        # Job.create_job(self, name = job_name, created_by="Dev")
        try:
            job = Job(name=job_name, created_by="Dev")
            db_session.add(job)
            db_session.commit()
            print(f"Job created successfully: {job_name}")
            dashboard_page.job_grid.controls.clear()
            dashboard_page.load_jobs(app)
        except Exception as e:
            print(f"Error creating job: {e}")
