from ctypes import c_float
from time import time
from OpenGL.GLUT import *
from Aarm import Aarm
from Corner import Corner
from Frame import Frame
from Node import Node
from OpenGLUtils import *
from Origin import Origin
from Tierod import Tierod
from Tire import Tire
from linalg import matrix as m
from linalg import quaternion as q

WIDTH = 2880
HEIGHT = 1800
wireframes = {}

PERSPECTIVE, BUMP, SQUAT, LIGHTING = b'p', b'b', b's', b'l'

perspective = False
lighting = False

rotating = False
scaling = False

rotation = q.quaternion(-math.sqrt(2)/2)
scale = .005

squat_toggle, bump_toggle = False, False

squat_check_time, bump_check_time = 0.01, 0.01

squat_step, bump_step = 0.0, 0.0

squat_step_amt, bump_step_amt = 0.01, 0.01

squat_height, bump_height = 200.0, 200.0

squat_time, bump_time = time(), time()


def create_shader(shader_type, source):
    """compile a shader."""
    shader = glCreateShader(shader_type)
    glShaderSource(shader, source)
    glCompileShader(shader)
    if glGetShaderiv(shader, GL_COMPILE_STATUS) != GL_TRUE:
        raise RuntimeError(glGetShaderInfoLog(shader))
    return shader


def init_program():
    program = glCreateProgram()

    glLinkProgram(program)
    if glGetProgramiv(program, GL_LINK_STATUS) != GL_TRUE:
        raise RuntimeError(glGetProgramInfoLog(program))

    glUseProgram(program)


def c_matrix(matrix):
    return (c_float * 16)(*m.column_major(matrix))


def draw_object():
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glScale(scale, scale, scale)
    glMultMatrixf(m.column_major(q.matrix(rotation)))

    for wireframe in wireframes.values():
        wireframe.display()

    render_reference_grid(10000, 1000)

    glPopMatrix()


def screen_shot(ss_name="screen_shot.png"):
    """window screenshot."""
    width, height = glutGet(GLUT_WINDOW_WIDTH), glutGet(GLUT_WINDOW_HEIGHT)
    data = glReadPixels(0, 0, width, height, GL_RGB, GL_UNSIGNED_BYTE)

    import png
    png.write(open(ss_name, "wb"), width, height, 3, data)


def reshape(width, height):
    """window reshape callback."""
    bump()
    squat()
    glViewport(0, 0, width, height)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    radius = .5 * min(width, height)
    w, h = width / radius, height / radius
    if perspective:
        glFrustum(-w, w, -h, h, 4, 32)
        glTranslate(0, 0, -12)
        glScale(1.5, 1.5, 1.5)
    else:
        glOrtho(-w, w, -h, h, -4, 4)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def display():
    """window redisplay callback."""
    bump()
    squat()

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    draw_object()
    glutSwapBuffers()


def keyboard(c, _x=0, _y=0):
    """keyboard callback."""
    global perspective, lighting

    if c == PERSPECTIVE:
        perspective = not perspective
        reshape(glutGet(GLUT_WINDOW_WIDTH), glutGet(GLUT_WINDOW_HEIGHT))

    elif c == SQUAT:
        toggle_squat()

    elif c == BUMP:
        toggle_bump()

    elif c == LIGHTING:
        lighting = not lighting
        if lighting:
            glEnable(GL_LIGHTING)
        else:
            glDisable(GL_LIGHTING)

    elif c == b'q':
        sys.exit(0)
    glutPostRedisplay()


def screen2space(_x, _y):
    width, height = glutGet(GLUT_WINDOW_WIDTH), glutGet(GLUT_WINDOW_HEIGHT)
    radius = max(width, height) * 1.
    return (2. * _x - width) / radius, -(2. * _y - height) / radius


def mouse(button, state, _x, _y):
    global rotating, scaling, x0, y0
    if button == GLUT_LEFT_BUTTON:
        rotating = (state == GLUT_DOWN)
    elif button == GLUT_RIGHT_BUTTON:
        scaling = -(state == GLUT_DOWN)
    x0, y0 = _x, _y


def motion(x1, y1):
    global x0, y0, rotation, scale
    if rotating:
        p0 = screen2space(x0, y0)
        p1 = screen2space(x1, y1)
        rotation = q.product(rotation, q.arcball(*p0), q.arcball(*p1))
    if scaling:
        scale *= math.exp(((x1 - x0) - (y1 - y0)) * .01)
    x0, y0 = x1, y1
    glutPostRedisplay()


def init_glut(argv):
    """glut initialization."""
    glutInit(argv)
    glutInitWindowSize(*(WIDTH, HEIGHT))
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)

    glutCreateWindow(argv[0].encode())

    glutSetWindowTitle("KinMatKs")

    glutReshapeFunc(reshape)
    glutDisplayFunc(display)
    glutKeyboardFunc(keyboard)
    glutMouseFunc(mouse)
    glutMotionFunc(motion)
    glutIdleFunc(idle)


def init_opengl():
    # depth test
    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LEQUAL)

    # lighting
    glEnable(GL_NORMALIZE)
    glEnable(GL_LIGHT0)
    light_position = [0., 10., 10., 0.]
    glLight(GL_LIGHT0, GL_POSITION, light_position)

    glEnable(GL_COLOR_MATERIAL)
    glColorMaterial(GL_FRONT, GL_AMBIENT_AND_DIFFUSE)
    glMaterialfv(GL_FRONT, GL_SPECULAR, [1., 1., 1., 1.])
    glMaterialf(GL_FRONT, GL_SHININESS, 100.)

    for k in [PERSPECTIVE, LIGHTING]:
        keyboard(k)


