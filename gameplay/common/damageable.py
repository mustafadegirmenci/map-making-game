from abc import ABC

from infrastructure.event import Event


class Damageable(ABC):
    def __init__(self, health: int = 100):
        self.health = health

        self.on_healed = Event()
        self.on_damaged = Event()
        self.on_died = Event()

    def take_damage(self, damage: int):
        self.health -= damage
        self.on_damaged.invoke(self.health)
        if self.health <= 0:
            self.health = 0
            self.on_died.invoke()

    def heal(self, amount: int):
        self.health += amount
