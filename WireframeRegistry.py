from OpenGLUtils import *
from linalg import matrix as m
from linalg import quaternion as q


class WireframeRegistry:
    def __init__(self):
        self.wireframes = {}
        self.scale = .005
        self.rotation = q.quaternion(-math.sqrt(2)/2)

    def display_all(self):
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glScale(self.scale, self.scale, self.scale)
        glMultMatrixf(m.column_major(q.matrix(self.rotation)))

        for wireframe in self.wireframes.values():
            wireframe.display()

        render_reference_grid(10000, 1000)

        glPopMatrix()

    def register(self, registered_name, registered_self):
        self.wireframes[registered_name] = registered_self
