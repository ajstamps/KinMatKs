from Wireframe import Wireframe
from Edge import Edge
from Node import Node


class Origin(Wireframe):
    def __init__(self):
        super().__init__()
        x_node_1 = Node(0, 0, 0, 2, (255, 0, 0))
        x_node_2 = Node(10, 0, 0, 2, (255, 0, 0))
        y_node_1 = Node(0, 0, 0, 2, (0, 255, 0))
        y_node_2 = Node(0, 10, 0, 2, (0, 255, 0))
        z_node_1 = Node(0, 0, 0, 2, (0, 0, 255))
        z_node_2 = Node(0, 0, 10, 2, (0, 0, 255))

        x_edge = Edge(x_node_1, x_node_2, 2, (255, 0, 0))
        y_edge = Edge(y_node_1, y_node_2, 2, (0, 255, 0))
        z_edge = Edge(z_node_1, z_node_2, 2, (0, 0, 255))

        self.add_edges([x_edge, y_edge, z_edge])
        self.add_nodes([x_node_1, x_node_2, y_node_1, y_node_2, z_node_1, z_node_2])

    def display(self):
        for edge in self.edges:
            edge.display()

        for node in self.nodes:
            node.display()
