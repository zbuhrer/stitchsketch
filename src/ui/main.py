import flet as ft

from flet.fastapi.flet_fastapi import FastAPI

from models.models import Job, Employee
from modals import NewJobModal, JobModal
from nav_pages import DashboardPage, SettingsPage
from widgets import CustomAppBar, ToasterMessage

app = FastAPI()

def main(page: ft.Page):
    def route_change(route):
        job = Job()
        dashboard_page = DashboardPage()
        newjob_modal = NewJobModal(dashboard_page, app)
        job_modal = JobModal(dashboard_page, job)

        page.theme = ft.Theme(color_scheme_seed="red")
        page.title = "StitchSketch"
        page.window_frameless = True
        page.views.clear()
        page.appbar = CustomAppBar()
        page.appbar.newtask_button.on_click = lambda e: open_modal(open_modal(newjob_modal))
        page.appbar.dashboard_navoption.on_click = lambda e: on_nav_change("/dashboard")
        page.appbar.settings_navoption.on_click = lambda e: on_nav_change("/settings")
        page.appbar.testing_navoption.on_click = lambda e: on_nav_change("/testing")

        if page.route == "/dashboard":
            dashboard_page.load_jobs(open_modal(job_modal))
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

        elif page.route == "/testing":
            page.views.append(
                ft.View(
                    "/testing",
                    [
                        page.appbar,
                        ft.Text("Testing Page"),
                        ft.Column([
                            ft.Text("Sandbox"),

                        ])
                    ]
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

    def open_modal(modal: ft.AlertDialog):
        print(f"Modal opening: {modal}")
        modal.modal = True
        page.overlay.append(modal)
        modal.open = True
        page.add(modal)
        page.update()
        return modal

    def close_modal(modal):
        print(f"{modal} modal: closed")
        modal.open = False
        page.update()
        return modal

    page.on_route_change = route_change
    page.on_view_pop = view_pop

    page.go("/dashboard")

# ft.app(target=main, export_asgi_app=True)
# ft.app(target=main)

if __name__ == "__main__":
    ft.app(target=main)
