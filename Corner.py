from CombinedWireframe import CombinedWireframe
from Tierod import Tierod
import math


class Corner(CombinedWireframe):
    def __init__(self, components):
        super().__init__(components)
        self.tie_rod = None
        self.a_arms = []

        count = 0
        for component in components:
            if type(component) == Tierod:
                self.tie_rod = component
            else:
                self.a_arms.append(component)
                count += 1

    def bump(self, bump_height):
        for a_arm in self.a_arms:
            a_arm.bump(bump_height)

        self.tie_rod.bump(bump_height)

    def squat(self, squat_height):
        for a_arm in self.a_arms:
            a_arm.squat(squat_height)

        self.tie_rod.squat(squat_height)
