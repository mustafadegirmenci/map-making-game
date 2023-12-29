from typing import List, Dict

from server.gameplay.player import Player
from server.infrastructure.bounds import Bounds
from server.infrastructure.event import Event
from server.infrastructure.vector2 import Vector2


class Team:
    def __init__(self, name: str):
        self.name = name
        self.players: Dict[str, Player] = {}
        self.visible_positions: set[Vector2] = set()

        self.on_player_added = Event()
        self.on_player_removed = Event()

    def add_player(self, player: Player) -> bool:
        unique_id = player.get_unique_id()
        if unique_id not in self.players:
            self.players[unique_id] = player
            self.on_player_added.invoke(player)
            self.extend_visible_positions(player.get_position(), player.get_vision_range())
            player.on_moved.add_handler(
                lambda: self.extend_visible_positions(player.get_position(), player.get_vision_range()))
            return True
        else:
            print(f"Player with id '{unique_id}' is already in the team.")
            return False

    def remove_player(self, unique_id: str) -> bool:
        if unique_id in self.players:
            removed_player = self.players.pop(unique_id)
            removed_player.on_moved.remove_handler(self.extend_visible_positions)
            self.on_player_removed.invoke(removed_player)
            return True
        else:
            print(f"Player with id '{unique_id}' is not in the team.")
            return False

    def get_players(self) -> List[Player]:
        return list(self.players.values())

    def extend_visible_positions(self, new_position: Vector2, line_of_sight: int):
        revealed = Bounds(
            min_x=new_position.x - line_of_sight,
            max_x=new_position.x + line_of_sight,
            min_y=new_position.y - line_of_sight,
            max_y=new_position.y + line_of_sight)

        revealed.iterate_through_points(lambda x, y: self.visible_positions.add(Vector2(x, y)))

    def get_visible_positions(self) -> set[Vector2]:
        return self.visible_positions