def add_wireframe(wireframe_name, wireframe):
    wireframes[wireframe_name] = wireframe


def toggle_bump():
    global squat_toggle, bump_toggle
    if squat_toggle:
        squat_toggle = not squat_toggle

    bump_toggle = not bump_toggle


def toggle_squat():
    global squat_toggle, bump_toggle
    if bump_toggle:
        bump_toggle = not bump_toggle

    squat_toggle = not squat_toggle


def bump():
    global bump_time, bump_step
    if bump_toggle:
        if time() - bump_time > squat_check_time:
            bump_time = time()
            bump_step += bump_step_amt
            for (wf_name, wireframe) in wireframes.items():
                if isinstance(wireframe, Corner):
                    wireframe.bump(bump_height * math.copysign(bump_step_amt, math.sin(bump_step * math.pi)))


def squat():
    global squat_time, squat_step
    if squat_toggle:
        if time() - squat_time > squat_check_time:
            squat_time = time()
            squat_step += squat_step_amt
            for (wf_name, wireframe) in wireframes.items():
                if isinstance(wireframe, Corner):
                    copy_sign_output = math.copysign(squat_step_amt, math.sin(squat_step * math.pi))
                    temp_squat_height = squat_height * copy_sign_output
                    wireframe.squat(temp_squat_height)


# Resets the bump and squat of the system
def reset(self):
    self.wireframes['front left'].bump(0)
    self.wireframes['front right'].bump(0)
    self.bump_step = 0.0

    self.wireframes['front left'].squat(0)
    self.wireframes['front right'].squat(0)
    self.squat_step = 0.0


def idle():
    glutPostRedisplay()


def main(argv=None):
    if argv is None:
        argv = sys.argv

    origin = Origin(0, 100, 0)
    upper_a_arm_color = (100, 255, 100)
    lower_a_arm_color = (100, 100, 255)
    tie_rod_color = (255, 100, 255)

    # ---LEFT CORNER--- #
    # Define upper left a-arm
    # in rear, in front, outboard, color
    u_l_a_arm_outboard = Node(-555, 400, 0, 10, upper_a_arm_color)
    u_l_a_arm = Aarm(Node(-200, 375, -250, 10, upper_a_arm_color),
                     Node(-200, 375, 250, 10, upper_a_arm_color),
                     u_l_a_arm_outboard,
                     upper_a_arm_color)

    # Define lower left a-arm
    l_l_a_arm_outboard = Node(-555, 140, 0, 10, lower_a_arm_color)
    l_l_a_arm = Aarm(Node(-200, 150, -250, 10, lower_a_arm_color),
                     Node(-200, 150, 250, 10, lower_a_arm_color),
                     l_l_a_arm_outboard,
                     lower_a_arm_color)

    l_tie_rod_outboard = Node(-555, 175, 100, 7, tie_rod_color)
    l_tie_rod = Tierod(Node(-200, 175, 100, 7, tie_rod_color),
                       l_tie_rod_outboard,
                       tie_rod_color)

    l_tire_inner_node = Node(-555, 265, 0, 0, (0, 0, 0))
    l_tire_outer_node = Node(-635, 265, 0, 0, (0, 0, 0))
    l_tire = Tire(u_l_a_arm_outboard, l_l_a_arm_outboard, l_tie_rod_outboard,
                  l_tire_inner_node, l_tire_outer_node, 328.9, 533.4)

    # ---RIGHT CORNER--- #
    # Define upper right a-arm
    u_r_a_arm_outboard = Node(555, 400, 0, 10, upper_a_arm_color)
    u_r_a_arm = Aarm(Node(200, 375, -250, 10, upper_a_arm_color),
                     Node(200, 375, 250, 10, upper_a_arm_color),
                     u_r_a_arm_outboard,
                     upper_a_arm_color)

    # Define lower right a-arm
    l_r_a_arm_outboard = Node(555, 140, 0, 10, lower_a_arm_color)
    l_r_a_arm = Aarm(Node(200, 150, -250, 10, lower_a_arm_color),
                     Node(200, 150, 250, 10, lower_a_arm_color),
                     l_r_a_arm_outboard,
                     lower_a_arm_color)

    r_tie_rod_outboard = Node(555, 175, 100, 7, tie_rod_color)
    r_tie_rod = Tierod(Node(200, 175, 100, 7, tie_rod_color),
                       r_tie_rod_outboard,
                       tie_rod_color)

    r_tire_inner_node = Node(555, 265, 0, 0, (0, 0, 0))
    r_tire_outer_node = Node(635, 265, 0, 0, (0, 0, 0))
    r_tire = Tire(u_r_a_arm_outboard, l_r_a_arm_outboard, r_tie_rod_outboard,
                  r_tire_inner_node, r_tire_outer_node, 328.9, 533.4)

    # Define Corners
    front_left_corner = Corner([u_l_a_arm, l_l_a_arm, l_tie_rod, l_tire])
    front_right_corner = Corner([u_r_a_arm, l_r_a_arm, r_tie_rod, r_tire])

    front = Frame([front_left_corner, front_right_corner])

    add_wireframe('frame', front)
    add_wireframe('front left', front_left_corner)
    add_wireframe('front right', front_right_corner)
    add_wireframe('origin', origin)

    init_glut(argv)
    init_program()
    init_opengl()
    return glutMainLoop()


if __name__ == "__main__":
    wireframes = {}
    sys.exit(main())
