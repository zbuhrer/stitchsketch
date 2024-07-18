# controllers/main_controller.py
import flet as ft

from ui.pages import MainPage, PageController
from ui.widgets import NewJobBtn, NavRailBtn, NavRail
from ui.modals import NewJobModal
    

class MainController:
    def __init__(self, page: ft.Page):
        self.page = page
        
        self.page.title = "3D Mesh CRM System"
        self.page.theme = ft.Theme(color_scheme_seed="red")
        self.page_controller = PageController()
        self.main_page = MainPage(self.page_controller)
        self.njb = NewJobBtn()
        self.njm = NewJobModal()
        self.setup()

    def setup(self):
        nav_rail = self.create_nav_rail()
        self.page.add(
            ft.Row(
                [
                    nav_rail,
                    # ft.VerticalDivider(),
                    self.main_page,
                ],
                expand=True,
            )
        )

    def open_newjob(self, e):
        self.njm = NewJobModal()
        print(f"Opening {self.njm.semantics_label}")
        self.njm.modal = True
        self.page.update()
        return 

    def create_nav_rail(self):
        def on_nav_change(e):
            selected_index = e.control.selected_index
            page_name = ["dashboard", "job_details", "scan_model", "settings", "analytics"][selected_index]
            self.main_page.navigate_to(page_name)



        nav_rail = NavRail(
                selected_index=0,
                on_change=on_nav_change,)
        self.destinationdict = [
            {"label": "DashboardPage", "icon": ft.icons.BUILD_CIRCLE_OUTLINED, "selected_icon": ft.icons.BUILD_CIRCLE},
            {"label": "JobDetailsPage", "icon": ft.icons.BOOKMARK_OUTLINED, "selected_icon": ft.icons.BOOKMARK},
            {"label": "ThreeDPage", "icon": ft.icons.SHAPE_LINE_OUTLINED, "selected_icon": ft.icons.SHAPE_LINE},
            {"label": "SettingsPage", "icon": ft.icons.SETTINGS_OUTLINED, "selected_icon": ft.icons.SETTINGS},
            {"label": "AnalyticsPage", "icon": ft.icons.ANALYTICS_OUTLINED, "selected_icon": ft.icons.ANALYTICS},
            ]
        
        destinationlist = []
        # Create NavRail destinations
        for dest in self.destinationdict:
            navrail_btn = ft.NavigationRailDestination(label=dest["label"], icon=dest["icon"], selected_icon=dest["selected_icon"])
            print(f"Created navrail destination: {navrail_btn.label} with icon {navrail_btn.icon}")
            destinationlist.append(navrail_btn)
        
        nav_rail.destinations = destinationlist
        nav_rail.on_change = on_nav_change
        nav_rail.selected_index = 0
        nav_rail.leading = self.njb
        self.njb.on_click = self.open_newjob

        return nav_rail