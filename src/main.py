import flet as ft

def main(page: ft.Page):
    page.title = "Подводная лодка"
    page.bgcolor = ft.Colors.PINK_50  # Нежно-розовый фон
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # Создаем текстовые метки для вывода сообщений
    map_text = ft.Text("", color=ft.Colors.RED)
    calculations_text = ft.Text("", color=ft.Colors.GREEN_900)

    def create_map(e):
        map_text.value = "Карта создана"
        page.update()  # Обновляем страницу, чтобы отобразить изменения

    def get_additional_info(e):
        map_text.value = "Не передвигайте дальномер во время проведения замеров!"
        page.update()  # Обновляем страницу, чтобы отобразить изменения

    def show_calculations(e):
        calculations_text.value = "Расчёты:"
        page.update()  # Обновляем страницу, чтобы отобразить изменения

    create_map_button = ft.ElevatedButton(
        text="Создать карту",
        on_click=create_map,
        color=ft.Colors.WHITE,
        bgcolor=ft.Colors.RED,
        width=400,
        height=200
    )

    get_info_button = ft.ElevatedButton(
        text="?",
        on_click=get_additional_info,
        color=ft.Colors.BLACK,
        bgcolor=ft.Colors.PINK_100,
        width=50,
        height=50
    )

    show_calculations_button = ft.ElevatedButton(
        text="Вывести список расчётов",
        on_click=show_calculations,
        color=ft.Colors.BLACK,
        bgcolor=ft.Colors.GREEN_100,
        width=200,
        height=100
    )

    # Добавляем стек с кнопками и текстовыми метками на страницу
    page.add(
        ft.Column(
            [
                create_map_button,
                show_calculations_button,
                get_info_button,
                map_text,
                calculations_text
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
    )

ft.app(target=main)
