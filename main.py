from ProjectionViewer import ProjectionViewer
from Node import Node
from Aarm import Aarm
from Tierod import Tierod
from Corner import Corner
from Frame import Frame
from Origin import Origin

WIDTH = 1920
HEIGHT = 1080

if __name__ == "__main__":
    pv = ProjectionViewer(WIDTH, HEIGHT)
    origin = Origin()
    upper_a_arm_color = (100, 255, 100)
    lower_a_arm_color = (100, 100, 255)
    tie_rod_color = (255, 100, 255)

    # ---LEFT CORNER--- #
    # Define upper left a-arm
    # in rear, in front, outboard, color
    u_l_a_arm = Aarm(Node(-100, 25, -100, 2, upper_a_arm_color),
                     Node(-100, 25, 100, 2, upper_a_arm_color),
                     Node(-200, 25, 0, 2, upper_a_arm_color),
                     upper_a_arm_color)

    # Define lower left a-arm
    l_l_a_arm = Aarm(Node(-100, -25, -100, 2, lower_a_arm_color),
                     Node(-100, -25, 100, 2, lower_a_arm_color),
                     Node(-200, -25, 0, 2, lower_a_arm_color),
                     lower_a_arm_color)

    # ---RIGHT CORNER--- #
    # Define upper right a-arm
    u_r_a_arm = Aarm(Node(100, 25, -100, 2, upper_a_arm_color),
                     Node(100, 25, 100, 2, upper_a_arm_color),
                     Node(200, 25, 0, 2, upper_a_arm_color),
                     upper_a_arm_color)

    # Define lower right a-arm
    l_r_a_arm = Aarm(Node(100, -25, -100, 2, lower_a_arm_color),
                     Node(100, -25, 100, 2, lower_a_arm_color),
                     Node(200, -25, 0, 2, lower_a_arm_color),
                     lower_a_arm_color)

    # Define left tie rod
    l_tie_rod = Tierod(Node(-100, -25, 125, 3, tie_rod_color),
                       Node(-200, -25, 100, 3, tie_rod_color),
                       tie_rod_color)

    r_tie_rod = Tierod(Node(100, -25, 125, 3, tie_rod_color),
                       Node(200, -25, 100, 3, tie_rod_color),
                       tie_rod_color)

    front_left_corner = Corner([u_l_a_arm, l_l_a_arm, l_tie_rod])
    front_right_corner = Corner([u_r_a_arm, l_r_a_arm, r_tie_rod])

    front = Frame([front_left_corner, front_right_corner])

    pv.add_wireframe('frame', front)
    pv.add_wireframe('front left', front_left_corner)
    pv.add_wireframe('front right', front_right_corner)
    pv.add_wireframe('origin', origin)

    pv.run()
