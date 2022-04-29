# coding=utf-8
"""
Interactions with keyboard and mouse via GLFW/python

More information at:
https://www.glfw.org/docs/latest/input_guide.html

How to convert GLFW/C calls to GLFW/python
https://pypi.org/project/glfw/
"""

#from asyncio.windows_events import NULL
import tr, bs, glfw
from OpenGL.GL import *
from sys import argv, exit
import numpy as np
import es

width = 800
height = 600

# A class to control the application
class Controller:
    def __init__(self):

        self.logo = None
        self.x = 0
        self.y = 0
        self.rotation = 2
        self.velx = 0
        self.vely = 0
        self.s = 0
        self.bounced = False

    def setS(self, rut):
        self.s = (int(rut)/20000000)**8

    def setVel(self, iniciales):
        alpha = ord(iniciales[0]) * ord(iniciales[1])
        self.velx = 350 * np.cos(alpha) / 800
        self.vely = 350 * np.sin(alpha) / 600
    
    def getColor(self, nombre):
        l = len(nombre)
        r = (ord(nombre[0%l]) * ord(nombre[1%l]) % 255) /255
        g = (ord(nombre[2%l]) * ord(nombre[3%l]) % 255) /255
        b = (ord(nombre[4%l]) * ord(nombre[5%l]) % 255) /255   
        return (r, g, b)

    def createLogo(self, nombre, pipeline):
        (r, g, b) = self.getColor(nombre)
        self.logo = Logo(pipeline, r, g, b)

    def draw(self):
        if(not self.bounced):
            self.logo.draw(self.x, self.y, self.rotation, 1, 1, 1)
        else:
            self.logo.draw(self.x, self.y, self.rotation, self.s, 4/3, 3/4)

    def clear(self):
        self.logo.clear()

    def bounce(self):
        self.rotation += 0.5
        self.bounced = not self.bounced
        
    def update(self, dt):
        #calculamos el ancho de la figura
        if(self.bounced):
            offset = self.s * 0.2 *3/4
        else:
            offset = 0.2
            
        dx = self.velx*dt
        newx = self.x+dx
        if(np.abs(newx) + offset > 1):
            diff = 1 - np.abs(newx)
            if(self.bounced):
                offset = offset/self.s
            else:
                offset = offset*self.s

            if(newx > 0):
                self.x =   1 - diff - 0.1
            else:
                self.x = -(1 - diff - 0.1)
            self.velx = -self.velx
            self.bounce()
        else:
            self.x = newx
            
        if(self.bounced):
            offset *= (4/3)**2
        dy = dt*self.vely
        newy = self.y + dy 
        if(np.abs(newy) + offset > 1):
            diff = 1 - np.abs(newy)
            if(self.bounced):
                offset = offset/self.s
            else:
                offset = offset*self.s
            
            if(newy > 0):
                self.y =   1 - diff - 0.15
            else:
                self.y = -(1 - diff - 0.15)
            self.vely = -self.vely
            self.bounce()
        else:
            self.y = newy
class Logo:
    def __init__(self, pipeline, r, g, b):
        self.x = 0
        self.y = 0
        self.pipeline = pipeline
        self.shapes, self.transformations = EldenRingLogo(pipeline, r, g, b)

    def clear(self):
        for shape in self.shapes:
            shape.clear()

    def draw(self, x, y, rotations, scale, sx, sy):
        assert(len(self.shapes) == len(self.transformations))       
        for i in range(len(self.shapes)):
            glUniformMatrix4fv(glGetUniformLocation(self.pipeline.shaderProgram, "transform"), 1, GL_TRUE, tr.matmul(
                [tr.translate(x, y, 0), tr.rotationZ(rotations*np.pi), tr.scale(sx, sy, 1), tr.scale(0.5, 0.5, 0.5)] +
                [tr.scale(0.4*scale, 0.4*scale, 0.4*scale)] +
                self.transformations[i]
                ))
            self.pipeline.drawCall(self.shapes[i])

def EldenRingLogo(pipeline, r, g, b):
    background = bs.createColorQuad(0, 0, 0).getGPUShape(pipeline)
    circle = bs.createEmptyColorCircle(45, r, g, b, 0.95, 1).getGPUShape(pipeline)
    semicircle1 = bs.createEmptyColorCircle(45, r, g, b, 0.99, 1/8).getGPUShape(pipeline)
    semicircle2 = bs.createEmptyColorCircle(45, r, g, b, 0.98, 1/8).getGPUShape(pipeline)
    quad = bs.createColorQuad(r, g, b).getGPUShape(pipeline)

    shapes = [background, circle, circle, circle, circle, semicircle1, semicircle2, quad]

    transf = [[tr.scale(2, 2, 2)]]
    transf += [[tr.translate(0, -0.05, 0), tr.scale(3/4, 1, 1), tr.scale(0.45, 0.45, 1)]]
    transf += [[tr.translate(0.15, -0.15, 0), tr.scale(3/4*0.8, 1*0.8, 1), tr.scale(0.5, 0.5, 1)]]
    transf += [[tr.translate(-0.15, -0.15, 0), tr.scale(3/4*0.8, 1*0.8, 1), tr.scale(0.5, 0.5, 1)]]
    transf += [[tr.translate(0, 0.15, 0), tr.scale(3/4*0.8, 1*0.8, 1), tr.scale(0.5, 0.5, 1)]]
    transf += [[tr.translate(0, 0.5, 0), tr.scale(3, 2, 1), tr.rotationZ(11/8*np.pi ), tr.scale(0.6, 0.6, 1)]]
    transf += [[tr.translate(0, 1.15, 0), tr.scale(0.25, 0.3, 1), tr.scale(3, 2.5, 1), tr.rotationZ(11/8*np.pi ), tr.scale(0.6, 0.6, 1)]]
    transf += [[tr.scale(0.01, 1.65, 1)]]

    return shapes, transf
 
def onClose(window):
    glfw.set_window_should_close(window, True)
        

# we will use the global controller as communication with the callback function
controller = Controller()



def main():

    # Initialize glfw
    if not glfw.init():
        return -1

    window = glfw.create_window(width, height, "Salva Pantallas DVD", None, None)

    if not window:
        glfw.terminate()
        glfw.set_window_should_close(window, True)
        return -1

    glfw.make_context_current(window)

    glfw.set_window_close_callback(window, onClose)

    # Creating our shader program and telling OpenGL to use it
    pipeline = es.SimpleTransformShaderProgram()
    
    # Le pasamos el pipeline al controlador para que inicialice el logo
    controller.createLogo("Alvaro Morales", pipeline)
    controller.setVel("AM")
    controller.setS("20265040")


    glUseProgram(pipeline.shaderProgram)

    # Setting up the clear screen color
    glClearColor(0.1, 0.1, 0.1, 1.0)

    # Convenience function to ease initialization

    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

    t0 = glfw.get_time()

    while not glfw.window_should_close(window):
        # Getting the time difference from the previous iteration
        t1 = glfw.get_time()
        dt = t1 - t0
        t0 = t1
        controller.update(dt)

        # Using GLFW to check for input events
        glfw.poll_events()

        # Clearing the screen in both, color and depth
        glClear(GL_COLOR_BUFFER_BIT)
        
        controller.draw()

        # Once the render is done, buffers are swapped, showing only the complete scene.
        glfw.swap_buffers(window)

    # freeing GPU memory
    controller.clear()

    glfw.terminate()

if __name__ == "__main__":
    
    main()