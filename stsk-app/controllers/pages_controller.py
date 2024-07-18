from ui.pages import DashboardPage, SettingsPage, JobDetailsPage, AnalyticsPage, ScanModelPage
from ui.pages import BasePage


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