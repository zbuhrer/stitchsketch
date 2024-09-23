import flet as ft
from modals import JobModal
from widgets import JobCard, NewJobBtn
from page_classes import BasePage, DashboardPage, SettingsPage, JobDetailsPage, AnalyticsPage, ScanModelPage

class PageController:
    def __init__(self):
        self.main_page = MainPage(self)

    def get_page(self, page_name: str) -> ft.Page:
        if page_name == "dashboard":
            return DashboardPage()
        elif page_name == "settings":
            return SettingsPage()
        elif page_name == "job_details":
            return JobDetailsPage()
        elif page_name == "analytics":
            return AnalyticsPage()
        elif page_name == "scan_model":
            return ScanModelPage()
        else:
            raise ValueError(f"Page '{page_name}' not found")

class MainPage(ft.Column):
    def __init__(self, page_controller: PageController):
        super().__init__()
        self.page_controller = page_controller
        self.expand = True
        self.controls = [self.page_controller.get_page("dashboard")]

    def navigate_to(self, page_name: str):
        self.controls = [self.page_controller.get_page(page_name)]
        self.update()
