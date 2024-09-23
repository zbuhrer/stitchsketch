import flet as ft
from nav_pages import PageController, MainPage


def main(page: ft.Page):
    page.title = "Job Management App"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # Initialize the Page Controller and Main Page
    controller = PageController()
    main_page = controller.main_page

    # Add controls to the main page as needed
    main_page.controls.extend([
        ft.ElevatedButton("Go to Dashboard", on_click=lambda _: controller.main_page.navigate_to("dashboard")),
        ft.ElevatedButton("Go to Settings", on_click=lambda _: controller.main_page.navigate_to("settings")),
        ft.ElevatedButton("Go to Job Details", on_click=lambda _: controller.main_page.navigate_to("job_details")),
        ft.ElevatedButton("Go to Analytics", on_click=lambda _: controller.main_page.navigate_to("analytics")),
        ft.ElevatedButton("Go to Scan Model", on_click=lambda _: controller.main_page.navigate_to("scan_model")),
    ])

    # Display the main page
    page.add(main_page)

# Run the app
ft.app(target=main)
