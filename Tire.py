import math

from Wireframe import Wireframe


class Tire(Wireframe):
    def __init__(self, upper_a_arm_node, lower_a_arm_node, tie_rod_node,
                 center_of_tire_node, width, sidewall_pct, diameter):
        super().__init__()
        self.upper_a_arm_node = upper_a_arm_node
        self.lower_a_arm_node = lower_a_arm_node
        self.tie_rod_node = tie_rod_node
        self.center_of_tire_node = center_of_tire_node
        self.dist_between_a_arms = self.upper_a_arm_node.dist_between_node(self.lower_a_arm_node)
        self.width = width
        self.sidewall_pct = sidewall_pct
        self.diameter = diameter
        self.total_diameter = width / 10 + diameter

        self.add_nodes([self.upper_a_arm_node, self.lower_a_arm_node, self.tie_rod_node, self.center_of_tire_node])

    # def get_camber(self):
    #     return self.dynamic_camber_theta
    #
    # def get_toe(self):
    #     return self.dynamic_toe_theta

    def display(self):
        i = 0
        # OpenGLUtils.draw_tire(self.inner_node, self.outer_node, 330, 530, 100, 200)

    # def bump(self, bump_height, inboard_front_node, inboard_rear_node):
    #     bump_angle = math.asin(bump_height / self.rotation_length)
    #     self.rotate_node_formula(bump_angle)

    def rotate_node_formula(self, theta, inboard_front_node, inboard_rear_node):
        direction_vector = inboard_front_node - inboard_rear_node

        length = direction_vector.magnitude()

        a = inboard_rear_node.x
        b = inboard_rear_node.y
        c = inboard_rear_node.z

        u = float(direction_vector.x) / length
        v = float(direction_vector.y) / length
        w = float(direction_vector.z) / length

        x = self.center_of_tire_node.x
        y = self.center_of_tire_node.y
        z = self.center_of_tire_node.z

        u2 = u * u
        v2 = v * v
        w2 = w * w

        cos_t = math.cos(theta)

        one_minus_cos_t = 1 - cos_t

        sin_t = math.sin(theta)

        self.center_of_tire_node.x = (a * (v2 + w2) - u * (
                b * v + c * w - u * x - v * y - w * z)) * one_minus_cos_t + x * cos_t + (
                                             -c * v + b * w - w * y + v * z) * sin_t

        self.center_of_tire_node.y = (b * (u2 + w2) - v * (
                a * u + c * w - u * x - v * y - w * z)) * one_minus_cos_t + y * cos_t + (
                                             c * u - a * w + w * x - u * z) * sin_t

        self.center_of_tire_node.z = (c * (u2 + v2) - w * (
                a * u + b * v - u * x - v * y - w * z)) * one_minus_cos_t + z * cos_t + (
                                             -b * u + a * v - v * x + u * y) * sin_t
