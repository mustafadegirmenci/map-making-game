from typing import Dict

from gameplay.common.explosive import Explosive
from gameplay.player import Player
from infrastructure.event import Event


class Map:
    def __init__(self):
        self.players: Dict[str, Player] = {}
        self.explosives: Dict[str, Explosive] = {}

        self.on_player_joined = Event()
        self.on_player_left = Event()
        self.on_explosive_added = Event()

    def add_player(self, player: Player) -> bool:

        def handle_player_movement(moved_player: Player):
            for explosive in self.explosives.values():
                if explosive.position == moved_player.get_position():
                    explosive.activate()

        def handle_player_drop(dropped_explosive: Explosive):
            self.add_explosive(dropped_explosive)

        unique_id = player.get_unique_id()
        if unique_id in self.players:
            print(f"Player with id '{unique_id}' already exists in the map.")
            return False
        self.players[unique_id] = player
        self.on_player_joined.invoke(player)

        player.on_moved.add_handler(lambda: handle_player_movement(player))
        player.on_dropped.add_handler(lambda dropped_explosive: handle_player_drop(dropped_explosive))
        player.on_died.add_handler(lambda: self.remove_player(player.get_unique_id()))
        return True

    def remove_player(self, unique_id: str) -> bool:
        if unique_id in self.players:
            left_player = self.players.pop(unique_id)
            self.on_player_left.invoke(left_player)
            return True
        else:
            print(f"No player with id '{unique_id}' found in the map.")
            return False

    def add_explosive(self, explosive: Explosive) -> bool:

        def handle_explosion(exploded_explosive: Explosive):
            for player in self.players.values():
                exploded_explosive.apply_explosion_to_target(player)

        unique_id = explosive.get_unique_id()
        if unique_id in self.explosives:
            print(f"Explosive with id '{unique_id}' already exists in the map.")
            return False
        self.explosives[unique_id] = explosive
        self.on_explosive_added.invoke(explosive)
        explosive.on_exploded.add_handler(lambda: handle_explosion(explosive))
        return True
