from enum import Enum


class Direction(Enum):
    NORTH = 'N'
    SOUTH = 'S'
    EAST = 'E'
    WEST = 'W'
    NORTHEAST = 'NE'
    NORTHWEST = 'NW'
    SOUTHEAST = 'SE'
    SOUTHWEST = 'SW'

    @classmethod
    def from_string(cls, direction_str: str) -> 'Direction':
        str_to_dir = {
            'N': Direction.NORTH,
            'S': Direction.SOUTH,
            'E': Direction.EAST,
            'W': Direction.WEST,
            'NE': Direction.NORTHEAST,
            'NW': Direction.NORTHWEST,
            'SE': Direction.SOUTHEAST,
            'SW': Direction.SOUTHWEST
        }
        return str_to_dir.get(direction_str.upper(), None)

    def __eq__(self, other):
        if isinstance(other, str):
            return self.value == other.upper()
        return super().__eq__(other)
