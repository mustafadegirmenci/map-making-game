import uuid
from typing import Optional

from infrastructure.event import Event
from infrastructure.vector2 import Vector2


class GameObject:
    def __init__(self,
                 position: Optional[Vector2] = None,
                 name: Optional[str] = None):

        self.unique_id: str = str(uuid.uuid4())
        self.position: Vector2 = position if position is not None else Vector2(0.0, 0.0)
        self.name: str = name if name is not None else "New GameObject"

        self.on_position_changed = Event()

    def get_unique_id(self) -> str:
        return self.unique_id

    def set_position(self, new_position: Vector2):
        old_position = self.position
        self.position = new_position

        if old_position != new_position:
            self.on_position_changed.invoke(old_position, new_position)

    def get_position(self) -> Vector2:
        return self.position

    def set_name(self, new_name: str):
        self.name = new_name

    def get_name(self) -> str:
        return self.name
