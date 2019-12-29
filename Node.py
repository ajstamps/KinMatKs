from OpenGLUtils import render_point


class Node:
    def __init__(self, x, y, z, radius, color):
        self.x = x
        self.y = y
        self.z = z
        self.radius = radius
        self.color = color

    def dist_between_node(self, node):
        return ((self.x - node.x) ** 2 +
                (self.y - node.y) ** 2 +
                (self.z - node.z) ** 2) ** 0.5

    def __add__(self, other):
        x = self.x + other.x
        y = self.y + other.y
        z = self.z + other.z

        return Node(x, y, z, self.radius, self.color)

    def __sub__(self, other):
        x = self.x - other.x
        y = self.y - other.y
        z = self.z - other.z

        return Node(x, y, z, self.radius, self.color)

    def __pow__(self, other):
        x = self.x * other.x
        y = self.y * other.y
        z = self.z * other.z

        return Node(x, y, z, self.radius, self.color)

    def __mul__(self, other):
        x = self.y * other.z - self.z * other.y
        y = self.z * other.x - self.x * other.z
        z = self.x * other.y - self.y * other.x

        return Node(x, y, z, self.radius, self.color)

    def magnitude(self):
        return (self.x ** 2 + self.y ** 2 + self.z ** 2) ** 0.5

    def dist_between_axis(self, node1, node2):
        ab = node2 - node1
        ac = self - node1
        area = (ab * ac).magnitude()
        cd = area / ab.magnitude()
        return cd

    def display(self):
        render_point(self, self.color, self.radius, 20)
