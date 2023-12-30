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
        unique_id = player.unique_id
        if unique_id not in self.players:
            self.players[unique_id] = player
            self.on_player_added.invoke(player)
            self.extend_visible_positions(player)
            player.on_moved.add_handler(
                lambda: self.extend_visible_positions(player))
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

    def extend_visible_positions(self, player: Player):
        def reveal(x, y):
            if player.current_map is not None:
                map_bounds = Bounds(
                    min_x=0,
                    max_x=int(player.current_map.width),
                    min_y=0,
                    max_y=int(player.current_map.height))
                if map_bounds.is_within_bounds(x, y):
                    self.visible_positions.add(Vector2(x, y))
            else:
                self.visible_positions.add(Vector2(x, y))

        revealed = Bounds(
            min_x=player.position.x - player.vision_range,
            max_x=player.position.x + player.vision_range,
            min_y=player.position.y - player.vision_range,
            max_y=player.position.y + player.vision_range)

        revealed.iterate_through_points(reveal)

    def get_visible_positions(self) -> set[Vector2]:
        return self.visible_positions
