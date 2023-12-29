import threading
from abc import ABC, abstractmethod
from typing import Optional

from gameplay.common.gameobject import GameObject
from gameplay.player import Player
from infrastructure.event import Event
from infrastructure.vector2 import Vector2


class Explosive(GameObject, ABC):
    def __init__(self,
                 name: Optional[str] = 'Explosive',
                 position: Optional[Vector2] = Vector2(0, 0),
                 timer_duration: Optional[int] = 3,
                 explosion_range: Optional[int] = 2
                 ):
        GameObject.__init__(self, name=name, position=position)
        self.timer_duration = timer_duration
        self.explosion_range = explosion_range
        self.activated = False
        self.on_exploded = Event()

    def activate(self) -> bool:
        if self.activated:
            return False
        self.activated = True
        timer_thread = threading.Timer(self.timer_duration, lambda: self.on_exploded.invoke())
        timer_thread.start()
        return True

    @abstractmethod
    def apply_explosion_to_target(self, target: Player):
        pass
