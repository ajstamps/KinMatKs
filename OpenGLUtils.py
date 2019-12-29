import math
from OpenGL.GL import *
from OpenGL.GLU import *
import OpenGL.raw.GLUT as glut


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
    glColor(cyl_color[0]/255.0, cyl_color[1]/255.0, cyl_color[2]/255.0)
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
    gluQuadricOrientation(quadratic, GLU_INSIDE)
    glTranslatef(node.x, node.y, node.z)
    glColor(node_color[0] / 255.0, node_color[1] / 255.0, node_color[2] / 255.0)
    gluSphere(quadratic, radius, num_slices, 10)
    gluDeleteQuadric(quadratic)


def draw_torus(x, y, z, inner_radius, outer_radius, num_sides, rings):
    glPushMatrix()
    glTranslatef(x, y, z)
    glColor(0.2, 0.2, 0.2)
    glRotatef(90.0, 0.0, 1.0, 0.0)
    glut.glutSolidTorus(inner_radius, outer_radius, num_sides, rings)
    glPopMatrix()
