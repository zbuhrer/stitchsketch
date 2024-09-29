import flet as ft

from fastapi import Query, Path, Depends
from flet.fastapi.flet_fastapi import List, FastAPI
from sqlalchemy.orm import Session

from models.database import db_session, get_db
from models.job import Job

from modals import JobModal
from nav_pages import DashboardPage, SettingsPage
from widgets import CustomAppBar


def __init__(self):
    route = "/dashboard"
    pass

app = FastAPI()

@app.get("/jobs/", response_model=None)
def get_jobs(db: Session = Depends(get_db)):
    job = Job(id=1, description="example description")
    return job

@app.post("/jobs/", response_model=None)
def new_job(name: str, description: str = Query(..., min_length=3), db: Session=Depends(get_db)):
    new_job = Job.create_job(name, description)
    return new_job

@app.get("/search/jobs/", response_model=None)
    # List[Job])
async def search_jobs(query: str, db: Session = Depends(get_db)):
    # job searching!
    jobs = db.query(Job).filter(Job.description.contains(query)).all()
    return jobs

def main(page: ft.Page):
    page.title = "StitchSketch"
    dashboard_page = DashboardPage(app)
    dashboard_page.load_jobs(app)
    job_modal = JobModal(dashboard_page, app)

    page.window_frameless = True

    def route_change(route):
        print(f"Setting route: {page.route}")
        page.views.clear()
        page.appbar = CustomAppBar()
        page.appbar.newtask_button.on_click = lambda e: open_modal(job_modal)
        page.appbar.dashboard_navoption.on_click = lambda e: on_nav_change("/dashboard")
        page.appbar.settings_navoption.on_click = lambda e: on_nav_change("/settings")
        if page.route == "/dashboard":
            page.views.append(
                ft.View(
                    "/dashboard",
                    [
                        page.appbar,
                        dashboard_page,
                    ]
                )
            )
            page.update()

        elif page.route == "/settings":
            page.views.append(
                ft.View(
                    "/settings",
                    [
                        page.appbar,
                        ft.Text("Settings Page"),
                        ft.FloatingActionButton(tooltip="Dashboard",icon=ft.icons.DASHBOARD, on_click=lambda _:page.go("/dashboard"))],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    vertical_alignment=ft.MainAxisAlignment.CENTER,
                )
            )

        page.update()

    def on_nav_change(new_route):
        print(f"Navigating: {new_route}")
        page.go(new_route)

    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    def open_modal(modal):
        print(f"{modal.semantics_label} modal: opened")
        page.overlay.append(modal)
        modal.open = True
        page.update()

    def close_modal(modal):
        print(f"{modal} modal: closed")
        modal.open = False
        page.update()

    page.on_route_change = route_change
    page.on_view_pop = view_pop

    page.go("/dashboard")



ft.app(target=main)
