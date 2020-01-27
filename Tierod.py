import math

import OpenGLUtils
from Edge import Edge
from Node import Node
from Wireframe import Wireframe


class Tierod(Wireframe):
    def __init__(self, inboard_node, outboard_node, tie_rod_color):
        super().__init__()
        self.inboard_node = inboard_node
        self.outboard_node = outboard_node
        self.tie_rod_color = tie_rod_color

        self.tie_rod_edge = Edge(self.inboard_node, self.outboard_node, 3, self.tie_rod_color)

        self.add_nodes([self.inboard_node, self.outboard_node])
        self.add_edges([self.tie_rod_edge])
        self.rotation_length = self.outboard_node.x - self.inboard_node.x

        self.negative_x = False
        if self.outboard_node.x < 0:
            self.negative_x = True

        self.inboard_node_store = inboard_node.y
        self.outboard_node_store = outboard_node.y

    def bump(self, bump_height):
        bump_angle = math.asin(bump_height / self.rotation_length)
        node2 = Node(self.inboard_node.x,
                     self.inboard_node.y,
                     self.inboard_node.z + 1, 0, (0, 0, 0))

        OpenGLUtils.rotate_node_formula(self.outboard_node, node2, self.inboard_node, bump_angle)

    def squat(self, squat_height):
        squat_dist_x = math.sqrt(math.pow(self.rotation_length, 2) - math.pow(squat_height, 2))

        if self.negative_x:
            self.outboard_node.x = (-squat_dist_x + self.rotation_length)
        else:
            self.outboard_node.x = (squat_dist_x + self.rotation_length)

        self.inboard_node.y = (self.inboard_node_store + squat_height)

    def display(self):
        for edge in self.edges:
            edge.display()

        for node in self.nodes:
            node.display()
        # OpenGLUtils.draw_text(self.outboard_node, "X: {:.1f} Y:{:.1f} Z:{:.1f} Length: {:.2f}"
        #                       .format(self.outboard_node.x,
        #                               self.outboard_node.y,
        #                               self.outboard_node.z,
        #                               self.outboard_node.dist_between_node(self.inboard_node)))
