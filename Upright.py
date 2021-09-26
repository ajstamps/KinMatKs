import Tire
import OpenGLUtils
import math


class Upright:
    def __init__(self, upper_susp_connection, lower_susp_connection, tie_rod_connection,
                 wheel_center_offset, static_camber, static_toe, tire_width, rim_width):
        self.upper_susp_connection = upper_susp_connection
        self.lower_susp_connection = lower_susp_connection
        self.tie_rod_connection = tie_rod_connection
        self.wheel_center_offset = wheel_center_offset
        self.static_camber = static_camber
        self.static_toe = static_toe
        self.tire_width = tire_width
        self.rim_width = rim_width

        self.node_1 = self.wheel_center_offset + (self.rim_width * 0.5)
        self.node_2 = self.wheel_center_offset - (self.rim_width * 0.5)

    def bump(self, bump_height, rotation_axis):
        rotation_length_1 = self.node_1.distance_between_axis_ax(rotation_axis)
        rotation_length_2 = self.node_2.distance_between_axis_ax(rotation_axis)

        bump_height_1 = -math.asin(bump_height / rotation_length_1)
        bump_height_2 = -math.asin(bump_height / rotation_length_2)

        OpenGLUtils.rotate_node_formula_axis(self.node_1, rotation_axis, bump_height_1)
        OpenGLUtils.rotate_node_formula_axis(self.node_2, rotation_axis, bump_height_2)
