import math

import OpenGL.raw.GLUT as glut
from OpenGL.GL import *
from OpenGL.GLU import *


def render_cylinder_complex(node1, node2, radius, num_slices, quadratic, cyl_color):
    vx = node2.x - node1.x
    vy = node2.y - node1.y
    vz = node2.z - node1.z

    # If vz = 0, it will cause problems, so approximate it
    if vz == 0:
        vz = .0001

    v = (math.sqrt(vx * vx +
                   vy * vy +
                   vz * vz))

    ax = 57.2957795 * math.acos(vz / v)
    if vz < 0.0:
        ax = -ax
    rx = -vy * vz
    ry = vx * vz
    glPushMatrix()

    # Draw the cylinders body
    glColor(cyl_color[0] / 255.0, cyl_color[1] / 255.0, cyl_color[2] / 255.0)
    glTranslatef(node1.x, node1.y, node1.z)
    glRotatef(ax, rx, ry, 0.0)
    gluQuadricOrientation(quadratic, GLU_OUTSIDE)
    gluCylinder(quadratic, radius, radius, v, num_slices, 1)

    glPopMatrix()


def render_cylinder(node1, node2, radius, subdivisions, cyl_color):
    quadratic = gluNewQuadric()
    gluQuadricNormals(quadratic, GLU_SMOOTH)
    render_cylinder_complex(node1, node2, radius, subdivisions, quadratic, cyl_color)
    gluDeleteQuadric(quadratic)


def render_point(node, node_color, radius, num_slices):
    quadratic = gluNewQuadric()
    glPushMatrix()
    gluQuadricOrientation(quadratic, GLU_INSIDE)
    glTranslatef(node.x, node.y, node.z)
    glColor(node_color[0] / 255.0, node_color[1] / 255.0, node_color[2] / 255.0)
    gluSphere(quadratic, radius, num_slices, 10)
    glPopMatrix()
    gluDeleteQuadric(quadratic)


def draw_torus(node, inner_radius, outer_radius, num_sides, rings):
    glPushMatrix()
    glTranslatef(node.x, node.y, node.z)
    glColor(0.2, 0.2, 0.2)
    glRotatef(90.0, 0.0, 1.0, 0.0)
    glut.glutSolidTorus(inner_radius, outer_radius, num_sides, rings)
    glPopMatrix()


def draw_tire(inner_node, outer_node, inner_radius, outer_radius, sub_divs, rings):
    render_cylinder(inner_node, outer_node, inner_radius, sub_divs, (51, 51, 51))
    render_cylinder(inner_node, outer_node, outer_radius, sub_divs, (51, 51, 51))
    draw_torus(inner_node, (outer_radius - inner_radius) / 2, (inner_radius + outer_radius) / 2, sub_divs, rings)
    draw_torus(outer_node, (outer_radius - inner_radius) / 2, (inner_radius + outer_radius) / 2, sub_divs, rings)


# def draw_text(position, text_string):
#     glRasterPos3d(position.x, position.y, position.z)
#     for char in text_string:
#         glut_.glutBitmapCharacter(GLUT_BITMAP_TIMES_ROMAN_24, ord(char))


def render_reference_grid(half_grid_size, step):
    glBegin(GL_LINES)

    glColor3f(0.75, 0.75, 0.75)
    for i in range(-half_grid_size, half_grid_size, step):
        glVertex3f(float(i), 0, float(-half_grid_size))
        glVertex3f(float(i), 0, float(half_grid_size))

        glVertex3f(float(-half_grid_size), 0, float(i))
        glVertex3f(float(half_grid_size), 0, float(i))

    glEnd()
