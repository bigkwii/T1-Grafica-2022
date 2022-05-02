# coding=utf-8
"""
Interactions with keyboard and mouse via GLFW/python

More information at:
https://www.glfw.org/docs/latest/input_guide.html

How to convert GLFW/C calls to GLFW/python
https://pypi.org/project/glfw/
"""

import tr, bs, glfw
from OpenGL.GL import *
from sys import argv, exit
import numpy as np
import es
import sys
import os.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

width = 896
height = 504
try:
    assert(width/height == 16/9)
except:
    print("Resolution must be 16:9")
    exit()

def getAssetPath(filename):
    """Convenience function to access assets files regardless from where you run the example script."""

    thisFilePath = os.path.abspath(__file__)
    thisFolderPath = os.path.dirname(thisFilePath)
    assetsDirectory = os.path.join(thisFolderPath, "assets")
    requestedPath = os.path.join(assetsDirectory, filename)
    return requestedPath

def asCartesian(rthetaphi):
    '''
    Takes an array of a radius, theta, phi and returns a cartesian coordinate
    Swapping y and z since I want +y to be UP.
    '''
    r       = rthetaphi[0]
    theta   = rthetaphi[1]
    phi     = rthetaphi[2]
    x = r * np.sin( theta ) * np.cos( phi )
    y = r * np.sin( theta ) * np.sin( phi )
    z = r * np.cos( theta )
    return np.array([x,z,y])

# Controller class
class Controller:
    def __init__(self):
        self.fillPolygon = True
        self.radius = 3
        self.theta = np.pi/2
        self.phi = 0
        self.eye = asCartesian([self.radius, self.theta, self.phi])

# our controller
controller = Controller()

def on_key(window, key, scancode, action, mods):
    if action != glfw.PRESS:
        return
    global controller
    if key == glfw.KEY_SPACE:
        controller.fillPolygon = not controller.fillPolygon
    elif key == glfw.KEY_ESCAPE:
        glfw.set_window_should_close(window, True)
    elif key == glfw.KEY_W:
        controller.theta = (controller.theta-np.pi/90)%(2*np.pi)
        controller.eye = asCartesian([controller.radius, controller.theta, controller.phi])
    elif key == glfw.KEY_S:
        controller.theta = (controller.theta+np.pi/90)%(2*np.pi)
        controller.eye = asCartesian([controller.radius, controller.theta, controller.phi])
    elif key == glfw.KEY_A:
        controller.phi = (controller.phi+np.pi/90)%(2*np.pi)
        controller.eye = asCartesian([controller.radius, controller.theta, controller.phi])
    elif key == glfw.KEY_D:
        controller.phi = (controller.phi-np.pi/90)%(2*np.pi)
        controller.eye = asCartesian([controller.radius, controller.theta, controller.phi])
        
    else:
        print('Unknown key')

def main():

    window = None # Just putting this here so the next instane of window isn't underlined by vscode

    # Initialize glfw
    if not glfw.init():
        glfw.set_window_should_close(window, True)
        return
    
    window = glfw.create_window(width, height, "T1P2", None, None)

    if not window: 
        glfw.terminate()
        glfw.set_window_should_close(window, True)
        return
    
    glfw.make_context_current(window)
    
    # Connecting the callback function 'on_key' to handle keyboard events
    glfw.set_key_callback(window, on_key)

    # A simple shader program with position and texture coordinates as inputs.
    pipeline = es.SimpleTextureModelViewProjectionShaderProgram()

    # Telling OpenGL to use our shader program
    glUseProgram(pipeline.shaderProgram)

    # Setting up the clear screen color
    glClearColor(0.25, 0.25, 0.25, 1.0)

    # Creating shapes on GPU memory
    # Texture Sphere!
    shape = bs.createTextureSphere(4, 2)
    gpuShape = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuShape)
    gpuShape.fillBuffers(shape.vertices, shape.indices, GL_STATIC_DRAW)
    gpuShape.texture = es.textureSimpleSetup(
        getAssetPath("earth.png"), GL_CLAMP_TO_EDGE, GL_CLAMP_TO_EDGE, GL_LINEAR, GL_LINEAR
    )

    # Color Sphere!
    # shape = bs.createSphere(1,0,0,100, 100)
    # gpuShape = es.GPUShape().initBuffers()
    # pipeline.setupVAO(gpuShape)
    # gpuShape.fillBuffers(shape.vertices, shape.indices, GL_STATIC_DRAW)


    # Projection and view
    projection = tr.perspective(45, float(width)/float(height), 0.1, 100)
    view = tr.lookAt(
            controller.eye,
            np.array([0,0,0]),
            np.array([0,1,0])
        )

    # MAIN LOOP
    while not glfw.window_should_close(window):
        # Using GLFW to check for input events
        glfw.poll_events()

        if (controller.fillPolygon):
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        else:
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

        # Update eye position
        view = tr.lookAt(
            controller.eye,
            np.array([0,0,0]),
            np.array([0,1,0])
        )

        # Clearing the screen in both, color and depth
        glClear(GL_COLOR_BUFFER_BIT)

        # Drawing the shapes        
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "transform"), 1, GL_TRUE, tr.uniformScale(1.5))
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "view"), 1, GL_TRUE, view)
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "model"), 1, GL_TRUE, tr.matmul([
            tr.translate(0.0, 0.0, 0.0),          
            tr.scale(1.0, 1.0, 1.0)
        ]))

        pipeline.drawCall(gpuShape)

        # Once the render is done, buffers are swapped, showing only the complete scene.
        glfw.swap_buffers(window)
    
    # freeing GPU memory
    gpuShape.clear()

    glfw.terminate()

if __name__ == "__main__":
    main()

