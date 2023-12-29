import uuid
from abc import ABC
from typing import Optional

from infrastructure.bounds import Bounds
from infrastructure.direction import Direction
from infrastructure.event import Event
from infrastructure.vector2 import Vector2


class GameObject(ABC):
    def __init__(self,
                 name: Optional[str] = "New GameObject",
                 position: Optional[Vector2] = Vector2(0, 0)
                 ):

        self.unique_id: str = str(uuid.uuid4())
        self.name: str = name
        self.position: Vector2 = position

        self.on_moved = Event()

    def set_position(self, new_position: Vector2):
        old_position = self.position
        self.position = new_position

        if old_position != new_position:
            self.on_moved.invoke()

    def get_position(self) -> Vector2:
        return self.position

    def move(self, direction: Direction, bounds: Optional[Bounds] = None) -> bool:
        new_x, new_y = self.position.x, self.position.y

        if direction == Direction.NORTH:
            new_y += 1
        elif direction == Direction.SOUTH:
            new_y -= 1
        elif direction == Direction.EAST:
            new_x += 1
        elif direction == Direction.WEST:
            new_x -= 1
        elif direction == Direction.NORTHEAST:
            new_x += 1
            new_y += 1
        elif direction == Direction.NORTHWEST:
            new_x -= 1
            new_y += 1
        elif direction == Direction.SOUTHEAST:
            new_x += 1
            new_y -= 1
        elif direction == Direction.SOUTHWEST:
            new_x -= 1
            new_y -= 1

        if bounds and not bounds.is_within_bounds(new_x, new_y):
            print("Cannot move. New position is outside the bounds.")
            return False

        self.set_position(Vector2(new_x, new_y))
        return True

    def get_unique_id(self) -> str:
        return self.unique_id

    def set_name(self, new_name: str):
        self.name = new_name

    def get_name(self) -> str:
        return self.name
