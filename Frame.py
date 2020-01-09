from Edge import Edge
from Wireframe import Wireframe


class Frame(Wireframe):
    def __init__(self, corners):
        super().__init__()
        self.node_edges = []

        self.frame_color = (255, 100, 100)

        # Front to rear of A Arm node
        self.node_edges.append(Edge(corners[0].a_arms[0].inboard_rear_node,
                                    corners[0].a_arms[0].inboard_front_node, 2, self.frame_color))

        self.node_edges.append(Edge(corners[0].a_arms[1].inboard_rear_node,
                                    corners[0].a_arms[1].inboard_front_node, 2, self.frame_color))

        self.node_edges.append(Edge(corners[1].a_arms[0].inboard_rear_node,
                                    corners[1].a_arms[0].inboard_front_node, 2, self.frame_color))

        self.node_edges.append(Edge(corners[1].a_arms[1].inboard_rear_node,
                                    corners[1].a_arms[1].inboard_front_node, 2, self.frame_color))

        # Top node to bottom node corners
        self.node_edges.append(Edge(corners[1].a_arms[0].inboard_rear_node,
                                    corners[1].a_arms[1].inboard_rear_node, 2, self.frame_color))

        self.node_edges.append(Edge(corners[1].a_arms[0].inboard_front_node,
                                    corners[1].a_arms[1].inboard_front_node, 2, self.frame_color))

        self.node_edges.append(Edge(corners[0].a_arms[0].inboard_rear_node,
                                    corners[0].a_arms[1].inboard_rear_node, 2, self.frame_color))

        self.node_edges.append(Edge(corners[0].a_arms[0].inboard_front_node,
                                    corners[0].a_arms[1].inboard_front_node, 2, self.frame_color))

        # A Arm to A Arm Tubes
        self.node_edges.append(Edge(corners[1].a_arms[0].inboard_front_node,
                                    corners[0].a_arms[0].inboard_front_node, 2, self.frame_color))

        self.node_edges.append(Edge(corners[1].a_arms[1].inboard_front_node,
                                    corners[0].a_arms[1].inboard_front_node, 2, self.frame_color))

        self.node_edges.append(Edge(corners[1].a_arms[0].inboard_rear_node,
                                    corners[0].a_arms[0].inboard_rear_node, 2, self.frame_color))

        self.node_edges.append(Edge(corners[1].a_arms[1].inboard_rear_node,
                                    corners[0].a_arms[1].inboard_rear_node, 2, self.frame_color))

        # Add edges
        self.add_edges(self.node_edges)

    def display(self):
        for edge in self.node_edges:
            edge.display()
