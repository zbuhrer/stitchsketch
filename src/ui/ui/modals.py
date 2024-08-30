import flet as ft
from models.job import Job


class NewJobModal(ft.AlertDialog):
    def __init__(self):
        super().__init__()
        
        # build all of our form fields 
        self.semantics_label = "new job form pop-up modal"
        self.job_name = ft.TextField(label="Job Name", hint_text="New Job", value="")
        self.job_description = ft.TextField(label="Job Description", hint_text="New Job Description", multiline=True)
        self.job_type = ft.Dropdown(label="Job Type")
        self.customer_name = ft.TextField(label="Customer Name", hint_text="New Customer Name")
        self.customer_address = ft.TextField(label="Customer Address", hint_text="New Customer Address", multiline=True)
        self.title = ft.Text("New Job")

        # not open by default obvs 
        # self.open=False
        
        # structure the content block inside the modal 
        self.content = ft.Column([
            self.job_name,
            self.job_description,
            self.job_type,
            ft.Divider(),
            self.customer_name,
            self.customer_address,
        ])
        
        # actionable doodads at the bottom of the modal 
        self.actions = [
            ft.ElevatedButton("Add", on_click=lambda e: print("Modal dialog dismissed!")),
            ft.ElevatedButton("Cancel", on_click=lambda e: print("Modal dialog dismissed!")),
        ]

    async def create_job(self):

        import datetime
              
        # make a job object via job model class 
        
        job = Job(
            id='00000id',
            name=f"{self.job_name.value}",
            date_entered=datetime.date.today(),
            date_modified=datetime.date.today(),
            modified_user_id='username',
            created_by='username',
            description=f"{self.job_description.value}"
            )
        print("Job Created:")
        print(f"{job}")
        return job 
