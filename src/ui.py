import flet as ft

class GalleryContent(ft.Container):
    def __init__(self):
        super().__init__()
        self.content = ft.Column(
            [
                ft.Text("Gallery Content"),
                ft.Image(src="https://example.com/gallery.jpg")
            ]
        )

class CameraContent(ft.Column):
    def __init__(self):
        super().__init__
        self.content = [
            ft.Text("Camera Content"),
            ft.ElevatedButton("Take Photo")
        ]

class SettingsContent(ft.Container):
    def __init__(self):
        super().__init__()
        self.content = ft.Column(
            [
                ft.Text("Settings Content"),
                ft.Switch(label="Notifications"),
                ft.Dropdown(label="Theme", options=[
                    ft.dropdown.Option("Light"),
                    ft.dropdown.Option("Dark")
                ])
            ]
        )

async def ui(page: ft.Page) -> None:
    async def handler(e):
        await asyncio.sleep(3)
        page.add(ft.Text("Handler clicked"))

    async def handler_async(e):
        await asyncio.sleep(3)
        page.add(ft.Text("Async handler clicked"))

    navigation_bar = ft.NavigationBar(
        [
            ft.NavigationItem(icon=ft.icons.BROWSE_GALLERY_OUTLINED, on_click=lambda e: page.go("/gallery"), label="Gallery"),
            ft.NavigationItem(icon=ft.icons.CAMERA, on_click=lambda e: page.go("/camera"), label="Camera"),
            ft.NavigationItem(icon=ft.icons.SETTINGS, on_click=lambda e: page.go("/settings"), label="Settings")
        ]
    )

    page.add(
        navigation_bar,
        ft.Container(content=GalleryContent().content),
        ft.ElevatedButton("Call handler", on_click=handler),
        ft.ElevatedButton("Call async handler", on_click=handler_async)
    )
