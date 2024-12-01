import flet as ft
from kafka import KafkaProducer, KafkaConsumer
import json
import random
import threading
import uuid


class TransactionApp(ft.UserControl):
    def __init__(self, kafka_server):
        super().__init__()
        self.kafka_server = kafka_server
        self.producer = KafkaProducer(bootstrap_servers=[kafka_server])
        self.user_id = str(random.randint(1, 9999))
        self.order_id = str(uuid.uuid4())[:8]

        self.consumer = KafkaConsumer(
            'transaction_complete',
            bootstrap_servers=[self.kafka_server],
            auto_offset_reset='earliest',
            group_id="transaction_complete_listener"
        )
        threading.Thread(target=self.wait_for_confirmation, daemon=True).start()

        self.status = ft.Text("")
        self.currency = ft.Dropdown(
            label="Валюта",
            label_style=ft.TextStyle(color=ft.colors.BLACK),
            options=[
                ft.dropdown.Option("USDT", text_style=ft.TextStyle(color=ft.colors.BLACK)),
                ft.dropdown.Option("RUB", text_style=ft.TextStyle(color=ft.colors.BLACK))
            ],
            value="USDT",
            focused_border_color=ft.colors.BLACK,
            focused_color=ft.colors.BLACK,
            bgcolor="white"
        )
        self.amount = ft.TextField(label="Сумма пополнения на пиво", width=750, label_style=ft.TextStyle(color=ft.colors.BLACK),
                                   focused_border_color=ft.colors.BLACK, cursor_color=ft.colors.BLACK,
                                   color=ft.colors.BLACK)
        self.pay_button = ft.ElevatedButton("Оплатить", bgcolor=ft.colors.WHITE, color=ft.colors.RED,
                                            on_click=self.send_transaction, width=750, height=80,
                                            style=ft.ButtonStyle(overlay_color=ft.colors.WHITE, shape=ft.RoundedRectangleBorder(radius=10),
                                                                 color={ft.ControlState.FOCUSED: ft.colors.WHITE,
                                                                        ft.ControlState.HOVERED: ft.colors.RED,
                                                                        ft.ControlState.DEFAULT: ft.colors.RED}))

        self.container = ft.Column(
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=40,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                self.amount,
                self.currency,
                self.pay_button
            ]
        )

    def send_transaction(self, e):
        if not self.amount.value:
            self.status.value = "Введите сумму пополнения"
            self.update()
            return

        transaction_data = {
            "user_id": self.user_id,
            "order_id": self.order_id,
            "amount": float(self.amount.value),
            "currency": self.currency.value
        }
        try:
            future = self.producer.send('transaction_validation', json.dumps(transaction_data).encode('utf-8'))
            future.get(timeout=10)
            self.status.value = f"Order {self.order_id}"
            self.container.controls = [ft.Text("Ожидание подтверждения...", color=ft.colors.BLACK,
                                               weight=ft.FontWeight.BOLD)]
        except Exception as ex:
            self.status.value = f"Ошибка: {ex}"
        self.update()

    def wait_for_confirmation(self):
        for message in self.consumer:
            transaction_data = json.loads(message.value.decode('utf-8'))
            if transaction_data['user_id'] == self.user_id and transaction_data['order_id'] == self.order_id:
                self.container.controls = [
                    ft.Icon(name=ft.icons.CHECK_CIRCLE, color="green", size=50),
                    ft.Text("Оплата прошла успешно!", color="green", size=20, weight=ft.FontWeight.BOLD)
                ]
                self.update()
                break

    def build(self):
        return ft.Container(
            content=ft.Column(
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Text("PayEasy", size=24, weight=ft.FontWeight.BOLD, color=ft.colors.BLACK),
                    self.container,
                    self.status
                ]
            ),
            alignment=ft.alignment.center,
            width=400,
            height=400,
            border_radius=ft.border_radius.all(10),
            padding=20,
            bgcolor=ft.colors.WHITE,
            shadow=ft.BoxShadow(blur_radius=15, color=ft.colors.BLACK, spread_radius=1, offset=ft.Offset(0, 0),
                                blur_style=ft.ShadowBlurStyle.OUTER)
        )


def main(page):
    page.title = "Сервис Транзакций - BudPay"
    page.horizontal_alignment = "center"
    page.vertical_alignment = "center"
    page.bgcolor = "#A5A5A5"
    with open("kafka_config.txt", "r") as f:
        kafka_server = f.read().strip()
    page.add(TransactionApp(kafka_server))


if __name__ == "__main__":
    ft.app(target=main)
