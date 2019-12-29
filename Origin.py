from Wireframe import Wireframe
from Edge import Edge
from Node import Node


class Origin(Wireframe):
    def __init__(self):
        super().__init__()

        x_edge = Edge(Node(0, 0, 0, 2, (255, 0, 0)), Node(10, 0, 0, 2, (255, 0, 0)), 2, (255, 0, 0))
        y_edge = Edge(Node(0, 0, 0, 2, (0, 255, 0)), Node(0, 10, 0, 2, (0, 255, 0)), 2, (0, 255, 0))
        z_edge = Edge(Node(0, 0, 0, 2, (0, 0, 255)), Node(0, 0, 10, 2, (0, 0, 255)), 2, (0, 0, 255))

        self.add_edges([x_edge, y_edge, z_edge])

    def display(self):
        for edge in self.edges:
            edge.display()
