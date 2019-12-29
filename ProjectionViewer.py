import math
import pygame
import OpenGLUtils
from OpenGL.GL import *
from OpenGL.GLU import *
from pygame.locals import *
from time import time
from Corner import Corner
import numpy


class ProjectionViewer:
    """ Displays 3D objects on a Pygame screen """

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height), OPENGL | DOUBLEBUF)
        pygame.display.set_caption('Wireframe Display')
        pygame.init()
        self.background = (10, 10, 50)

        # Defining camera position
        self.lastPosX = 0
        self.lastPosY = 0
        self.zoomScale = 1.0
        self.dataL = 0
        self.xRot = 0
        self.yRot = 0
        self.zRot = 0

        # Defining bump amt
        self.bump_height = 25.0
        self.bump_step = 0.0
        self.bump_step_amt = 0.01
        self.bump_time = time()
        self.bump_check_time = 0.01
        self.bump_toggle = False

        # Defining squat amt
        self.squat_height = 25.0
        self.squat_step = 0.0
        self.squat_step_amt = 0.01
        self.squat_time = time()
        self.squat_check_time = 0.01
        self.squat_toggle = False

        #
        self.wireframes = {}
        self.displayNodes = True
        self.displayEdges = True
        self.nodeRadius = 4
        self.clock = pygame.time.Clock()
        self.key_to_function = {
            pygame.K_b: (lambda x: x.toggle_bump()),
            pygame.K_l: (lambda x: x.toggle_squat()),
            pygame.K_m: (lambda x: x.reset())}

    def run(self):
        """ Create a pygame screen until it is closed. """
        running = True

        glMatrixMode(GL_PROJECTION)
        glEnable(GL_TEXTURE_2D)
        glEnable(GL_DEPTH_TEST)
        glLoadIdentity()
        gluPerspective(30, float(self.width) / self.height, 1, 10000)
        glTranslate(0, 0, -750)

        while running:
            self.bump()
            self.squat()

            for event in pygame.event.get():
                self.mouse_move(event)
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key in self.key_to_function:
                        self.key_to_function[event.key](self)

            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            self.display()
            OpenGLUtils.draw_torus(-200, 0, 0, 15, 50, 50, 50)
            OpenGLUtils.draw_torus(200, 0, 0, 15, 50, 50, 50)
            self.draw_text((0, 0, 0), "Bump Height: {0:.1f}".
                           format(self.bump_height * math.sin(self.bump_step * math.pi)))
            pygame.display.flip()
            self.clock.tick(60)

    def add_wireframe(self, wireframe_name, wireframe):
        self.wireframes[wireframe_name] = wireframe

    def display(self):
        for wireframe in self.wireframes.values():
            wireframe.display()

    def toggle_bump(self):
        if self.squat_toggle:
            self.squat_toggle = not self.squat_toggle

        self.bump_toggle = not self.bump_toggle

    def toggle_squat(self):
        if self.bump_toggle:
            self.bump_toggle = not self.bump_toggle

        self.squat_toggle = not self.squat_toggle

    def bump(self):
        if self.bump_toggle:
            if time() - self.bump_time > self.squat_check_time:
                self.bump_time = time()
                self.bump_step += self.bump_step_amt
                for (wf_name, wireframe) in self.wireframes.items():
                    if isinstance(wireframe, Corner):
                        wireframe.bump(self.bump_height * math.sin(self.bump_step * math.pi))

    def squat(self):
        if self.squat_toggle:
            if time() - self.squat_time > self.squat_check_time:
                self.squat_time = time()
                self.squat_step += self.squat_step_amt
                for (wf_name, wireframe) in self.wireframes.items():
                    if isinstance(wireframe, Corner):
                        wireframe.squat(self.squat_height * math.sin(self.squat_step * math.pi))

    # Resets the bump and squat of the system
    def reset(self):
        self.wireframes['front left'].bump(0)
        self.wireframes['front right'].bump(0)
        self.bump_step = 0.0

        self.wireframes['front left'].squat(0)
        self.wireframes['front right'].squat(0)
        self.squat_step = 0.0

    @staticmethod
    def mouse_move(event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 4:  # wheel rolled up
            glScaled(1.05, 1.05, 1.05)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 5:  # wheel rolled down
            glScaled(0.95, 0.95, 0.95)

        mouse_dx, mouse_dy = pygame.mouse.get_rel()
        if pygame.mouse.get_pressed()[0]:
            look_speed = 0.5
            buffer = glGetDoublev(GL_MODELVIEW_MATRIX)
            c = (-1 * numpy.mat(buffer[:3, :3]) * numpy.mat(buffer[3, :3]).T).reshape(3, 1)
            # c is camera center in absolute coordinates,
            # we need to move it back to (0,0,0)
            # before rotating the camera
            glTranslate(c[0], c[1], c[2])
            m = buffer.flatten()
            glRotate(mouse_dx * look_speed, m[1], m[5], m[9])
            glRotate(mouse_dy * look_speed, m[0], m[4], m[8])

            # compensate roll
            glRotated(-math.atan2(-m[4], m[5]) * 57.295779513082320876798154814105, m[2], m[6], m[10])
            glTranslate(-c[0], -c[1], -c[2])

    @staticmethod
    def init_lights():
        glEnable(GL_LIGHTING)
        glLightModeli(GL_LIGHT_MODEL_TWO_SIDE, GL_TRUE)

        ambient = (.1, .1, .1)
        diffuse = (.5, .5, .5)
        specular = (0.0, 0.0, 0.0, 1.0)
        pos = (-1000, 2000, 0, 1)

        glLightModelfv(GL_LIGHT_MODEL_AMBIENT, ambient)
        glLightfv(GL_LIGHT0, GL_AMBIENT, ambient)
        glLightfv(GL_LIGHT0, GL_DIFFUSE, diffuse)
        glLightfv(GL_LIGHT0, GL_SPECULAR, specular)
        glLightfv(GL_LIGHT0, GL_POSITION, pos)

        glEnable(GL_LIGHT0)

        mat_specular = (1.0, 1.0, 1.0, 1.0)
        mat_diffuse = (1.0, 1.0, 1.0, 1.0)
        mat_ambient = (1.0, 1.0, 1.0, 1.0)
        mat_emission = (1.0, 1.0, 1.0, 1.0)
        mat_shininess = 10.0

        glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, mat_specular)
        glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, mat_diffuse)
        glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, mat_ambient)
        glMaterialfv(GL_FRONT_AND_BACK, GL_EMISSION, mat_emission)
        glMaterialfv(GL_FRONT_AND_BACK, GL_SHININESS, mat_shininess)

        glShadeModel(GL_SMOOTH)

        glEnable(GL_NORMALIZE)

    @staticmethod
    def draw_text(position, text_string):
        font = pygame.font.Font(None, 64)
        text_surface = font.render(text_string, True, (255, 255, 255, 255), (0, 0, 0, 255))
        text_data = pygame.image.tostring(text_surface, "RGBA", True)
        glRasterPos3d(*position)
        glDrawPixels(text_surface.get_width(), text_surface.get_height(), GL_RGBA, GL_UNSIGNED_BYTE, text_data)
