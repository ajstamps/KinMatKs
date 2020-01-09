import math


class Plane:
    def __init__(self, a, b, c, d):
        self.a = a
        self.b = b
        self.c = c
        self.d = d

    @staticmethod
    def plane_from_3_points(p1, p2, p3):
        a1 = p2.x - p1.x
        b1 = p2.y - p1.y
        c1 = p2.z - p1.z
        a2 = p3.x - p1.x
        b2 = p3.y - p1.y
        c2 = p3.z - p1.z
        a = b1 * c2 - b2 * c1
        b = a2 * c1 - a1 * c2
        c = a1 * b2 - b1 * a2
        d = (- a * p1.x - b * p1.y - c * p1.z)

        return Plane(a, b, c, d)

    def angle_between_planes(self, plane2):
        a = self.a * plane2.a
        b = self.b * plane2.b
        c = self.c * plane2.c

        numerator = abs(a + b + c)

        abc1 = math.pow(self.a, 2) + math.pow(self.b, 2) + math.pow(self.c, 2)
        abc2 = math.pow(plane2.a, 2) + math.pow(plane2.b, 2) + math.pow(plane2.c, 2)

        denominator = math.sqrt(abc1) * math.sqrt(abc2)

        return math.acos(numerator/denominator)
