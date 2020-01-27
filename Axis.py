import OpenGLUtils


class Axis:
    def __init__(self, dir_vector, point, color=(55, 55, 55)):
        self.dir_vector = dir_vector
        self.point = point
        self.color = color

    @staticmethod
    def axis_from_two_points(point1, point2):
        return Axis(point2-point1, point1)

    def display(self):
        self.point.display()
        OpenGLUtils.draw_cone(self.point, self.dir_vector, self.color)
