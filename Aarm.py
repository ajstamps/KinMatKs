import math

from Edge import Edge
from Wireframe import Wireframe


class Aarm(Wireframe):
    def __init__(self, inboard_rear_node, inboard_front_node, outboard_node, color):
        super().__init__()
        self.inboard_rear_node = inboard_rear_node
        self.inboard_front_node = inboard_front_node
        self.outboard_node = outboard_node
        self.outboard_node_store_x = outboard_node.x
        self.outboard_node_store_y = outboard_node.y
        self.outboard_node_store_z = outboard_node.z
        self.inboard_rear_node_store = inboard_rear_node.y
        self.inboard_front_node_store = inboard_front_node.y
        self.a_arm_color = color
        self.rotation_length = self.outboard_node.dist_between_axis(self.inboard_rear_node, self.inboard_front_node)
        if self.outboard_node_store_x < 0:
            self.rotation_length *= -1
        self.rear_arm = Edge(self.inboard_rear_node, self.outboard_node, 10, self.a_arm_color)
        self.front_arm = Edge(self.inboard_front_node, self.outboard_node, 10, self.a_arm_color)

        self.node_list = [self.inboard_rear_node, self.inboard_front_node, self.outboard_node]
        self.edge_list = [self.rear_arm, self.front_arm]

        self.add_nodes(self.node_list)

        self.add_edges(self.edge_list)

    def bump(self, bump_height):
        bump_angle = math.asin(bump_height / self.rotation_length)
        self.rotate_node_formula(bump_angle)

    def squat(self, squat_height):
        squat_dist_x = math.sqrt(math.pow(self.rotation_length, 2) - math.pow(squat_height, 2))

        if self.outboard_node.x < 0:
            squat_dist_x *= -1

        self.outboard_node.x = (squat_dist_x + self.rotation_length)

        self.inboard_rear_node.y = (self.inboard_rear_node_store + squat_height)
        self.inboard_front_node.y = (self.inboard_front_node_store + squat_height)

    def rotate_node_formula(self, theta):
        direction_vector = self.inboard_front_node - self.inboard_rear_node

        length = direction_vector.magnitude()

        a = self.inboard_rear_node.x
        b = self.inboard_rear_node.y
        c = self.inboard_rear_node.z

        u = float(direction_vector.x) / length
        v = float(direction_vector.y) / length
        w = float(direction_vector.z) / length

        x = self.outboard_node_store_x
        y = self.outboard_node_store_y
        z = self.outboard_node_store_z

        u2 = u * u
        v2 = v * v
        w2 = w * w

        cos_t = math.cos(theta)

        one_minus_cos_t = 1 - cos_t

        sin_t = math.sin(theta)

        self.outboard_node.x = (a * (v2 + w2) - u * (
                b * v + c * w - u * x - v * y - w * z)) * one_minus_cos_t + x * cos_t + (
                                       -c * v + b * w - w * y + v * z) * sin_t

        self.outboard_node.y = (b * (u2 + w2) - v * (
                a * u + c * w - u * x - v * y - w * z)) * one_minus_cos_t + y * cos_t + (
                                       c * u - a * w + w * x - u * z) * sin_t

        self.outboard_node.z = (c * (u2 + v2) - w * (
                a * u + b * v - u * x - v * y - w * z)) * one_minus_cos_t + z * cos_t + (
                                       -b * u + a * v - v * x + u * y) * sin_t

    def display(self):
        for edge in self.edges:
            edge.display()

        for node in self.nodes:
            node.display()

        # OpenGLUtils.draw_text(self.outboard_node, "X: {:.1f} Y:{:.1f} Z:{:.1f} rotation length: {:.2f}".format(
        #     self.outboard_node.x, self.outboard_node.y, self.outboard_node.z,
        #     self.outboard_node.dist_between_axis(self.inboard_rear_node, self.inboard_front_node)))
