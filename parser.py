import requests
import time
from threading import Thread, Event
from textual.app import App, ComposeResult
from textual.containers import ScrollableContainer
from textual.widgets import Button, Header, Footer, Static


class DataMonitor(App):
    """Textual приложение для мониторинга API"""

    CSS = """
    Screen {
        layout: vertical;
    }
    #output {
        height: 1fr;
        border: solid $accent;
        padding: 1;
        overflow-y: auto;
    }
    """

    BINDINGS = [("q", "quit", "Quit")]

    def __init__(self):
        super().__init__()
        self.stop_event = Event()
        self.worker_thread = None
        self.seen_usernames = set()

    def compose(self) -> ComposeResult:
        yield Header()
        yield ScrollableContainer(Static(id="output"))
        yield Button("Start", id="start", variant="success")
        yield Button("Stop", id="stop", variant="error", disabled=True)
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "start":
            self.start_monitoring()
        elif event.button.id == "stop":
            self.stop_monitoring()

    def start_monitoring(self):
        """Запуск мониторинга"""
        self.query_one("#start").disabled = True
        self.query_one("#stop").disabled = False
        self.stop_event.clear()
        self.worker_thread = Thread(target=self.monitor_loop, daemon=True)
        self.worker_thread.start()
        self.log_message("Мониторинг запущен...")

    def stop_monitoring(self):
        """Остановка мониторинга"""
        self.stop_event.set()
        if self.worker_thread:
            self.worker_thread.join(timeout=1)
        self.query_one("#start").disabled = False
        self.query_one("#stop").disabled = True
        self.log_message("Мониторинг остановлен")

    def monitor_loop(self):
        """Цикл мониторинга в отдельном потоке"""
        while not self.stop_event.is_set():
            try:
                response = requests.get("https://api.aresmine.ru/orders/last/5", timeout=10)
                response.raise_for_status()
                self.process_data(response.json())
            except Exception as e:
                self.log_message(f"Ошибка: {str(e)}")
            time.sleep(30)

    def process_data(self, data):
        """Обработка полученных данных"""
        new_entries = False
        output = []

        for order in data:
            username = order.get("userName", "N/A")
            if username not in self.seen_usernames:
                self.seen_usernames.add(username)
                output.extend([
                    f"Username: {username}",
                    f"Product: {order.get('productName', 'N/A')}",
                    f"Paid: {order.get('paid', 'N/A')}",
                    "―" * 20
                ])
                new_entries = True

        if new_entries:
            self.log_message("\n".join(output))
            self.save_to_file("\n".join(output) + "\n")
        else:
            self.log_message("Новых записей не обнаружено")

    def save_to_file(self, data):
        """Сохранение данных в файл"""
        with open("output.txt", "a", encoding="utf-8") as f:
            f.write(data)

    def log_message(self, message):
        """Вывод сообщения в интерфейс"""
        output = self.query_one("#output")
        output.update(output.renderable + "\n" + message)
        output.scroll_end()


if __name__ == "__main__":
    app = DataMonitor()
    app.run()
