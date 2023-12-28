from typing import Optional

from infrastructure.bounds import Bounds
from infrastructure.direction import Direction
from infrastructure.gameobject import GameObject
from infrastructure.vector2 import Vector2


class Player(GameObject):
    def __init__(self, name: str, line_of_sight: int, position: Optional['Vector2'] = None):
        super().__init__(name=name, position=position)
        self.line_of_sight = line_of_sight

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

    def get_line_of_sight(self) -> int:
        return self.line_of_sight
