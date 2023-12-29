from typing import Optional

from server.gameplay.common.damageable import Damageable
from server.gameplay.common.explosive import Explosive
from server.gameplay.common.gameobject import GameObject
from server.infrastructure.bounds import Bounds
from server.infrastructure.direction import Direction
from server.infrastructure.event import Event
from server.infrastructure.vector2 import Vector2


class Player(Damageable, GameObject):
    def __init__(self,
                 name: str,
                 position: Optional[Vector2] = Vector2(0, 0),
                 vision_range: Optional[int] = 2,
                 health: Optional[int] = 100,
                 ):
        Damageable.__init__(self, health=health)
        GameObject.__init__(self, name=name, position=position)
        self.vision_range = vision_range
        self.stunned = False

        self.on_dropped = Event()

    def get_vision_range(self) -> int:
        return self.vision_range

    def stun(self):
        self.stunned = True

    def remove_stun(self):
        self.stunned = False

    def move(self, direction: Direction, bounds: Optional[Bounds] = None) -> bool:
        if self.stunned:
            return False
        return GameObject.move(self, direction, bounds)

    def drop(self, explosive: Explosive) -> bool:
        if self.stunned:
            return False

        explosive.set_position(self.position)
        self.on_dropped.invoke(explosive)
        return True
