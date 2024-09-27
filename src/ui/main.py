import flet as ft
from modals import JobModal
from nav_pages import DashboardPage, SettingsPage

def __init__(self):

    return

def main(page: ft.Page):
    page.title = "StitchSketch"

    def route_change(route):
        print(f"Setting route: {page.route}")
        page.views.clear()
        if page.route == "/dashboard":
            dashboard_page = DashboardPage()
            dashboard_page.load_jobs()
            job_modal = JobModal(dashboard_page)
            page.views.append(
                ft.View(
                    "/dashboard",
                    [
                        ft.Row(vertical_alignment=ft.CrossAxisAlignment.START,
                            controls=[
                                ft.FloatingActionButton(tooltip="Refresh",
                                    icon=ft.icons.REFRESH,
                                    on_click=lambda _: dashboard_page.load_jobs()),
                                dashboard_page

                        ]),
                        ft.FloatingActionButton(tooltip="New Job",icon=ft.icons.ADD_TASK,on_click=lambda e: open_modal(job_modal))
                    ]))
            page.update()

        elif page.route == "/settings":
            page.views.append(
                ft.View(
                    "/settings",
                    [ft.Text("Settings Page"),
                        ft.FloatingActionButton(tooltip="Dashboard",icon=ft.icons.DASHBOARD, on_click=lambda _:page.go("/dashboard"))],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    vertical_alignment=ft.MainAxisAlignment.CENTER,
                )
            )

        page.update()

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


ft.app(main, view=ft.AppView.WEB_BROWSER, port=8009)

# ft.app(target=main, view=ft.AppView.FLET_APP, port=8009)
