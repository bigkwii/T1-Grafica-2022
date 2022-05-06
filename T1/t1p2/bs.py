#from asyncio.windows_events import NULL
import math
from OpenGL.GL import *
import es
import numpy as np

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

def createCube(r,g,b):
    # Defining locations and colors for each vertex of the shape
    vertices = [
    #    positions         colors
        -0.5, -0.5,  0.5,  r,g,b,
         0.5, -0.5,  0.5,  r,g,b,
         0.5,  0.5,  0.5,  r,g,b,
        -0.5,  0.5,  0.5,  r,g,b,
        -0.5, -0.5, -0.5,  r,g,b,
         0.5, -0.5, -0.5,  r,g,b,
         0.5,  0.5, -0.5,  r,g,b,
        -0.5,  0.5, -0.5,  r,g,b]

    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = [
         0, 1, 2, 2, 3, 0,
         4, 5, 6, 6, 7, 4,
         4, 5, 1, 1, 0, 4,
         6, 7, 3, 3, 2, 6,
         5, 6, 2, 2, 1, 5,
         7, 4, 0, 0, 3, 7]

    return Shape(vertices, indices)

def createSphere(r,g,b,slices,stacks):
    '''
    There are many ways to generate a sphere.
    You can read all about it here:
    http://www.songho.ca/opengl/gl_sphere.html#:~:text=In%20order%20to%20draw%20the,triangle%20strip%20cannot%20be%20used.
    We will use the first one because, well, it's easy.
    This Sphere is a Single color.
    '''
    vertices = []
    indices = []
    sliceStep = 2*np.pi/slices
    stackStep = np.pi/stacks
    # vertices
    for i in range(stacks+1):
        lon = i*stackStep
        for j in range(slices+1):
            lat = j*sliceStep
            x = np.sin(lon)*np.sin(lat)
            y = np.cos(lon)
            z = np.sin(lon)*np.cos(lat)
            nx = j/slices
            ny = i/stacks
            vertices += [x,y,z,r,g,b]
    # indices TODO: fix this
    for i in range(stacks):
        k1 = i*(slices+1)
        k2 = k1 + slices + 1
        for j in range(slices):
            indices += [k1, k2, k1+1]
            indices += [k1+1, k2, k2+1]
            k1 += 1
            k2 += 1
    return Shape(vertices, indices)

def createTextureSphere(slices,stacks):
    '''
    There are many ways to generate a sphere.
    You can read all about it here:
    http://www.songho.ca/opengl/gl_sphere.html#:~:text=In%20order%20to%20draw%20the,triangle%20strip%20cannot%20be%20used.
    We will use the first one because, well, it's easy to texture.
    This assumes that the entire texture will be used, that +y is UP and that the radius is 1.
    '''
    vertices = []
    indices = []
    sliceStep = 2*np.pi/slices
    stackStep = np.pi/stacks
    # vertices
    for i in range(stacks+1):
        lon = i*stackStep
        for j in range(slices+1):
            lat = j*sliceStep
            x = np.sin(lon)*np.sin(lat)
            y = np.cos(lon)
            z = np.sin(lon)*np.cos(lat)
            nx = j/slices
            ny = i/stacks
            vertices += [x,y,z,nx,ny]
    # indices TODO: fix this
    for i in range(stacks):
        k1 = i*(slices+1)
        k2 = k1 + slices + 1
        for j in range(slices):
            indices += [k1, k2, k1+1]
            indices += [k1+1, k2, k2+1]
            k1 += 1
            k2 += 1
    return Shape(vertices, indices)

def createAlfaCube(r,g,b,a):
    '''
    Makes a rgba cube.
    '''
    # Defining the location and colors of each vertex  of the shape
    vertices = [
    #    positions         colors
        -0.5, -0.5,  0.5,  r,g,b,a,
         0.5, -0.5,  0.5,  r,g,b,a,
         0.5,  0.5,  0.5,  r,g,b,a,
        -0.5,  0.5,  0.5,  r,g,b,a,
        -0.5, -0.5, -0.5,  r,g,b,a,
         0.5, -0.5, -0.5,  r,g,b,a,
         0.5,  0.5, -0.5,  r,g,b,a,
        -0.5,  0.5, -0.5,  r,g,b,a]

    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = [
         0, 1, 2, 2, 3, 0,
         4, 5, 6, 6, 7, 4,
         4, 5, 1, 1, 0, 4,
         6, 7, 3, 3, 2, 6,
         5, 6, 2, 2, 1, 5,
         7, 4, 0, 0, 3, 7]

    return Shape(vertices, indices)





