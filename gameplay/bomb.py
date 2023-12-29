from typing import Optional

from gameplay.common.explosive import Explosive
from gameplay.player import Player
from infrastructure.vector2 import Vector2


class Bomb(Explosive):
    def __init__(self,
                 position: Optional[Vector2] = Vector2(0, 0),
                 timer_duration: Optional[int] = 3,
                 explosion_range: Optional[int] = 2,
                 explosion_damage: Optional[int] = 10
                 ):
        Explosive.__init__(self,
                           name='Bomb',
                           position=position,
                           timer_duration=timer_duration,
                           explosion_range=explosion_range
                           )
        self.explosion_damage = explosion_damage

    def apply_explosion_to_target(self, target: Player):
        target.take_damage(self.explosion_damage)
