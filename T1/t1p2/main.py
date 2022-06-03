# coding=utf-8
"""
Tarea 1 Parte 2
by: Álvaro Morales
rut: 20.265.040-6

I took a lot of creative liberties but technically I did what I was asked.

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
    Shuffling x, y and z since I want +y to be UP.
    '''
    r       = rthetaphi[0]
    theta   = rthetaphi[1]
    phi     = rthetaphi[2]
    z = r * np.sin( theta ) * np.cos( phi )
    x = r * np.sin( theta ) * np.sin( phi )
    y = r * np.cos( theta )
    return np.array([x,y,z])

# Controller class
class Controller:
    def __init__(self):
        self.fillPolygon = True
        self.radius = 4.0311288741493 # i got these values with an online calculator :3
        self.theta = 82.874983651098*np.pi/180
        self.phi = 0
        self.eye = asCartesian([self.radius, self.theta, self.phi])
        self.up_phi = np.pi/2
        self.up = np.array([np.cos(self.up_phi),np.sin(self.up_phi),0])

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
    elif key == glfw.KEY_Q:
        controller.up_phi = (controller.up_phi+np.pi/90)%(2*np.pi)
        controller.up = np.array([np.cos(controller.up_phi),np.sin(controller.up_phi),0])
    elif key == glfw.KEY_E:
        controller.up_phi = (controller.up_phi-np.pi/90)%(2*np.pi)
        controller.up = np.array([np.cos(controller.up_phi),np.sin(controller.up_phi),0])
    elif key == glfw.KEY_LEFT:
        controller.phi = (controller.phi+2*np.pi/15)%(2*np.pi)
        controller.eye = asCartesian([controller.radius, controller.theta, controller.phi])
    elif key == glfw.KEY_RIGHT:
        controller.phi = (controller.phi-2*np.pi/15)%(2*np.pi)
        controller.eye = asCartesian([controller.radius, controller.theta, controller.phi])
    elif key == glfw.KEY_ESCAPE:
        glfw.set_window_should_close(window, True)
    else:
        print('Unknown key')

def main():

    window = None # Just putting this here so the next instane of window isn't underlined by vscode

    # Initialize glfw
    if not glfw.init():
        glfw.set_window_should_close(window, True)
        return
    
    window = glfw.create_window(width, height, "What Melty Blood: Type Lumina should have been", None, None)

    if not window: 
        glfw.terminate()
        glfw.set_window_should_close(window, True)
        return
    
    glfw.make_context_current(window)
    
    # Connecting the callback function 'on_key' to handle keyboard events
    glfw.set_key_callback(window, on_key)

    # Setting up the clear screen color
    glClearColor(0.25, 0.25, 0.25, 1.0)

    # SPHERE PIPELINE AND SHAPE
    spherePipeline = es.SimpleTextureModelViewProjectionShaderProgram()
<<<<<<< HEAD
    sphere = bs.createTextureSphere(10, 10)
=======
    sphere = bs.createTextureSphere(20, 20)
>>>>>>> 27bcd66a87985bce93e4aabcbe9afdd3011c6b2c
    gpuSphere = es.GPUShape().initBuffers()
    spherePipeline.setupVAO(gpuSphere)
    gpuSphere.fillBuffers(sphere.vertices, sphere.indices, GL_STATIC_DRAW)

    # BOX PIPELINE AND SHAPE
    boxPipeline = es.SimpleColorAlphaModelViewProjectionShaderProgram()
    cube = bs.createAlfaCube(1,0,0,1)
    gpuCube = es.GPUShape().initBuffers()
    boxPipeline.setupVAO(gpuCube)
    gpuCube.fillBuffers(cube.vertices, cube.indices, GL_STATIC_DRAW)

    # We're working in 3d, so we need this.
    glEnable(GL_DEPTH_TEST)

    # TRANSPARENCY!
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glAlphaFunc(GL_GREATER, 0.01)
    glEnable(GL_ALPHA_TEST)

    # Projection and view
    projection = tr.perspective(60, float(width)/float(height), 0.1, 100)
    view = tr.lookAt(
            controller.eye,
            np.array([0,0,0]),
            controller.up
        )

    # Physics
    t0 = glfw.get_time()
    L = 2.5 # cube size
    ft = L/50 # frame thickness
    r = 0.3 # sphere radius
    V = 0.4*L # 1.0
    pos1 = np.array([0,0,0.3*L])
    pos2 = np.array([0.3*L,0.1,-0.3*L])
    vel1 = np.array([np.cos(20265040)**2,0,np.sin(20265040)**2]) # pseudo random velocity
    vel2 = np.array([np.sin(20265040)**2,0,np.cos(20265040)**2])
    g = np.array([0,-9.8,0]) # gravity acceleration
    readyForCollision = True # collision with other sphere flag
    rotSpeed = 1 # rotation speed
    # MAIN LOOP
    while not glfw.window_should_close(window):
        t = glfw.get_time()
        dt = t - t0
        t0 = t
        pos1 += dt*vel1
        pos2 += dt*vel2

        # y
        if pos1[1] <= -L/2+r:
            pos1[1] = -L/2+r
            vel1[1] *= -1
        else:
            vel1 += g*dt # gravity
        if pos1[1] >= L/2-r:
            pos1[1] = L/2-r
            vel1[1] = 0
            vel1 += g*dt # gravity
        if pos2[1] <= -L/2+r:
            pos2[1] = -L/2+r
            vel2[1] *= -1
        else:
            vel2 += g*dt # gravity
        if pos2[1] >= L/2-r:
            pos2[1] = L/2-r
            vel2[1] = 0
            vel2 += g*dt # gravity
        # x
        if pos1[0] <= -L/2+r:
            pos1[0] = -L/2+r
            vel1[0] *= -1
        if pos1[0] >= L/2-r:
            pos1[0] = L/2-r
            vel1[0] *= -1
        if pos2[0] <= -L/2+r:
            pos2[0] = -L/2+r
            vel2[0] *= -1
        if pos2[0] >= L/2-r:
            pos2[0] = L/2-r
            vel2[0] *= -1
        # z
        if pos1[2] <= -L/2+r:
            pos1[2] = -L/2+r
            vel1[2] *= -1
        if pos1[2] >= L/2-r:
            pos1[2] = L/2-r
            vel1[2] *= -1
        if pos2[2] <= -L/2+r:
            pos2[2] = -L/2+r
            vel2[2] *= -1
        if pos2[2] >= L/2-r:
            pos2[2] = L/2-r
            vel2[2] *= -1
        # NECO MEETS CHAOS:
        # My attempt at collision detection between spheres
        d = 2*r - np.linalg.norm(pos1-pos2) # distance between sphere centers
        if d >= 0 and readyForCollision:
            readyForCollision = False # flag so we don't calculate this more times than necesarry
            # Solving conservation of momentum and kinetic energy
            vel1 = vel1 - np.dot(vel1-vel2,pos1-pos2)/(np.linalg.norm(pos1-pos2)**2)*(pos1-pos2)
            vel2 = vel2 - np.dot(vel2-vel1,pos2-pos1)/(np.linalg.norm(pos2-pos1)**2)*(pos2-pos1)
        if d < 0:
            readyForCollision = True

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
            controller.up
        )

        # Clearing the screen in both, color and depth
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # DRAWING THE SPHERES
        # Telling OpenGL to use our shader program
        glUseProgram(spherePipeline.shaderProgram)

        # NECO ARC
        gpuSphere.texture = es.textureSimpleSetup(
            getAssetPath("neco.png"), GL_CLAMP_TO_EDGE, GL_CLAMP_TO_EDGE, GL_LINEAR, GL_LINEAR
        )
        glUniformMatrix4fv(glGetUniformLocation(spherePipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)
        glUniformMatrix4fv(glGetUniformLocation(spherePipeline.shaderProgram, "view"), 1, GL_TRUE, view)
        glUniformMatrix4fv(glGetUniformLocation(spherePipeline.shaderProgram, "model"), 1, GL_TRUE, tr.matmul([
            tr.translate(pos1[0], pos1[1], pos1[2]),
            tr.rotationY(rotSpeed*t),         
            tr.scale(r,r,r)
        ]))

        # DRAW NECO
        spherePipeline.drawCall(gpuSphere)

        # NECO ARC CHAOS
        gpuSphere.texture = es.textureSimpleSetup(
            getAssetPath("chaos.png"), GL_CLAMP_TO_EDGE, GL_CLAMP_TO_EDGE, GL_LINEAR, GL_LINEAR
        )
        glUniformMatrix4fv(glGetUniformLocation(spherePipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)
        glUniformMatrix4fv(glGetUniformLocation(spherePipeline.shaderProgram, "view"), 1, GL_TRUE, view)
        glUniformMatrix4fv(glGetUniformLocation(spherePipeline.shaderProgram, "model"), 1, GL_TRUE, tr.matmul([
            tr.translate(pos2[0], pos2[1], pos2[2]),
            tr.rotationX(rotSpeed*t),     
            tr.scale(r,r,r)
        ]))

        # DRAW CHAOS
        spherePipeline.drawCall(gpuSphere)

        # DRAWING THE BOX
        glUseProgram(boxPipeline.shaderProgram)

        glUniformMatrix4fv(glGetUniformLocation(boxPipeline.shaderProgram, "colorScale"), 1, GL_TRUE, tr.colorScale(0.5-np.sin(2*t)/5, 1, 1, 0.05))
        glUniformMatrix4fv(glGetUniformLocation(boxPipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)
        glUniformMatrix4fv(glGetUniformLocation(boxPipeline.shaderProgram, "view"), 1, GL_TRUE, view)
        glUniformMatrix4fv(glGetUniformLocation(boxPipeline.shaderProgram, "model"), 1, GL_TRUE, tr.matmul([
            tr.translate(0.0, 0.0, 0.0),        
            tr.scale(L,L,L)
        ]))

        # DRAW GLASS BOX
        glDisable(GL_DEPTH_TEST)
        boxPipeline.drawCall(gpuCube)
        glEnable(GL_DEPTH_TEST)

        # BOX FRAME
        glUniformMatrix4fv(glGetUniformLocation(boxPipeline.shaderProgram, "colorScale"), 1, GL_TRUE, tr.colorScale(0.5-np.sin(2*t)/5, 1, 1, 1))
        glUniformMatrix4fv(glGetUniformLocation(boxPipeline.shaderProgram, "model"), 1, GL_TRUE, tr.matmul([
            tr.translate(-L/2, 0.0, -L/2),        
            tr.scale(ft,L,ft)
        ]))
        boxPipeline.drawCall(gpuCube)
        glUniformMatrix4fv(glGetUniformLocation(boxPipeline.shaderProgram, "model"), 1, GL_TRUE, tr.matmul([
            tr.translate(L/2, 0.0, -L/2),        
            tr.scale(ft,L,ft)
        ]))
        boxPipeline.drawCall(gpuCube)
        glUniformMatrix4fv(glGetUniformLocation(boxPipeline.shaderProgram, "model"), 1, GL_TRUE, tr.matmul([
            tr.translate(-L/2, 0.0, L/2),        
            tr.scale(ft,L,ft)
        ]))
        boxPipeline.drawCall(gpuCube)
        glUniformMatrix4fv(glGetUniformLocation(boxPipeline.shaderProgram, "model"), 1, GL_TRUE, tr.matmul([
            tr.translate(L/2, 0.0, L/2),        
            tr.scale(ft,L,ft)
        ]))
        boxPipeline.drawCall(gpuCube)
        # TOP
        glUniformMatrix4fv(glGetUniformLocation(boxPipeline.shaderProgram, "colorScale"), 1, GL_TRUE, tr.colorScale(0.5-np.sin(2*t)/5, 1, 1, 1))
        glUniformMatrix4fv(glGetUniformLocation(boxPipeline.shaderProgram, "model"), 1, GL_TRUE, tr.matmul([
            tr.translate(-L/2, L/2, 0.0),   
            tr.rotationX(np.pi/2),     
            tr.scale(ft,L,ft)
        ]))
        boxPipeline.drawCall(gpuCube)
        glUniformMatrix4fv(glGetUniformLocation(boxPipeline.shaderProgram, "model"), 1, GL_TRUE, tr.matmul([
            tr.translate(L/2, L/2, 0.0),
            tr.rotationX(np.pi/2),       
            tr.scale(ft,L,ft)
        ]))
        boxPipeline.drawCall(gpuCube)
        glUniformMatrix4fv(glGetUniformLocation(boxPipeline.shaderProgram, "model"), 1, GL_TRUE, tr.matmul([
            tr.translate(0.0, L/2, -L/2),
            tr.rotationZ(np.pi/2),       
            tr.scale(ft,L,ft)
        ]))
        boxPipeline.drawCall(gpuCube)
        glUniformMatrix4fv(glGetUniformLocation(boxPipeline.shaderProgram, "model"), 1, GL_TRUE, tr.matmul([
            tr.translate(0.0, L/2, L/2),
            tr.rotationZ(np.pi/2),       
            tr.scale(ft,L,ft)
        ]))
        boxPipeline.drawCall(gpuCube)
        # BOTTOM
        glUniformMatrix4fv(glGetUniformLocation(boxPipeline.shaderProgram, "colorScale"), 1, GL_TRUE, tr.colorScale(0.5-np.sin(2*t)/5, 1, 1, 1))
        glUniformMatrix4fv(glGetUniformLocation(boxPipeline.shaderProgram, "model"), 1, GL_TRUE, tr.matmul([
            tr.translate(-L/2, -L/2, 0.0),   
            tr.rotationX(np.pi/2),     
            tr.scale(ft,L,ft)
        ]))
        boxPipeline.drawCall(gpuCube)
        glUniformMatrix4fv(glGetUniformLocation(boxPipeline.shaderProgram, "model"), 1, GL_TRUE, tr.matmul([
            tr.translate(L/2, -L/2, 0.0),
            tr.rotationX(np.pi/2),       
            tr.scale(ft,L,ft)
        ]))
        boxPipeline.drawCall(gpuCube)
        glUniformMatrix4fv(glGetUniformLocation(boxPipeline.shaderProgram, "model"), 1, GL_TRUE, tr.matmul([
            tr.translate(0.0, -L/2, -L/2),
            tr.rotationZ(np.pi/2),       
            tr.scale(ft,L,ft)
        ]))
        boxPipeline.drawCall(gpuCube)
        glUniformMatrix4fv(glGetUniformLocation(boxPipeline.shaderProgram, "model"), 1, GL_TRUE, tr.matmul([
            tr.translate(0.0, -L/2, L/2),
            tr.rotationZ(np.pi/2),       
            tr.scale(ft,L,ft)
        ]))
        boxPipeline.drawCall(gpuCube)

        # Once the render is done, buffers are swapped, showing only the complete scene.
        glfw.swap_buffers(window)
    
    # freeing GPU memory
    gpuSphere.clear()
    gpuCube.clear()

    glfw.terminate()

if __name__ == "__main__":
    main()

