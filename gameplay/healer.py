from typing import Optional

from gameplay.common.explosive import Explosive
from gameplay.player import Player
from infrastructure.vector2 import Vector2


class Healer(Explosive):
    def __init__(self,
                 position: Optional[Vector2] = Vector2(0, 0),
                 timer_duration: Optional[int] = 0,
                 explosion_range: Optional[int] = 2,
                 heal_amount: Optional[int] = 20
                 ):
        Explosive.__init__(self,
                           name='Bomb',
                           position=position,
                           timer_duration=timer_duration,
                           explosion_range=explosion_range
                           )
        self.heal_amount = heal_amount

    def apply_explosion_to_target(self, target: Player):
        target.heal(self.heal_amount)
