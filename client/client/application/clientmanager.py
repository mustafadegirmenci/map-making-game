import json
import socket
from typing import Optional


class ClientManager:
    SERVER_ADDRESS: str = 'localhost'
    SERVER_PORT: int = 5555
    CLIENT_SOCKET = None

    @staticmethod
    def initialize():
        ClientManager.CLIENT_SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ClientManager.CLIENT_SOCKET.connect((ClientManager.SERVER_ADDRESS, ClientManager.SERVER_PORT))

    @staticmethod
    def send_command(command: str, args: Optional[list[str]] = [], token: Optional[str] = ''):
        message = f'{command} {" ".join(args)} {token}'
        ClientManager.CLIENT_SOCKET.sendall(message.encode())

    @staticmethod
    def receive_response():
        json_string = ClientManager.CLIENT_SOCKET.recv(1024).decode()
        response_dict = json.loads(json_string)
        return response_dict
