from typing import Dict

from server.gameplay.bomb import Bomb
from server.gameplay.freezer import Freezer
from server.gameplay.healer import Healer
from server.gameplay.map import Map
from server.gameplay.player import Player
from server.infrastructure.direction import Direction


class GameManager:
    maps: Dict[str, Map] = {}  # map_id : Map
    players: Dict[str, Player] = {}  # username : Player

    @staticmethod
    def get_map_by_id(map_id: str) -> Map | None:
        if map_id not in GameManager.maps:
            return None
        return GameManager.maps[map_id]

    @staticmethod
    def get_all_maps() -> list[Map]:
        return list(GameManager.maps.values())

    @staticmethod
    def create_map(width: int, height: int) -> Map:
        new_map = Map(width, height)
        GameManager.maps[new_map.id] = new_map
        return new_map

    @staticmethod
    def join_map(username, map_id, team_name) -> (bool, str):
        the_map = GameManager.get_map_by_id(map_id)
        if the_map is None:
            return False, f"No map with given id ({map_id})."

        the_player = Player(name=username)
        GameManager.players[username] = the_player

        if the_map.add_player(player=the_player, team_name=team_name):
            GameManager.players[username] = the_player
            return True, f"Player [{the_player.name}] joined map [{map_id}]."

        return False, "Failed to join map."

    @staticmethod
    def player_move(username: str, direction: Direction) -> bool:
        the_player = GameManager.players[username]

        if the_player is None:
            return False

        return the_player.move(direction=direction)

    @staticmethod
    def player_drop(username: str, object_code: str) -> bool:
        the_player = GameManager.players[username]

        if the_player is None:
            return False

        if object_code.upper() == 'B':
            return the_player.drop(Bomb())
        elif object_code.upper() == 'F':
            return the_player.drop(Freezer())
        elif object_code.upper() == 'H':
            return the_player.drop(Healer())
