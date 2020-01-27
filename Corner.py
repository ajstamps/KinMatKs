import math
from CombinedWireframe import CombinedWireframe
from Tierod import Tierod
from Tire import Tire
from Plane import Plane


class Corner(CombinedWireframe):
    def __init__(self, components):
        super().__init__(components)
        self.tie_rod = None
        self.a_arms = []
        self.tire = None

        for component in components:
            if type(component) == Tierod:
                self.tie_rod = component
            elif type(component) == Tire:
                self.tire = component
            else:
                self.a_arms.append(component)

    def bump(self, bump_height):
        for a_arm in self.a_arms:
            a_arm.bump(bump_height)

        self.tie_rod.bump(bump_height)

        instant_center = Plane.get_planar_intersect_axis(self.a_arms[0].get_a_arm_plane(),
                                                         self.a_arms[1].get_a_arm_plane())
        self.tire.bump(bump_height, instant_center)

    def squat(self, squat_height):
        for a_arm in self.a_arms:
            a_arm.squat(squat_height)

        self.tie_rod.squat(squat_height)

    def display(self):
        for a_arm in self.a_arms:
            a_arm.display()

        self.tie_rod.display()
        self.tire.display()
