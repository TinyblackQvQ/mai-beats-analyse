import math


def angle2arc(angle: float):
    return angle * math.pi / 180


def arc2angle(arc: float):
    return arc / math.pi * 180


class Vector:
    x: float = 0
    y: float = 0

    def __init__(self, x: float = 0, y: float = 0):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        delta_arc = self.arc() - other.arc()
        return self.len() * other.len() * math.cos(delta_arc)

    def len(self):
        return math.sqrt(self.x ** 2 + self.y ** 2)

    def arc(self):
        if self.x == 0:
            return math.pi / 2 if self.y > 0 else 3 * math.pi / 2
        if self.y == 0:
            return math.pi if self.x < 0 else 0
        return (1 if self.y >= 0 else -1) * math.atan(self.y / self.x)

    def angle(self):
        return self.arc() * 180 / math.pi

    def toTuple(self):
        return (self.x, self.y)

    def __str__(self):
        return str((self.x, self.y))
