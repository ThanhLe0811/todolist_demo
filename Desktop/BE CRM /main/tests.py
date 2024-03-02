from django.test import TestCase

# Create your tests here.
# tests.py
from channels.testing import WebsocketCommunicator
from django.test import TestCase
from main.routing import websocket_urlpatterns

class NotificationConsumerTests(TestCase):
    async def connect(self):
        communicator = WebsocketCommunicator(websocket_urlpatterns[0].application, "/ws/notifications/")
        connected, subprotocol = await communicator.connect()
        self.assertTrue(connected)

        return communicator

    async def disconnect(self, communicator):
        await communicator.disconnect()

    async def test_receive_notification(self):
        communicator = await self.connect()

        # Gửi thông điệp từ client
        message = {'message': 'Hello, world!'}
        await communicator.send_json_to(message)

        # Nhận thông điệp từ server
        response = await communicator.receive_json_from()

        # Kiểm tra xem thông điệp có đúng không
        self.assertEqual(response, message)

        # Ngắt kết nối
        await self.disconnect(communicator)
