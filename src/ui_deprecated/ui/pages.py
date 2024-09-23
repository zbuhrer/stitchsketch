import flet as ft
from .nav_pages import DashboardPage, SettingsPage, JobDetailsPage, AnalyticsPage, ScanModelPage
from .nav_pages import BasePage
from .modals import JobModal


class PageController:
    def __init__(self):
        self.pages = {
            "dashboard": DashboardPage,
            "settings": SettingsPage,
            "job_details": JobDetailsPage,
            "analytics": AnalyticsPage,
            "scan_model": ScanModelPage,
        }
        self.current_page = None

    def get_page(self, page_name: str) -> BasePage:
        page_class = self.pages.get(page_name)
        if page_class:
            self.current_page = page_class()
            return self.current_page
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
