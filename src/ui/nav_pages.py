import flet as ft
from sqlalchemy import func

from widgets import JobGrid, MiniJobCard

from models.models import Job
from models.database import db_session

class DashboardPage(ft.Container):
    def __init__(self):
        super().__init__()
        print(f"initializing DashBoardPage")
        self.expand = True
        self.success_toaster = ft.SnackBar(content=ft.Text("Test Message (Success Condition)"))
        self.fail_toaster = ft.SnackBar(content=ft.Text("Test Message (Fail Condition)"))
        self.in_progress_column = ft.Column()
        self.complete_column = ft.Column()
        self.cancelled_column = ft.Column()

    def build(self):
        self.content = ft.Row([
            ft.Column([
                ft.Text("In Progress"),
                self.in_progress_column
            ]),
            ft.Column([
                ft.Text("Complete"),
                self.complete_column
            ]),
            ft.Column([
                ft.Text("Cancelled"),
                self.cancelled_column
            ]),
        ])
        self.expand = True

    def newjob_success(self, app):
        print(f"New Job Created Successfully")
        return


    def load_jobs(self, open_modal):
        self.load_in_progress_jobs(open_modal)
        # self.load_cancelled_jobs(app)
        # self.load_complete_jobs(app)

    def load_in_progress_jobs(self, open_modal):
        print(f"Loading in progress jobs")
        self.in_progress_column.controls = []
        jobs = db_session.query(Job).all()
        self.in_progress = [job for job in db_session.query(Job).filter(func.lower(Job.status) == "in progress").all()]
        for self.inprogress_job in self.in_progress:
            self.jobcard = MiniJobCard(self.inprogress_job)
            self.jobcard.on_click = open_modal
            self.in_progress_column.controls.append(self.jobcard)

    def load_complete_jobs(self, app):
        print(f"Loading complete jobs")
        self.app = app
        self.complete_column.controls = []
        jobs = db_session.query(Job).all()
        complete = [job for job in db_session.query(Job).filter(func.lower(Job.status) == "complete").all()]
        # for complete_job in complete:
            # self.complete_column.controls.append(MiniJobCard(job=complete_job))

    def load_cancelled_jobs(self, app):
        print(f"Loading cancelled jobs")
        self.app = app
        self.cancelled_column.controls = []
        jobs = db_session.query(Job).all()
        cancelled = [job for job in db_session.query(Job).filter(func.lower(Job.status) == "cancelled").all()]
        # for cancelled_job in cancelled:
        #     self.cancelled_column.controls.append(MiniJobCard(job=cancelled_job))



class SettingsPage(ft.Column):
    def __init__(self):
        print(f"initializing SettingsPage")
        super().__init__()
