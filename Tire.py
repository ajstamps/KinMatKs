import math
import OpenGLUtils
from Plane import Plane
from Wireframe import Wireframe


class Tire(Wireframe):
    def __init__(self, upper_a_arm_node, lower_a_arm_node, tie_rod_node, inner_node,
                 outer_node, rim_diameter, wheel_diameter):
        super().__init__()
        self.upper_a_arm_node = upper_a_arm_node
        self.lower_a_arm_node = lower_a_arm_node
        self.tie_rod_node = tie_rod_node
        self.inner_node = inner_node
        self.outer_node = outer_node
        self.width = inner_node.dist_between_node(outer_node)
        self.wheel_diameter = wheel_diameter
        self.rim_diameter = rim_diameter

        self.add_nodes([self.upper_a_arm_node, self.lower_a_arm_node, self.tie_rod_node])

    def display(self):
        OpenGLUtils.draw_tire(self.inner_node, self.outer_node,
                              self.rim_diameter / 2,
                              self.wheel_diameter / 2, 100, 200)

    def bump(self, bump_height, rotation_axis):
        rotation_length = self.inner_node.distance_between_axis_ax(rotation_axis)
        bump_height = -math.asin(bump_height / rotation_length)

        OpenGLUtils.rotate_node_formula_axis(self.inner_node, rotation_axis, bump_height)
        OpenGLUtils.rotate_node_formula_axis(self.outer_node, rotation_axis, bump_height)

    def get_toe(self):
        plane = Plane.plane_from_3_points(self.lower_a_arm_node, self.upper_a_arm_node, self.tie_rod_node)

        return 57.2957795 * math.asin(plane.c / math.sqrt(math.pow(plane.a, 2) +
                                                          math.pow(plane.b, 2) +
                                                          math.pow(plane.c, 2)))

    def get_camber(self):
        plane = Plane.plane_from_3_points(self.lower_a_arm_node, self.upper_a_arm_node, self.tie_rod_node)

        return 57.2957795 * math.asin(plane.b / math.sqrt(math.pow(plane.a, 2) +
                                                          math.pow(plane.b, 2) +
                                                          math.pow(plane.c, 2)))