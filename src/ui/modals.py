import flet as ft

from models.models import Job
from models.database import db_session


def cancel(self):
    self.open = False
    self.update()
    return

class NewJobModal(ft.AlertDialog):
    def __init__(self, dashboard_page: ft.Container, app):
        super().__init__(title=ft.Text("Create Job"))
        self.semantics_label = "new job form pop-up modal"
        self.on_dismiss = lambda e: print("job modal dismissed")

        # form fields
        self.job_name = ft.TextField(label="Job Name", hint_text="New Job", value="")
        self.job_description = ft.TextField(label="Job Description", hint_text="New Job Description", multiline=True)
        self.submit_button = ft.ElevatedButton(text="Create Job", on_click=lambda _: self.submit_job(dashboard_page, app))
        self.cancel_button = ft.ElevatedButton(text="Cancel", on_click=lambda _: cancel(self))

        self.content = ft.Column([
            self.job_name,
            self.job_description,
            ft.Row([self.submit_button, self.cancel_button])
        ])

    def submit_job(self, dashboard_page, app):
        job_name = self.job_name.value
        job_description = self.job_description.value
        self.open = False

        # create job object
        try:
            job = Job(name=job_name, created_by="Dev")
            db_session.add(job)
            db_session.commit()
            dashboard_page.newjob_success(app)
            print(f"Job created successfully: {job_name}")
        except Exception as e:
            db_session.rollback()
            print(f"Error creating job: {e}")
        finally:
            self.update()
            dashboard_page.load_jobs(app)
            dashboard_page.update()

class JobModal (ft.AlertDialog):
    def __init__(self, dashboard_page: ft.Container, job: Job):
        super().__init__(title=ft.Text(f"Job {job.id}: {job.name}"))
        self.semantics_label = f"job modal for {job.name}"
        self.on_dismiss = lambda e: print(f"{job.name} modal dismissed")

        # self'd job details
        self.job = job
        self.job_name = ft.Text(f"{self.job.name}")
        self.job_status = ft.Container(ft.Text(f"{job.status}"))
        self.job_description = ft.Text(f"{self.job.description}")
        self.cancel_button = ft.ElevatedButton(text="Cancel", on_click=lambda _: cancel(self))
        self.build

    def build(self):
        self.content = ft.Column([self.job_name,self.job_status,self.job_description,self.cancel_button])
        return

    def open_modal(self, dashboard_page):
        self.modal = True
        self.open = True
        dashboard_page.update()
        return
