from enum import Enum


class Direction(Enum):
    NORTH = 'NORTH'
    SOUTH = 'SOUTH'
    EAST = 'EAST'
    WEST = 'WEST'
    NORTHEAST = 'NORTHEAST'
    NORTHWEST = 'NORTHWEST'
    SOUTHEAST = 'SOUTHEAST'
    SOUTHWEST = 'SOUTHWEST'

    @classmethod
    def from_string(cls, direction_str: str) -> 'Direction':
        str_to_dir = {
            'NORTH': Direction.NORTH,
            'SOUTH': Direction.SOUTH,
            'EAST': Direction.EAST,
            'WEST': Direction.WEST,
            'NORTHEAST': Direction.NORTHEAST,
            'NORTHWEST': Direction.NORTHWEST,
            'SOUTHEAST': Direction.SOUTHEAST,
            'SOUTHWEST': Direction.SOUTHWEST
        }
        return str_to_dir.get(direction_str.upper(), None)

    def __eq__(self, other):
        if isinstance(other, str):
            return self.value == other.upper()
        return super().__eq__(other)
