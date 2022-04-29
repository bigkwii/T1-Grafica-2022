#from asyncio.windows_events import NULL
import math
from OpenGL.GL import *
import es

# A simple class container to store vertices and indices that define a shape
class Shape:
    def __init__(self, vertices, indices):
        self.vertices = vertices
        self.indices = indices

    def __str__(self):
        return "vertices: " + str(self.vertices) + "\n"\
            "indices: " + str(self.indices)

    def getGPUShape(self, pipeline):
        gpushape = es.GPUShape().initBuffers()
        pipeline.setupVAO(gpushape)
        gpushape.fillBuffers(self.vertices, self.indices, GL_STATIC_DRAW)
        return gpushape

def createColorQuad(r, g, b):

    # Defining locations and colors for each vertex of the shape    
    vertices = [
    #   positions        colors
        -0.5, -0.5, 0.0,  r, g, b,
         0.5, -0.5, 0.0,  r, g, b,
         0.5,  0.5, 0.0,  r, g, b,
        -0.5,  0.5, 0.0,  r, g, b]

    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = [
         0, 1, 2,
         2, 3, 0]

    return Shape(vertices, indices)


def createEmptyColorCircle(N, r, g, b, l, f):

    # First vertex at the center
    vertices = []
    indices = []

    dtheta = f * 2 * math.pi / N

    for i in range(N):
        theta = i * dtheta

        newV= [
            # vertex coordinates
            math.cos(theta), math.sin(theta), 0,
            # color
            r, g, b,
            # vertex coordinates
            l*math.cos(theta), l*math.sin(theta), 0,
            # color
            r, g, b]
        vertices += newV
        indices += [2*i, 2*i+1, 2*i+2, 2*i+1, 2*i+2, 2*i+3]

    if(f == 1):
        indices += [2*N-2, 2*N-1, 0, 0, 1, 2*N-1]
    

    return Shape(vertices, indices)