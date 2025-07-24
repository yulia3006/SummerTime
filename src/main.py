import flet as ft
import serial
from io import BytesIO
import base64
import matplotlib.pyplot as plt
import numpy as np
import math
import threading
import time


class LidarApp:
    def __init__(self, page: ft.Page):
        self.page = page
        self.serial_conn = None
        self.scanning = False
        self.angles = []
        self.distances = []
        self.setup_ui()

    def setup_ui(self):
        self.status_text = ft.Text("Готов к работе. Порт: COM4", color="green")
        self.progress_bar = ft.ProgressBar(visible=False)

        self.plot_image = ft.Image(
            src_base64="iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAFhQHQwUJm7AAAAABJRU5ErkJggg==",
            width=800,
            height=600,
            fit=ft.ImageFit.CONTAIN
        )

        self.btn_start = ft.ElevatedButton(
            "Начать сканирование",
            on_click=self.start_scan,
            icon=ft.Icons.PLAY_ARROW
        )

        self.btn_stop = ft.ElevatedButton(
            "Остановить",
            on_click=self.stop_scan,
            icon=ft.Icons.STOP,
            disabled=True
        )

        self.page.add(
            ft.Column([
                ft.Row([self.btn_start, self.btn_stop]),
                self.progress_bar,
                self.status_text,
                ft.Container(
                    content=self.plot_image,
                    alignment=ft.alignment.center,
                    padding=10,
                    expand=True
                )
            ], expand=True)
        )
        self.page.update()

    def update_buttons_state(self):
        self.btn_start.disabled = self.scanning
        self.btn_stop.disabled = not self.scanning
        self.progress_bar.visible = self.scanning
        self.page.update()

    def start_scan(self, e):
        if not self.scanning:
            self.scanning = True
            self.angles = []
            self.distances = []
            self.status_text.value = "Сканирование... Порт: COM4"
            self.status_text.color = "blue"
            self.update_buttons_state()

            # Отправка команды RESET перед START для сброса состояния Arduino
            if self.serial_conn and self.serial_conn.is_open:
                self.serial_conn.write(b'RESET\n')
                self.serial_conn.flush()

            threading.Thread(target=self.read_serial_data, daemon=True).start()

    def stop_scan(self, e):
        self.scanning = False
        if self.serial_conn and self.serial_conn.is_open:
            try:
                self.serial_conn.write(b'STOP\n')
                self.serial_conn.flush()
            except Exception as e:
                print(f"Ошибка при отправке STOP: {e}")

        self.status_text.value = "Сканирование остановлено. Порт: COM4"
        self.status_text.color = "orange"
        self.update_buttons_state()

    def read_serial_data(self):
        try:
            self.serial_conn = serial.Serial('COM4', baudrate=9600, timeout=2)

            # Сначала сбрасываем состояние
            self.serial_conn.write(b'RESET\n')
            self.serial_conn.flush()
            time.sleep(0.1)

            # Затем отправляем команду START
            self.serial_conn.write(b'START\n')
            self.serial_conn.flush()

            while self.scanning and self.serial_conn.is_open:
                if self.serial_conn.in_waiting > 0:
                    # Читаем две строки подряд
                    line1 = self.serial_conn.readline().decode('utf-8').strip()
                    line2 = self.serial_conn.readline().decode('utf-8').strip()

                    if line1 and line2:
                        try:
                            # Первая строка (0-180 градусов)
                            angle1, distance1 = map(int, line1.split(','))
                            self.angles.append(angle1)
                            self.distances.append(distance1)

                            # Вторая строка (181-360 градусов)
                            angle2, distance2 = map(int, line2.split(','))
                            self.angles.append(angle2)
                            self.distances.append(distance2)

                            # Обновляем график каждые 6 точек
                            if len(self.angles) % 6 == 0:
                                self.update_plot()

                        except ValueError:
                            continue

            self.serial_conn.close()

        except Exception as e:
            self.status_text.value = f"Ошибка: {str(e)} (Порт: COM4)"
            self.status_text.color = "red"
            self.page.update()

    def update_plot(self):
        if len(self.angles) < 2:  # Нужно минимум 2 точки для соединения
            return

        plt.figure(figsize=(8, 6))

        try:
            # Сортируем точки по углу для правильного соединения
            sorted_indices = np.argsort(self.angles)
            sorted_angles = np.array(self.angles)[sorted_indices]
            sorted_distances = np.array(self.distances)[sorted_indices]

            # Конвертируем в декартовы координаты
            x = sorted_distances * np.cos(np.radians(sorted_angles))
            y = sorted_distances * np.sin(np.radians(sorted_angles))

            # Рисуем соединенные точки
            plt.plot(x, y, 'b-', alpha=0.3)  # Синяя линия соединения
            plt.scatter(x, y, c=sorted_angles, cmap='hsv', alpha=0.8, s=30)  # Цветные точки

            # Добавляем первую точку в конец для замыкания круга
            if len(x) > 2:
                plt.plot([x[-1], x[0]], [y[-1], y[0]], 'b-', alpha=0.3)

            plt.colorbar(label='Угол')
            plt.xlabel("X (см)")
            plt.ylabel("Y (см)")
            plt.title("Лазерное сканирование (окружность)")
            plt.grid(True)
            plt.axis('equal')

            # Сохраняем в буфер
            buf = BytesIO()
            plt.savefig(buf, format='png', dpi=100, bbox_inches='tight')
            buf.seek(0)

            # Обновляем изображение
            self.plot_image.src_base64 = base64.b64encode(buf.read()).decode('utf-8')
            self.status_text.value = f"Получено {len(self.angles)} точек (Порт: COM4)"

        except Exception as e:
            self.status_text.value = f"Ошибка построения графика: {str(e)}"
            self.status_text.color = "red"
        finally:
            plt.close()
            if 'buf' in locals():
                buf.close()
            self.page.update()


def main(page: ft.Page):
    page.title = "LIDAR Scanner (COM4)"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window_width = 1000
    page.window_height = 800
    page.padding = 10
    LidarApp(page)


ft.app(target=main)