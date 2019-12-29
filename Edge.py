import OpenGLUtils


class Edge:
    def __init__(self, start, stop, thickness, color):
        self.start = start
        self.stop = stop
        self.thickness = thickness
        self.color = color

    def display(self):
        OpenGLUtils.render_cylinder(self.start, self.stop, self.thickness, 100, self.color)
