import uuid
from typing import Dict

from server.gameplay.common.explosive import Explosive
from server.gameplay.player import Player
from server.gameplay.team import Team
from server.infrastructure.event import Event


class Map:
    def __init__(self, width, height):
        self.id: str = str(uuid.uuid4())
        self.width: int = width
        self.height: int = height

        self.teams: Dict[str, Team] = {}
        self.players: Dict[str, Player] = {}
        self.explosives: Dict[str, Explosive] = {}

        self.on_player_joined = Event()
        self.on_player_left = Event()
        self.on_explosive_added = Event()

    def add_player(self, player: Player, team_name: str) -> bool:

        def handle_player_movement(moved_player: Player):
            for explosive in self.explosives.values():
                if explosive.position == moved_player.get_position():
                    explosive.activate()

        def handle_player_drop(dropped_explosive: Explosive):
            self.add_explosive(dropped_explosive)

        unique_id = player.unique_id
        if unique_id in self.players:
            print(f"Player with id '{unique_id}' already exists in the map.")
            return False

        if team_name not in self.teams:
            self.teams[team_name] = Team(name=team_name)

        self.teams[team_name].add_player(player)
        self.players[unique_id] = player
        self.on_player_joined.invoke(player)

        player.current_map = self

        player.on_moved.add_handler(lambda: handle_player_movement(player))
        player.on_dropped.add_handler(lambda dropped_explosive: handle_player_drop(dropped_explosive))
        player.on_died.add_handler(lambda: self.remove_player(player.unique_id))
        return True

    def remove_player(self, unique_id: str) -> bool:
        if unique_id not in self.players:
            print(f"No player with id '{unique_id}' found in the map.")
            return False

        for team in self.teams.values():
            if unique_id in team.players.keys():
                team.remove_player(unique_id)

        left_player = self.players.pop(unique_id)
        left_player.current_map = None

        self.on_player_left.invoke(left_player)
        return True

    def add_explosive(self, explosive: Explosive) -> bool:

        def handle_explosion(exploded_explosive: Explosive):
            for player in self.players.values():
                exploded_explosive.apply_explosion_to_target(player)

        unique_id = explosive.unique_id
        if unique_id in self.explosives:
            print(f"Explosive with id '{unique_id}' already exists in the map.")
            return False
        self.explosives[unique_id] = explosive
        self.on_explosive_added.invoke(explosive)
        explosive.on_exploded.add_handler(lambda: handle_explosion(explosive))
        return True
