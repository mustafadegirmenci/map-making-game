import json
import socket
import threading
import traceback

from server.application.authmanager import AuthManager
from server.application.gamemanager import GameManager
from server.infrastructure.direction import Direction
from server.infrastructure.vector2 import Vector2


class ServerManager:
    @classmethod
    def initialize(cls):
        server = cls()
        server.start()

    def __init__(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(('localhost', 5555))
        self.server_socket.listen(5)
        print("Server started.")

    def start(self):
        while True:
            client, addr = self.server_socket.accept()
            client_thread = threading.Thread(target=client_handler, args=(client, addr,))
            client_thread.start()


def client_handler(client_socket, address):
    auth_manager = AuthManager()

    print(f"{address} connected.")

    while True:
        request = client_socket.recv(1024).decode().split()

        if not request:
            break

        command = request[0]
        args = request[1:]
        cookie = request[-1]

        if command == "register":
            try:
                username, password = args
                success, message = auth_manager.register(username=username, password=password)
                response_data = {
                    "success": success,
                    "message": message
                }
                json_response = json.dumps(response_data)
                client_socket.send(json_response.encode())
            except Exception as ex:
                print(ex)
                traceback.print_exc()
                client_socket.send(json.dumps({"success": False, "message": "Error"}).encode())

        elif command == "login":
            try:
                username, password = args
                success, message, token = auth_manager.login(username=username, password=password)
                response_data = {
                    "success": success,
                    "message": message,
                    "token": token
                }
                json_response = json.dumps(response_data)
                client_socket.send(json_response.encode())
            except Exception as ex:
                print(ex)
                traceback.print_exc()
                client_socket.send(json.dumps({"success": False, "message": "Error"}).encode())

        elif command == "logout":
            message = AuthManager.logout(cookie)
            client_socket.send(json.dumps({"success": False, "message": message}).encode())

        elif command == "showmaps":
            if not AuthManager.is_authenticated(token=cookie):
                client_socket.send(json.dumps({"success": False, "message": "Unauthorized."}).encode())
                continue

            try:
                maps = GameManager.get_all_maps()
                response_data = {
                    "maps": [map_item.id for map_item in maps]
                }
                json_response = json.dumps(response_data)
                client_socket.send(json_response.encode())
            except Exception as ex:
                print(ex)
                traceback.print_exc()
                client_socket.send(json.dumps({"success": False, "message": "Error"}).encode())

        elif command == "mapinfo":
            if not AuthManager.is_authenticated(token=cookie):
                client_socket.send(json.dumps({"success": False, "message": "Unauthorized."}).encode())
                continue

            try:
                map_id = args[0]
                team_name = args[1]
                the_map = GameManager.get_map_by_id(map_id)
                the_team = the_map.teams[team_name]

                response_data = {
                    "width": the_map.width,
                    "height": the_map.height,
                    "visible-positions": [(vp.x, vp.y) for vp in the_team.visible_positions],
                    "players": [{"name": p.name, "x": p.position.x, "y": p.position.y, "health": p.health}
                                for p in the_map.players.values()
                                if Vector2(p.position.x, p.position.y) in the_team.visible_positions
                                ],
                    "explosives": [{"name": e.name, "x": e.position.x, "y": e.position.y}
                                   for e in the_map.explosives.values()
                                   if Vector2(e.position.x, e.position.y) in the_team.visible_positions
                                   ],
                }
                json_response = json.dumps(response_data)
                client_socket.send(json_response.encode())
            except Exception as ex:
                print(ex)
                traceback.print_exc()
                client_socket.send(json.dumps({"success": False, "message": "Error"}).encode())

        elif command == "newmap":
            if not AuthManager.is_authenticated(token=cookie):
                client_socket.send(json.dumps({"success": False, "message": "Unauthorized."}).encode())
                continue

            try:
                width, height = args[0].split("x")
                GameManager.create_map(width, height)
                client_socket.send(json.dumps({"success": True, "message": "Map created."}).encode())
            except Exception as ex:
                print(ex)
                traceback.print_exc()
                client_socket.send(json.dumps({"success": False, "message": "Error"}).encode())

        elif command == "join":
            if not AuthManager.is_authenticated(token=cookie):
                client_socket.send(json.dumps({"success": False, "message": "Unauthorized."}).encode())
                continue

            try:
                map_id = args[0]
                team_name = args[1]
                username = AuthManager.get_username_from_token(token=cookie)
                success, message = GameManager.join_map(username=username, map_id=map_id, team_name=team_name)
                client_socket.send(json.dumps({"success": success, "message": message}).encode())

            except Exception as ex:
                print(ex)
                traceback.print_exc()
                client_socket.send(json.dumps({"success": False, "message": "Error"}).encode())

        elif command == "move":
            if not AuthManager.is_authenticated(token=cookie):
                client_socket.send(json.dumps({"success": False, "message": "Unauthorized."}).encode())
                continue

            try:
                direction_code = args[0]
                username = AuthManager.get_username_from_token(token=cookie)
                print(f'direction_code = {direction_code}')
                success = GameManager.player_move(username=username, direction=Direction.from_string(direction_code))
                if success:
                    client_socket.send(json.dumps({"success": True, "message": "Successfully moved."}).encode())
                else:
                    client_socket.send(json.dumps({"success": False, "message": "Drop failed."}).encode())
            except Exception as ex:
                print(ex)
                traceback.print_exc()
                client_socket.send(json.dumps({"success": False, "message": "Error"}).encode())

        elif command == "drop":
            if not AuthManager.is_authenticated(token=cookie):
                client_socket.send(json.dumps({"success": False, "message": "Unauthorized."}).encode())
                continue

            try:
                object_code = args[0]
                username = AuthManager.get_username_from_token(token=cookie)
                success = GameManager.player_drop(username=username, object_code=object_code)
                if success:
                    client_socket.send(json.dumps({"success": True, "message": "Successfully dropped."}).encode())
                else:
                    client_socket.send(json.dumps({"success": False, "message": "Drop failed."}).encode())
            except Exception as ex:
                print(ex)
                traceback.print_exc()
                client_socket.send(json.dumps({"success": False, "message": "Error"}).encode())

        else:
            client_socket.send("Invalid command.".encode())

    client_socket.close()
    print(f"Connection closed with {address}.")
