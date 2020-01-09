from Edge import Edge
from Node import Node
from Wireframe import Wireframe


class Origin(Wireframe):
    def __init__(self):
        super().__init__()
        base_node = Node(0, 0, 0, 10, (255, 255, 255))
        self.x_node_2 = Node(100, 0, 0, 10, (255, 0, 0))
        self.y_node_2 = Node(0, 100, 0, 10, (0, 255, 0))
        self.z_node_2 = Node(0, 0, 100, 10, (0, 0, 255))

        x_edge = Edge(base_node, self.x_node_2, 10, (255, 0, 0))
        y_edge = Edge(base_node, self.y_node_2, 10, (0, 255, 0))
        z_edge = Edge(base_node, self.z_node_2, 10, (0, 0, 255))

        self.add_edges([x_edge, y_edge, z_edge])
        self.add_nodes([self.x_node_2, self.y_node_2, self.z_node_2])

    def display(self):
        for edge in self.edges:
            edge.display()

        for node in self.nodes:
            node.display()

        # OpenGLUtils.draw_text(self.x_node_2, "X")
        # OpenGLUtils.draw_text(self.y_node_2, "Y")
        # OpenGLUtils.draw_text(self.z_node_2, "Z")
