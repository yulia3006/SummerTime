import flet as ft

def main(page: ft.Page):
    page.title = "Подводная лодка"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # URL изображения фона
    background_image_url = "https://mistralaiblackforestprod.blob.core.windows.net/images/blackforest/aa24/f78b/-7cc/d-4454-84a0-a54f6dfa08c2/image.jpg"

    def create_map(e):
        page.add(ft.Text("Создана новая карта!", color=ft.Colors.WHITE))

    def get_additional_info(e):
        page.add(ft.Text("Дополнительная информация получена!", color=ft.Colors.WHITE))

    def show_calculations(e):
        page.add(ft.Text("Список расчётов выведен!", color=ft.Colors.BLACK))

    create_map_button = ft.ElevatedButton(
        text="Создать карту",
        on_click=create_map,
        color=ft.Colors.WHITE,
        bgcolor=ft.Colors.RED,
        width=400,
        height=300,
        style=ft.ButtonStyle(text_size = 20)
    )

    get_info_button = ft.ElevatedButton(
        text="?",
        on_click=get_additional_info,
        color=ft.Colors.BLACK,
        bgcolor=ft.Colors.PINK_100,
        width=60,
        height=60,
        style=ft.ButtonStyle(text_size=30)
    )

    show_calculations_button = ft.ElevatedButton(
        text="Вывести список расчётов",
        on_click=show_calculations,
        color=ft.Colors.BLACK,
        bgcolor=ft.Colors.GREEN_100,
        width=250,
        height=70,
        style=ft.ButtonStyle(text_size=16)
    )

    background_image = ft.Image(
        src=background_image_url,
        fit=ft.ImageFit.COVER,
        width=page.width,
        height=page.height
    )

    buttons_container = ft.Container(
        content=ft.Stack(
            [
                ft.Container(
                    content=create_map_button,
                    alignment=ft.alignment.center,
                ),
                ft.Container(
                    content=show_calculations_button,
                    alignment=ft.alignment.center_right,
                    padding=ft.padding.only(right=50)
                ),
                ft.Container(
                    content=get_info_button,
                    alignment=ft.alignment.bottom_right,
                    padding=ft.padding.only(right=50, bottom=50)
                )
            ],
            expand=True
        ),
        width=page.width,
        height=page.height
    )

    page.add(
        ft.Stack(
            [
                background_image,
                buttons_container
            ],
            expand=True
        )
    )

ft.app(target=main)
