from typing import List, Dict

from gameplay.player import Player
from infrastructure.event import Event
from infrastructure.vector2 import Vector2


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
            player.on_position_changed.add_handler(self.extend_visible_positions)
            return True
        else:
            print(f"Player with id '{unique_id}' is already in the team.")
            return False

    def remove_player(self, unique_id: str) -> bool:
        if unique_id in self.players:
            removed_player = self.players.pop(unique_id)
            removed_player.on_position_changed.remove_handler(self.extend_visible_positions)
            self.on_player_removed.invoke(removed_player)
            return True
        else:
            print(f"Player with id '{unique_id}' is not in the team.")
            return False

    def get_players(self) -> List[Player]:
        return list(self.players.values())

    def extend_visible_positions(self, old_position: Vector2, new_position: Vector2):
        # Logic to extend visible positions based on player's line of sight
        # For example, adding the line_of_sight positions to the team's visible_positions set
        self.visible_positions.update(line_of_sight)

    def get_visible_positions(self) -> set[Vector2]:
        return self.visible_positions
