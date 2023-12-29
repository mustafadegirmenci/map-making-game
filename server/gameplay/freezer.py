import threading
from typing import Optional

from server.gameplay.common.explosive import Explosive
from server.gameplay.player import Player
from server.infrastructure.vector2 import Vector2


class Freezer(Explosive):
    def __init__(self,
                 position: Optional[Vector2] = Vector2(0, 0),
                 timer_duration: Optional[int] = 3,
                 explosion_range: Optional[int] = 2,
                 stun_duration: Optional[int] = 2
                 ):
        Explosive.__init__(self,
                           name='Freezer',
                           position=position,
                           timer_duration=timer_duration,
                           explosion_range=explosion_range
                           )
        self.stun_duration = stun_duration

    def apply_explosion_to_target(self, target: Player):
        target.stun()
        timer_thread = threading.Timer(self.stun_duration, target.remove_stun)
        timer_thread.start()
