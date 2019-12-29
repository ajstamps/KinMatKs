from Wireframe import Wireframe


class CombinedWireframe(Wireframe):
    def __init__(self, wireframes):
        super().__init__()

        for wireframe in wireframes:
            nodes = []
            edges = []
            for node in wireframe.nodes:
                nodes.append(node)

            for edge in wireframe.edges:
                edges.append(edge)

            self.add_nodes(nodes)
            self.add_edges(edges)

    def display(self):
        for node in self.nodes:
            node.display()

        for edge in self.edges:
            edge.display()