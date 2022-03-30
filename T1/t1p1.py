'''
Tarea 1 parte 1
'''

import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy as np
import tr
import es

width = 800
height = 600
ar = width/height # aspect ratio
tuNombre = "Álvaro"
l = len(tuNombre)
_r = ord(tuNombre[0%l])*ord(tuNombre[1%l])%255
_g = ord(tuNombre[2%l])*ord(tuNombre[3%l])%255
_b = ord(tuNombre[4%l])*ord(tuNombre[5%l])%255

# This controller will allow to toggle wireframe by hitting spacebar
class Controller:
    fillPolygon = True

# we will use the global controller as communication with the callback function
controller = Controller()

def on_key(window, key, scancode, action, mods):

    if action != glfw.PRESS:
        return
    
    global controller

    if key == glfw.KEY_SPACE:
        controller.fillPolygon = not controller.fillPolygon

    elif key == glfw.KEY_ESCAPE:
        glfw.set_window_should_close(window, True)

    else:
        print('Unknown key')

def createLogo(x=0.0,y=0.0,r=1.0,g=1.0,b=1.0):
    '''
    Here's the logo
    '''
    vertexData = np.array([
        # POS                   RGB
        #x     y     z          r   g   b
         0.5,  0.5,  0.0,       r,  g , b,
        -0.5, -0.5,  0.0,       r,  g , b,
         0.5, -0.5,  0.0,       r,  g , b

    ], dtype=np.float32)

    indexData = np.array(
        [
            0,1,2
        ], dtype=np.uint32)
    
    return vertexData , indexData

if __name__ == "__main__":

    # Initialize glfw
    window = None
    if not glfw.init():
        glfw.set_window_should_close(window, True)

    window = glfw.create_window(width, height, "Tarea 1 p1 uwu", None, None)

    if not window:
        glfw.terminate()
        glfw.set_window_should_close(window, True)

    glfw.make_context_current(window)
    glfw.set_key_callback(window, on_key)
 
    # Creating our shader program and telling OpenGL to use it
    pipeline = es.SimpleTransformShaderProgram()
    glUseProgram(pipeline.shaderProgram)

    # Setting up the clear screen color
    glClearColor(0.15, 0.15, 0.15, 1.0)

    # Creating shapes on GPU memory
    logo = createLogo(0 , 0, _r, _g, _b)
    gpuThing = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuThing)
    gpuThing.fillBuffers(logo[0], logo[1], GL_STATIC_DRAW)

    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

    t0 = glfw.get_time()

    while not glfw.window_should_close(window):
        # counting time
        t1 = glfw.get_time()
        dt = t1 - t0
        t0 = t1

        # Using GLFW to check for input events
        glfw.poll_events()

        # Filling or not the shapes depending on the controller state
        if (controller.fillPolygon):
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        else:
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

        # Clearing the screen in both, color and depth
        glClear(GL_COLOR_BUFFER_BIT)

        # Transformations
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "transform"), 1, GL_TRUE, tr.matmul(
            [tr.translate(0, 0, 0),
            tr.rotationZ(0.0),
            tr.scale(1.0, 1.0, 1.0)]
        ))

        # Drawing the Shapes
        pipeline.drawCall(gpuThing)

        # Once the render is done, buffers are swapped, showing only the complete scene.
        glfw.swap_buffers(window)

    # freeing GPU memory
    gpuThing.clear()

    glfw.terminate()