import math


class Vector2:
    def __init__(self, x: float, y: float):
        self.x: float = x
        self.y: float = y

    def __add__(self, other: 'Vector2') -> 'Vector2':
        return Vector2(self.x + other.x, self.y + other.y)

    def __sub__(self, other: 'Vector2') -> 'Vector2':
        return Vector2(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar: float) -> 'Vector2':
        return Vector2(self.x * scalar, self.y * scalar)

    def __truediv__(self, scalar: float) -> 'Vector2':
        return Vector2(self.x / scalar, self.y / scalar)

    def __str__(self) -> str:
        return f"({self.x}, {self.y})"

    def __eq__(self, other: 'Vector2') -> bool:
        return self.x == other.x and self.y == other.y

    def __ne__(self, other: 'Vector2') -> bool:
        return not self.__eq__(other)

    def __lt__(self, other: 'Vector2') -> bool:
        return self.magnitude() < other.magnitude()

    def __gt__(self, other: 'Vector2') -> bool:
        return self.magnitude() > other.magnitude()

    def __le__(self, other: 'Vector2') -> bool:
        return self.magnitude() <= other.magnitude()

    def __ge__(self, other: 'Vector2') -> bool:
        return self.magnitude() >= other.magnitude()

    def __hash__(self):
        return hash((self.x, self.y))

    def magnitude(self) -> float:
        return math.sqrt(self.x ** 2 + self.y ** 2)

    def normalize(self) -> 'Vector2':
        mag = self.magnitude()
        if mag != 0:
            return Vector2(self.x / mag, self.y / mag)
        else:
            return Vector2(0, 0)

    def dot(self, other: 'Vector2') -> float:
        return self.x * other.x + self.y * other.y
