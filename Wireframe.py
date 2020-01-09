class Wireframe:
    def __init__(self):
        self.nodes = []
        self.edges = []

    def add_nodes(self, node_list):
        for node in node_list:
            self.nodes.append(node)

    def add_edges(self, edge_list):
        for edge in edge_list:
            self.edges.append(edge)

    def output_nodes(self):
        print("\n --- nodes ---")
        for i, node in enumerate(self.nodes):
            print(" {0}: ({1:2f}, {2:2f}, {3:2f})".format(i, node.x, node.y, node.z))

    def output_edges(self):
        print("\n --- edges ---")
        for i, edge in enumerate(self.edges):
            print(" {0}: ({1:2f}, {2:2f}, {3:2f})".format(i, edge.start.x, edge.start.y, edge.start.z))
            print("to ({0:2f}, {1:2f}, {2:2f})".format(edge.stop.x, edge.stop.y, edge.stop.z))

    def find_center(self):
        """ Find the centre of the wireframe. """
        num_nodes = len(self.nodes)
        mean_x = sum([node.x for node in self.nodes]) / num_nodes
        mean_y = sum([node.y for node in self.nodes]) / num_nodes
        mean_z = sum([node.z for node in self.nodes]) / num_nodes
        return mean_x, mean_y, mean_z
