from typing import Dict, Optional, List
from infrastructure.gameobject import GameObject, Event
from infrastructure.vector2 import Vector2


class Map:
    def __init__(self):
        self.game_objects: Dict[str, GameObject] = {}
        self.on_object_added = Event()
        self.on_object_removed = Event()

    def add_object(self, game_obj: GameObject, position: Optional['Vector2'] = None) -> bool:
        unique_id = game_obj.get_unique_id()
        if unique_id not in self.game_objects:
            if position:
                game_obj.set_position(position)
            self.game_objects[unique_id] = game_obj
            self.on_object_added.invoke(game_obj)
            return True
        else:
            print(f"Object with id '{unique_id}' already exists in the map.")
            return False

    def remove_object(self, unique_id: str) -> bool:
        if unique_id in self.game_objects:
            removed_obj = self.game_objects.pop(unique_id)
            self.on_object_removed.invoke(removed_obj)
            return True
        else:
            print(f"No object with id '{unique_id}' found in the map.")
            return False

    def get_object_by_id(self, unique_id: str) -> Optional[GameObject]:
        return self.game_objects.get(unique_id, None)

    def get_objects_at_position(self, position: Vector2) -> List[GameObject]:
        objects_at_position = []
        for obj in self.game_objects.values():
            if obj.position == position:
                objects_at_position.append(obj)
        return objects_at_position

    def get_all_objects(self) -> List[GameObject]:
        return list(self.game_objects.values())
