class Bounds:
    def __init__(self, min_x: float, max_x: float, min_y: float, max_y: float):
        self.min_x = min_x
        self.max_x = max_x
        self.min_y = min_y
        self.max_y = max_y

    def is_within_bounds(self, x: float, y: float) -> bool:
        return self.min_x <= x <= self.max_x and self.min_y <= y <= self.max_y
