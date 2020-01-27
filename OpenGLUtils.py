import math
import OpenGL.GLUT as glut
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


def draw_tori(node1, node2, inner_radius, outer_radius, num_sides, rings):
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
    glColor(0.2, 0.2, 0.2)
    glTranslatef(node1.x, node1.y, node1.z)
    glRotatef(ax, rx, ry, 0.0)
    glut.glutSolidTorus(inner_radius, outer_radius, num_sides, rings)
    glPopMatrix()

    glPushMatrix()
    glColor(0.2, 0.2, 0.2)
    glTranslatef(node2.x, node2.y, node2.z)
    glRotatef(ax, rx, ry, 0.0)
    glut.glutSolidTorus(inner_radius, outer_radius, num_sides, rings)
    glPopMatrix()


def draw_tire(inner_node, outer_node, inner_radius, outer_radius, sub_divs, rings):
    render_cylinder(inner_node, outer_node, inner_radius, sub_divs, (51, 51, 51))
    render_cylinder(inner_node, outer_node, outer_radius, sub_divs, (51, 51, 51))
    draw_tori(inner_node, outer_node, (outer_radius - inner_radius) / 2,
              (inner_radius + outer_radius) / 2, sub_divs, rings)


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


def rotate_node_formula_axis(rotate_node, axis, theta):
    direction_vector = axis.dir_vector

    length = direction_vector.magnitude()

    a = axis.point.x
    b = axis.point.y
    c = axis.point.z

    u = float(direction_vector.x) / length
    v = float(direction_vector.y) / length
    w = float(direction_vector.z) / length

    x = rotate_node.x
    y = rotate_node.y
    z = rotate_node.z

    u2 = u * u
    v2 = v * v
    w2 = w * w

    cos_t = math.cos(theta)

    one_minus_cos_t = 1 - cos_t

    sin_t = math.sin(theta)

    rotate_node.x = (a * (v2 + w2) - u * (
            b * v + c * w - u * x - v * y - w * z)) * one_minus_cos_t + x * cos_t + (
                            -c * v + b * w - w * y + v * z) * sin_t

    rotate_node.y = (b * (u2 + w2) - v * (
            a * u + c * w - u * x - v * y - w * z)) * one_minus_cos_t + y * cos_t + (
                            c * u - a * w + w * x - u * z) * sin_t

    rotate_node.z = (c * (u2 + v2) - w * (
            a * u + b * v - u * x - v * y - w * z)) * one_minus_cos_t + z * cos_t + (
                            -b * u + a * v - v * x + u * y) * sin_t


def rotate_node_formula(rotate_node, axis_node1, axis_node2, theta):
    direction_vector = axis_node1 - axis_node2

    length = direction_vector.magnitude()

    a = axis_node2.x
    b = axis_node2.y
    c = axis_node2.z

    u = float(direction_vector.x) / length
    v = float(direction_vector.y) / length
    w = float(direction_vector.z) / length

    x = rotate_node.x
    y = rotate_node.y
    z = rotate_node.z

    u2 = u * u
    v2 = v * v
    w2 = w * w

    cos_t = math.cos(theta)

    one_minus_cos_t = 1 - cos_t

    sin_t = math.sin(theta)

    rotate_node.x = (a * (v2 + w2) - u * (
            b * v + c * w - u * x - v * y - w * z)) * one_minus_cos_t + x * cos_t + (
                            -c * v + b * w - w * y + v * z) * sin_t

    rotate_node.y = (b * (u2 + w2) - v * (
            a * u + c * w - u * x - v * y - w * z)) * one_minus_cos_t + y * cos_t + (
                            c * u - a * w + w * x - u * z) * sin_t

    rotate_node.z = (c * (u2 + v2) - w * (
            a * u + b * v - u * x - v * y - w * z)) * one_minus_cos_t + z * cos_t + (
                            -b * u + a * v - v * x + u * y) * sin_t


def draw_cone(point, vector, color):
    vx = vector.x
    vy = vector.y
    vz = vector.z

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

    quadratic = gluNewQuadric()
    glPushMatrix()

    glColor(color[0] / 255.0, color[1] / 255.0, color[2] / 255.0)
    glTranslatef(point.x, point.y, point.z)
    glRotatef(ax, rx, ry, 0.0)
    gluCylinder(quadratic, 5, 5, v, 20, 1)

    glTranslatef(point.x + vector.x, point.y + vector.y, point.z + vector.z)
    glut.glutSolidCone(10, 10, 20, 20)

    glPopMatrix()
    gluDeleteQuadric(quadratic)
