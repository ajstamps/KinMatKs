from Wireframe import Wireframe
from Edge import Edge
from Node import Node
import math


class Tierod(Wireframe):
    def __init__(self, inboard_node, outboard_node, tie_rod_color):
        super().__init__()
        self.inboard_node = inboard_node
        self.outboard_node = outboard_node
        self.tie_rod_color = tie_rod_color

        self.tie_rod_edge = Edge(self.inboard_node, self.outboard_node, 3, self.tie_rod_color)

        self.add_nodes([self.inboard_node, self.outboard_node])
        self.add_edges([self.tie_rod_edge])
        self.rotation_length = self.outboard_node.dist_between_node(self.inboard_node)
        if self.outboard_node.x < 0:
            self.rotation_length *= -1

        self.inboard_node_store = inboard_node.y
        self.outboard_node_store = outboard_node.y

    def bump(self, bump_height):
        bump_dist_x = math.sqrt(math.pow(self.rotation_length, 2) - math.pow(bump_height, 2))

        if self.outboard_node.x < 0:
            bump_dist_x *= -1

        self.outboard_node.x = (bump_dist_x + self.rotation_length)

        self.outboard_node.y = (self.outboard_node_store + bump_height)

    def squat(self, squat_height):
        squat_dist_x = math.sqrt(math.pow(self.rotation_length, 2) - math.pow(squat_height, 2))

        if self.outboard_node.get_x() < 0:
            squat_dist_x *= -1

        self.outboard_node.x = (squat_dist_x + self.rotation_length)

        self.inboard_node.y = (self.inboard_node_store + squat_height)
