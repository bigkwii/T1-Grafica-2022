'''
T2 p1
by: Álvaro Morales
rut: 20.265.040-6
map chosen: 1

Wish I could've done something with more detail or found a way to make it run better, but I'm seriously out of time.
So instead, I made a game out of it.
There are 4 Poorly made Neco Arcs hidden in the map.
Yeah, I made the model really fast and messed up the indices, but I don't have time to fix it.

Find them all to win! :3

CONTROLS:
    -WASD TO MOVE
    -SHIFT TO GO UP, CTRL TO GO DOWN
    -ARROWS TO LOOK AROUND
    -SPACE TOGGLES BIRD'S EYE VIEW
    -ALT TOGGLES WIREFRAME MODE
'''
import glfw
from OpenGL.GL import *
import numpy as np
import sys
import os.path

from soupsieve import match
from sqlalchemy import true
from libs.setup import setView, setPlot, createMinecraftBlock
import libs.transformations as tr
import libs.basic_shapes as bs
import libs.easy_shaders as es
import libs.scene_graph as sg
import libs.performance_monitor as pm
from libs.assets_path import getAssetPath
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import libs.neco_arc as neco

__author__ = "Álvaro Morales"
__license__ = "MIT"

width = 896
height = 504
try:
    assert(width/height == 16/9)
except:
    print("Resolution must be 16:9")
    exit()

# A class to store the application control
class Controller:
    def __init__(self):
        self.fillPolygon = True
        self.cameraMovementSpeed = 0.05#0.01
        self.closestPoint = 5
        self.furthestPoint = 13
        self.radialMovementSpeed = 0.04#0.02
        self.axesOn = False

        self.camPos = np.array([-5, -0.5, 8], dtype=np.float64)
        self.camForward = np.array([0, 0, -1], dtype=np.float64)
        self.camUp = np.array([0, 1, 0], dtype=np.float64)
        self.camRight = np.array([1, 0, 0], dtype=np.float64)
        self.camPhi = 0
        self.camTheta = 0
        self.maxCamTheta = np.pi/2-0.1
        self.minCamTheta = -np.pi/2+0.1
        self.camPointTo = np.array([np.cos(self.camPhi)*np.cos(self.camTheta),np.sin(self.camTheta),np.sin(self.camPhi)*np.cos(self.camTheta)],dtype=np.float64)

        self.camOrtho = False

        self.neco1Pos = np.array([ 3.71705596, -0.6, 8.13025371])
        self.neco2Pos = np.array([ 4.32789124, -0.56528538, -4.78915696])
        self.neco3Pos = np.array([-0.02005537, 2.36978355, -3.11630724])
        self.neco4Pos = np.array([ 2.37716548, -0.43418735, -8.44371672])

        self.neco1Found = False
        self.neco2Found = False
        self.neco3Found = False
        self.neco4Found = False

        self.necoCounter = 0

        self.necoSpeed = 5

        self.neco1Rot = np.pi
        self.neco2Rot = 0
        self.neco3Rot = -np.pi/2
        self.neco4Rot = np.pi

        self.win = False

        self.t = 0
        self.dt = 0
    
    def closeEnoughToNeco(self, necoPos):
        return np.linalg.norm(self.camPos-necoPos) < 0.5

    def updateStuff(self):
        self.camPhi = self.camPhi % (2*np.pi)
        self.camPointTo = np.array([np.cos(self.camPhi)*np.cos(self.camTheta),np.sin(self.camTheta),np.sin(self.camPhi)*np.cos(self.camTheta)],dtype=np.float64)
        self.camForward = self.camPointTo/np.linalg.norm(self.camPointTo)
        if self.camPos[0] > 5: self.camPos[0] = 5
        if self.camPos[0] < -5: self.camPos[0] = -5
        if self.camPos[1] > 4: self.camPos[1] = 4
        if self.camPos[1] < -0.8: self.camPos[1] = -0.8
        if self.camPos[2] > 10: self.camPos[2] = 10
        if self.camPos[2] < -10: self.camPos[2] = -10

        # Finding necos
        if self.closeEnoughToNeco(self.neco1Pos) and not self.neco1Found:
            self.neco1Found = True
            self.necoCounter += 1
            print("Neco 1 found!")
        if self.closeEnoughToNeco(self.neco2Pos) and not self.neco2Found:
            self.neco2Found = True
            self.necoCounter += 1
            print("Neco 2 found!")
        if self.closeEnoughToNeco(self.neco3Pos) and not self.neco3Found:
            self.neco3Found = True
            self.necoCounter += 1
            print("Neco 3 found!")
        if self.closeEnoughToNeco(self.neco4Pos) and not self.neco4Found:
            self.neco4Found = True
            self.necoCounter += 1
            print("Neco 4 found!")
        if self.neco1Found and self.neco2Found and self.neco3Found and self.neco4Found and not self.win:
            self.win = True
            print("All necos Found, You won! :3")
        
        # Spinning necos (Couldn't figure it out)
        # if self.neco1Found:
        #     self.neco1Rot += self.necoSpeed*self.dt
        # if self.neco2Found:
        #     self.neco2Rot += self.necoSpeed*self.dt
        # if self.neco3Found:
        #     self.neco3Rot += self.necoSpeed*self.dt
        # if self.neco4Found:
        #     self.neco4Rot += self.necoSpeed*self.dt
        


# global controller as communication with the callback function
controller = Controller()

def on_key(window, key, scancode, action, mods):

    if action != glfw.PRESS:
        return

    global controller

    # Camera position
    if key == glfw.KEY_W:
        controller.camPos += controller.cameraMovementSpeed*controller.camForward

    elif key == glfw.KEY_S:
        controller.camPos -= controller.cameraMovementSpeed*controller.camForward

    elif key == glfw.KEY_A:
        controller.camPos -= controller.cameraMovementSpeed*(np.cross(controller.camForward,controller.camUp)/np.linalg.norm(np.cross(controller.camForward,controller.camUp)))

    elif key == glfw.KEY_D:
        controller.camPos += controller.cameraMovementSpeed*(np.cross(controller.camForward,controller.camUp)/np.linalg.norm(np.cross(controller.camForward,controller.camUp)))

    elif key == glfw.KEY_LEFT_CONTROL:
        controller.camPos[1] -= controller.cameraMovementSpeed

    elif key == glfw.KEY_LEFT_SHIFT:
        controller.camPos[1] += controller.cameraMovementSpeed

    # Camera orientation
    elif key == glfw.KEY_UP:
        if controller.camTheta < controller.maxCamTheta:
            controller.camTheta += controller.radialMovementSpeed

    elif key == glfw.KEY_DOWN:
        if controller.camTheta > controller.minCamTheta:
            controller.camTheta -= controller.radialMovementSpeed

    elif key == glfw.KEY_LEFT:
        controller.camPhi -= controller.radialMovementSpeed

    elif key == glfw.KEY_RIGHT:
        controller.camPhi += controller.radialMovementSpeed

    # Activar/Desactivar ejes
    elif key == glfw.KEY_Q:
        controller.axesOn = not controller.axesOn

    elif key == glfw.KEY_LEFT_ALT:
        controller.fillPolygon = not controller.fillPolygon

    elif key == glfw.KEY_SPACE:
        controller.camOrtho = not controller.camOrtho

    elif key == glfw.KEY_ESCAPE:
        glfw.set_window_should_close(window, True)

    elif key == glfw.KEY_P:
        print(controller.camPos)

    else:
        print("key not defined")

def check_key_inputs(window):

    # Camera position
    if glfw.get_key(window, glfw.KEY_W) == glfw.PRESS:
        controller.camPos += controller.cameraMovementSpeed*controller.camForward

    elif glfw.get_key(window, glfw.KEY_S) == glfw.PRESS:
        controller.camPos -= controller.cameraMovementSpeed*controller.camForward

    if glfw.get_key(window, glfw.KEY_A) == glfw.PRESS:
        controller.camPos -= controller.cameraMovementSpeed*(np.cross(controller.camForward,controller.camUp)/np.linalg.norm(np.cross(controller.camForward,controller.camUp)))

    elif glfw.get_key(window, glfw.KEY_D) == glfw.PRESS:
        controller.camPos += controller.cameraMovementSpeed*(np.cross(controller.camForward,controller.camUp)/np.linalg.norm(np.cross(controller.camForward,controller.camUp)))

    if glfw.get_key(window, glfw.KEY_LEFT_CONTROL) == glfw.PRESS:
        controller.camPos[1] -= controller.cameraMovementSpeed

    elif glfw.get_key(window, glfw.KEY_LEFT_SHIFT) == glfw.PRESS:
        controller.camPos[1] += controller.cameraMovementSpeed

    # Camera orientation
    if glfw.get_key(window, glfw.KEY_UP) == glfw.PRESS:
        if controller.camTheta < controller.maxCamTheta:
            controller.camTheta += controller.radialMovementSpeed

    elif glfw.get_key(window, glfw.KEY_DOWN) == glfw.PRESS:
        if controller.camTheta > controller.minCamTheta:
            controller.camTheta -= controller.radialMovementSpeed
    
    if glfw.get_key(window, glfw.KEY_LEFT) == glfw.PRESS:
        controller.camPhi -= controller.radialMovementSpeed

    elif glfw.get_key(window, glfw.KEY_RIGHT) == glfw.PRESS:
        controller.camPhi += controller.radialMovementSpeed

def createScene(pipeline, pipelineForNecos):
    '''
    Here we go baby.
    '''
    # ---CREATING SHAPES IN GPU MEMORY---
    # CREATE FLOOR
    shapeFloor = bs.createTextureCube()
    gpuFloor = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuFloor)
    gpuFloor.fillBuffers(
        shapeFloor.vertices, shapeFloor.indices, GL_STATIC_DRAW
    )
    gpuFloor.texture = es.textureSimpleSetup(
        getAssetPath("floor.png"), GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR
    )
    # CREATE LEAF SPHERE
    shapeLeaf = bs.createTextureSphere()
    gpuLeaf = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuLeaf)
    gpuLeaf.fillBuffers(
        shapeLeaf.vertices, shapeLeaf.indices, GL_STATIC_DRAW
    )
    gpuLeaf.texture = es.textureSimpleSetup(
        getAssetPath("terrible_leafs.png"), GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR
    )
    # CREATE LOG
    shapeLog = createMinecraftBlock()
    gpuLog = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuLog)
    gpuLog.fillBuffers(
        shapeLog.vertices, shapeLog.indices, GL_STATIC_DRAW
    )
    gpuLog.texture = es.textureSimpleSetup(
        getAssetPath("log.png"), GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR
    )
    # CREATE DOOR
    shapeDoor = createMinecraftBlock()
    gpuDoor = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuDoor)
    gpuDoor.fillBuffers(
        shapeDoor.vertices, shapeDoor.indices, GL_STATIC_DRAW
    )
    gpuDoor.texture = es.textureSimpleSetup(
        getAssetPath("terrible_door.png"), GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR
    )
    # CREATE WINDOW
    shapeWindow = createMinecraftBlock()
    gpuWindow = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuWindow)
    gpuWindow.fillBuffers(
        shapeWindow.vertices, shapeWindow.indices, GL_STATIC_DRAW
    )
    gpuWindow.texture = es.textureSimpleSetup(
        getAssetPath("terrible_window.png"), GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR
    )
    # CREATE BOTTOM HOUSE
    shapeBottomHouse = createMinecraftBlock()
    gpuBottomHouse = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuBottomHouse)
    gpuBottomHouse.fillBuffers(
        shapeBottomHouse.vertices, shapeBottomHouse.indices, GL_STATIC_DRAW
    )
    gpuBottomHouse.texture = es.textureSimpleSetup(
        getAssetPath("bottom_floor.png"), GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR
    )
    # CREATE TOP HOUSE
    shapeTopHouse = createMinecraftBlock()
    gpuTopHouse = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuTopHouse)
    gpuTopHouse.fillBuffers(
        shapeTopHouse.vertices, shapeTopHouse.indices, GL_STATIC_DRAW
    )
    gpuTopHouse.texture = es.textureSimpleSetup(
        getAssetPath("top_floor.png"), GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR
    )


    # ---MAKING THE SCENE GRAPH---

    # TREE
    trueLog = sg.SceneGraphNode('True Log')
    trueLog.transform = tr.matmul([tr.scale(0.2, 2, 0.2)])
    trueLog.childs += [gpuLog]

    leaf1 = sg.SceneGraphNode('Leaf 1')
    leaf1.transform = tr.matmul([tr.translate(-0.2, 0.2, -0.1), tr.scale(0.5, 0.5, 0.5)])
    leaf1.childs += [gpuLeaf]
    leaf2 = sg.SceneGraphNode('Leaf 1')
    leaf2.transform = tr.matmul([tr.translate(0.4, 0.3, 0), tr.scale(0.5, 0.5, 0.5)])
    leaf2.childs += [gpuLeaf]
    leaf3 = sg.SceneGraphNode('Leaf 1')
    leaf3.transform = tr.matmul([tr.translate(-0.3, 0.8, 0.2), tr.scale(0.5, 0.5, 0.5)])
    leaf3.childs += [gpuLeaf]
    leaf4 = sg.SceneGraphNode('Leaf 1')
    leaf4.transform = tr.matmul([tr.translate(0.05, 1.1, -0.05), tr.scale(0.5, 0.5, 0.5)])
    leaf4.childs += [gpuLeaf]

    tree = sg.SceneGraphNode('Tree')
    tree.childs += [trueLog, leaf1, leaf2, leaf3, leaf4]

    # trees
    tree1 = sg.SceneGraphNode('Tree 1')
    tree1.transform = tr.matmul([tr.translate(2, 0, 5), tr.scale(0.9, 1.1, 0.9)])
    tree1.childs += [tree]
    tree2 = sg.SceneGraphNode('Tree 2')
    tree2.transform = tr.matmul([tr.translate(3, 0, 4), tr.scale(1.1, 1.1, 1.1)])
    tree2.childs += [tree]
    tree3 = sg.SceneGraphNode('Tree 3')
    tree3.transform = tr.matmul([tr.translate(4, 0, 5.5), tr.scale(0.9, 1.1, 0.9)])
    tree3.childs += [tree]
    tree4 = sg.SceneGraphNode('Tree 4')
    tree4.transform = tr.matmul([tr.translate(2.5, 0, 8), tr.scale(0.9, 1.5, 0.9)])
    tree4.childs += [tree]
    tree5 = sg.SceneGraphNode('Tree 5')
    tree5.transform = tr.matmul([tr.translate(4, 0, 6.5), tr.scale(0.9, 1.1, 0.9)])
    tree5.childs += [tree]
    tree6 = sg.SceneGraphNode('Tree 6')
    tree6.transform = tr.matmul([tr.translate(2, 0, 7), tr.scale(0.9, 1.1, 0.9)])
    tree6.childs += [tree]

    # forest1
    forest1 = sg.SceneGraphNode('Forest1')
    forest1.childs += [tree1, tree2,tree3, tree4, tree5, tree6]
    # forest2
    forest2 = sg.SceneGraphNode('Forest2')
    forest2.transform = tr.matmul([tr.translate(8, 0, 4), tr.rotationY(-np.pi/2.1)])
    forest2.childs += [forest1]

    # lone tree
    loneTree = sg.SceneGraphNode('Lone Tree')
    loneTree.transform = tr.matmul([tr.translate(4, 0, -4), tr.scale(0.9, 1.3, 0.9)])
    loneTree.childs += [tree]

    # all trees
    allTrees = sg.SceneGraphNode('All Trees')
    allTrees.childs += [forest1, forest2, loneTree]

    # door (points north)
    door = sg.SceneGraphNode('Door')
    door.transform = tr.matmul([tr.translate(0,-0.5,0), tr.scale(0.05, 0.9, 0.4)])
    door.childs += [gpuDoor]

    # window (points north)
    window = sg.SceneGraphNode('Window')
    window.transform = tr.matmul([tr.translate(0,-0.7,0), tr.scale(0.05, 0.5, 0.5)])
    window.childs += [gpuWindow]

    # bottom block
    bottomBlock = sg.SceneGraphNode('Bottom Block')
    bottomBlock.transform = tr.matmul([tr.translate(0,0,0), tr.scale(1, 1, 1)])
    bottomBlock.childs += [gpuBottomHouse]

    # top block
    topBlock = sg.SceneGraphNode('Top Block')
    topBlock.transform = tr.matmul([tr.translate(0,0,0), tr.scale(1, 1, 1)])
    topBlock.childs += [gpuTopHouse]

    # window facing north
    windowNorth = sg.SceneGraphNode('Window North')
    windowNorth.transform = tr.matmul([tr.translate(-0.5,0.7,0), tr.rotationY(0)])
    windowNorth.childs += [window]

    # window facing south
    windowSouth = sg.SceneGraphNode('Window South')
    windowSouth.transform = tr.matmul([tr.translate(0.5,0.7,0), tr.rotationY(np.pi)])
    windowSouth.childs += [window]

    # window facing east
    windowEast = sg.SceneGraphNode('Window East')
    windowEast.transform = tr.matmul([tr.translate(0,0.7,0.5), tr.rotationY(np.pi/2)])
    windowEast.childs += [window]

    # window facing west
    windowWest = sg.SceneGraphNode('Window West')
    windowWest.transform = tr.matmul([tr.translate(0,0.7,-0.5), tr.rotationY(-np.pi/2)])
    windowWest.childs += [window]

    # 3 windows
    windows3 = sg.SceneGraphNode('Windows 3')
    windows3.transform = tr.matmul([tr.translate(0,0,0)])
    windows3.childs += [windowSouth, windowEast, windowWest]

    # 4 windows
    windows4 = sg.SceneGraphNode('Windows 4')
    windows4.transform = tr.matmul([tr.translate(0,0,0)])
    windows4.childs += [windowNorth, windowSouth, windowEast, windowWest]

    # entrance door
    entranceDoor = sg.SceneGraphNode('Entrance Door')
    entranceDoor.transform = tr.matmul([tr.translate(-0.5,0.2,0), tr.uniformScale(0.75)])
    entranceDoor.childs += [door]

    # first floor
    firstFloor = sg.SceneGraphNode('First Floor')
    firstFloor.childs += [bottomBlock, entranceDoor, windows3]

    # middle floor
    middleFloor = sg.SceneGraphNode('Middle Floor')
    middleFloor.childs += [bottomBlock, windows4]

    # top floor
    topFloor = sg.SceneGraphNode('Top Floor')
    topFloor.childs += [topBlock, windows4]

    # One story house
    oneStoryHouse = sg.SceneGraphNode('One Story House')
    oneStoryHouse.childs += [topBlock, entranceDoor, windows3]

    # Middle floor Up by 1
    middleFloorUpBy1 = sg.SceneGraphNode('Middle Floor Up')
    middleFloorUpBy1.transform = tr.matmul([tr.translate(0,1,0)])
    middleFloorUpBy1.childs += [middleFloor]

    # Top Floor Up by 1
    topFloorUpBy1 = sg.SceneGraphNode('Top Floor Up')
    topFloorUpBy1.transform = tr.matmul([tr.translate(0,1,0)])
    topFloorUpBy1.childs += [topFloor]

    # Top Floor Up by 2
    topFloorUpBy2 = sg.SceneGraphNode('Top Floor Up')
    topFloorUpBy2.transform = tr.matmul([tr.translate(0,2,0)])
    topFloorUpBy2.childs += [topFloor]

    # Two story house
    twoStoryHouse = sg.SceneGraphNode('Two Story House')
    twoStoryHouse.childs += [firstFloor, topFloorUpBy1]

    # Three story house
    threeStoryHouse = sg.SceneGraphNode('Three Story House')
    threeStoryHouse.childs += [firstFloor, middleFloorUpBy1, topFloorUpBy2]

    # Hell
    # house1
    house1 = sg.SceneGraphNode('House1')
    house1.transform = tr.matmul([tr.translate(-3.75,-0.5,7.25), tr.scale(1, 1, 1), tr.rotationY(0)])
    house1.childs += [oneStoryHouse]

    #house 2
    house2 = sg.SceneGraphNode('House2')
    house2.transform = tr.matmul([tr.translate(-3.25,-0.5,6.25), tr.scale(1.5, 1, 0.75), tr.rotationY(0)])
    house2.childs += [oneStoryHouse]

    #house 3
    house3 = sg.SceneGraphNode('House3')
    house3.transform = tr.matmul([tr.translate(-3.5,-0.5,4.8), tr.scale(1.3, 1, 1.3), tr.rotationY(0)])
    house3.childs += [oneStoryHouse]

    #house 4
    house4 = sg.SceneGraphNode('House4')
    house4.transform = tr.matmul([tr.translate(-3.3,-0.5,3.65), tr.scale(1.7, 1, 1), tr.rotationY(0)])
    house4.childs += [oneStoryHouse]

    #house 5
    house5 = sg.SceneGraphNode('House5')
    house5.transform = tr.matmul([tr.translate(-3.3,-0.5,2.6), tr.scale(1.8, 1, 0.9), tr.rotationY(0)])
    house5.childs += [oneStoryHouse]

    #house 6
    house6 = sg.SceneGraphNode('House6')
    house6.transform = tr.matmul([tr.translate(-2.6,-0.5,1.2), tr.scale(2, 1, 1.6), tr.rotationY(0)])
    house6.childs += [twoStoryHouse]

    #house 7
    house7 = sg.SceneGraphNode('House7')
    house7.transform = tr.matmul([tr.translate(-3.5,-0.5,-1.25), tr.scale(1.5, 1, 1.6), tr.rotationY(0)])
    house7.childs += [twoStoryHouse]

    #house 8
    house8 = sg.SceneGraphNode('House8')
    house8.transform = tr.matmul([tr.translate(-2.5,-0.5,-3), tr.scale(2.2, 1, 1.4), tr.rotationY(0)])
    house8.childs += [twoStoryHouse]

    #house 9
    house9 = sg.SceneGraphNode('House9')
    house9.transform = tr.matmul([tr.translate(-3.2,-0.5,-5.2), tr.scale(1.5, 1, 1.5), tr.rotationY(0)])
    house9.childs += [twoStoryHouse]

    #house 10
    house10 = sg.SceneGraphNode('House10')
    house10.transform = tr.matmul([tr.translate(-2.25,-0.5,-6.8), tr.scale(1.8, 1, 1.5), tr.rotationY(0)])
    house10.childs += [twoStoryHouse]

    #house 11
    house11 = sg.SceneGraphNode('House11')
    house11.transform = tr.matmul([tr.translate(-3.75,-0.5,-7), tr.scale(0.75, 1, 0.75), tr.rotationY(0)])
    house11.childs += [oneStoryHouse]

    #house 12
    house12 = sg.SceneGraphNode('House12')
    house12.transform = tr.matmul([tr.translate(-3,-0.5,-7.8), tr.scale(3, 1, 0.6), tr.rotationY(0)])
    house12.childs += [oneStoryHouse]

    #house 13
    house13 = sg.SceneGraphNode('House13')
    house13.transform = tr.matmul([tr.translate(-3.3,-0.5,-8.8), tr.scale(1.3, 1, 1.3), tr.rotationY(-np.pi/2)])
    house13.childs += [twoStoryHouse]

    #house 14
    house14 = sg.SceneGraphNode('House14')
    house14.transform = tr.matmul([tr.translate(-1.5,-0.5,-9), tr.scale(1.4, 1, 1.4), tr.rotationY(-np.pi/2)])
    house14.childs += [twoStoryHouse]

    #house 15
    house15 = sg.SceneGraphNode('House15')
    house15.transform = tr.matmul([tr.translate(0.2,-0.5,-9.1), tr.scale(1.5, 1, 1.5), tr.rotationY(-np.pi/2)])
    house15.childs += [twoStoryHouse]

    #house 16
    house16 = sg.SceneGraphNode('House16')
    house16.transform = tr.matmul([tr.translate(2.5,-0.5,-8.9), tr.scale(1.7, 1, 1.7), tr.rotationY(-np.pi/2)])
    house16.childs += [twoStoryHouse]

    #house 17
    house17 = sg.SceneGraphNode('House17')
    house17.transform = tr.matmul([tr.translate(3,-0.5,-7), tr.scale(1.5, 1, 1.5), tr.rotationY(np.pi)])
    house17.childs += [oneStoryHouse]

    #house 18
    house18 = sg.SceneGraphNode('House18')
    house18.transform = tr.matmul([tr.translate(2.5,-0.5,-5.1), tr.scale(1.8, 1, 1.8), tr.rotationY(np.pi)])
    house18.childs += [oneStoryHouse]

    #house 19
    house19 = sg.SceneGraphNode('House19')
    house19.transform = tr.matmul([tr.translate(3,-0.5,-1), tr.scale(2.1, 1, 2.1), tr.rotationY(np.pi)])
    house19.childs += [oneStoryHouse]

    #house 20
    house20 = sg.SceneGraphNode('House20')
    house20.transform = tr.matmul([tr.translate(0,-0.5,1.2), tr.scale(1.8, 1, 1.8), tr.rotationY(np.pi)])
    house20.childs += [twoStoryHouse]

    #house 21
    house21 = sg.SceneGraphNode('House21')
    house21.transform = tr.matmul([tr.translate(1.2,-0.5,0.2), tr.scale(0.75, 1, 0.75), tr.rotationY(np.pi)])
    house21.childs += [oneStoryHouse]

    #house 22
    house22 = sg.SceneGraphNode('House22')
    house22.transform = tr.matmul([tr.translate(-1,-0.5,3), tr.scale(1.6, 1, 1.6), tr.rotationY(np.pi)])
    house22.childs += [twoStoryHouse]

    #house 23
    house23 = sg.SceneGraphNode('House23')
    house23.transform = tr.matmul([tr.translate(-2.1,-0.5,4.9), tr.scale(1, 1, 1.5), tr.rotationY(np.pi)])
    house23.childs += [oneStoryHouse]

    #house 24
    house24 = sg.SceneGraphNode('House24')
    house24.transform = tr.matmul([tr.translate(-0.1,-0.5,-1.3), tr.scale(1.8, 1, 1.8), tr.rotationY(np.pi)])
    house24.childs += [threeStoryHouse]

    #house 25
    house25 = sg.SceneGraphNode('House25')
    house25.transform = tr.matmul([tr.translate(0.1,-0.5,-3.2), tr.scale(2, 1, 1.5), tr.rotationY(np.pi)])
    house25.childs += [threeStoryHouse]

    #house 26
    house26 = sg.SceneGraphNode('House26')
    house26.transform = tr.matmul([tr.translate(-0.5,-0.5,-4.5), tr.scale(1.6, 1, 0.8), tr.rotationY(np.pi)])
    house26.childs += [threeStoryHouse]

    #house 27
    house27 = sg.SceneGraphNode('House27')
    house27.transform = tr.matmul([tr.translate(-0.3,-0.5,-5.5), tr.scale(1.8, 1, 1), tr.rotationY(np.pi)])
    house27.childs += [threeStoryHouse]

    #house 28
    house28 = sg.SceneGraphNode('House28')
    house28.transform = tr.matmul([tr.translate(1,-0.5,-7), tr.scale(1.8, 1, 1.8), tr.rotationY(np.pi)])
    house28.childs += [threeStoryHouse]

    # Lone House
    loneHouse = sg.SceneGraphNode('LoneHouse')
    loneHouse.transform = tr.matmul([tr.translate(-0.5,-0.5,7), tr.rotationY(-np.pi/6), tr.scale(1.5, 1, 2)])
    loneHouse.childs += [oneStoryHouse]

    # All houses
    allHouses = sg.SceneGraphNode('All Houses')
    allHouses.childs += [house1, house2, house3, house4, house5, house6, house7, house8, house9, house10, house11, house12, house13, house14, house15,
                         house16, house17, house18, house19, house20, house21, house22, house23, house24, house25, house26, house27, house28, loneHouse]

    # SCENE GRAPH ROOT NODE
    scene = sg.SceneGraphNode('system')

    # FLOOR NODE
    floor = sg.SceneGraphNode('floor')
    floor.transform = tr.matmul([tr.translate(0,-1,0),tr.rotationY(-np.pi/2),tr.scale(-20,0.1,10)])
    floor.childs += [gpuFloor]

    
    scene.childs += [floor, allTrees, allHouses]
    

    # ---NECO ARC HUNT---
    # BASE NECO
    base_neco = neco.createNecoArcNode(pipelineForNecos, "base_neco")

    #NECOS 1-4
    neco1 = sg.SceneGraphNode('neco1')
    neco1.transform = tr.matmul([tr.translate(
        controller.neco1Pos[0], controller.neco1Pos[1], controller.neco1Pos[2]
        ),tr.rotationY(controller.neco1Rot),tr.scale(0.5,0.5,0.5)])
    neco1.childs += [base_neco]
    neco2 = sg.SceneGraphNode('neco2')
    neco2.transform = tr.matmul([tr.translate(
        controller.neco2Pos[0], controller.neco2Pos[1], controller.neco2Pos[2]
        ),tr.rotationY(controller.neco2Rot),tr.scale(0.5,0.5,0.5)])
    neco2.childs += [base_neco]
    neco3 = sg.SceneGraphNode('neco3')
    neco3.transform = tr.matmul([tr.translate(
        controller.neco3Pos[0], controller.neco3Pos[1], controller.neco3Pos[2]
        ),tr.rotationY(controller.neco3Rot),tr.scale(0.5,0.5,0.5)])
    neco3.childs += [base_neco]
    neco4 = sg.SceneGraphNode('neco4')
    neco4.transform = tr.matmul([tr.translate(
        controller.neco4Pos[0], controller.neco4Pos[1], controller.neco4Pos[2]
        ),tr.rotationY(controller.neco4Rot),tr.scale(0.5,0.5,0.5)])
    neco4.childs += [base_neco]

    hidden_necos = sg.SceneGraphNode('hidden_necos')
    hidden_necos.childs += [neco1, neco2, neco3, neco4]

    return scene , hidden_necos



def main():
    # Initialize glfw
    if not glfw.init():
        glfw.set_window_should_close(window, True)

    title = "Find the 4 hidden Neco Arcs!"

    window = glfw.create_window(width, height, title, None, None)

    if not window:
        glfw.terminate()
        glfw.set_window_should_close(window, True)

    glfw.make_context_current(window)

    # Connecting the callback function 'on_key' to handle keyboard events
    glfw.set_key_callback(window, on_key)

    # Creating shader programs for textures and for colors
    textureShaderProgram = es.SimpleTextureModelViewProjectionShaderProgram()
    colorShaderProgram = es.SimpleModelViewProjectionShaderProgram()

    # Setting up the clear screen color
    glClearColor(0.85, 0.85, 0.85, 1.0)

    # As we work in 3D, we need to check which part is in front,
    # and which one is at the back
    glEnable(GL_DEPTH_TEST)

    cpuAxis = bs.createAxis(2)
    gpuAxis = es.GPUShape().initBuffers()
    colorShaderProgram.setupVAO(gpuAxis)
    gpuAxis.fillBuffers(cpuAxis.vertices, cpuAxis.indices, GL_STATIC_DRAW)

    dibujo = createScene(textureShaderProgram, colorShaderProgram)[0]
    dibujo_necos = createScene(textureShaderProgram, colorShaderProgram)[1]

    setPlot(textureShaderProgram, colorShaderProgram, width, height)

    perfMonitor = pm.PerformanceMonitor(glfw.get_time(), 0.5)

    controller.t = glfw.get_time()
    while not glfw.window_should_close(window):
        controller.dt = glfw.get_time() - controller.t
        controller.t = glfw.get_time()

        # Measuring performance
        perfMonitor.update(glfw.get_time())
        
        if controller.necoCounter == 0: title = "Find the 4 hidden Neco Arcs!"
        if controller.necoCounter == 1: title = "3 More Necos to go!"
        if controller.necoCounter == 2: title = "2 More! Nya!"
        if controller.necoCounter == 3: title = "Last One! Doridoridori!"
        if controller.necoCounter == 4: title = "YOU WIN!"
        
        glfw.set_window_title(window, title + str(perfMonitor))

        # Using GLFW to check for input events
        glfw.poll_events()

        check_key_inputs(window)

        # Updating the thetas and phis
        controller.updateStuff()

        # Filling or not the shapes depending on the controller state
        if (controller.fillPolygon):
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        else:
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

        setView(textureShaderProgram, colorShaderProgram, controller)

        # Clearing the screen in both, color and depth
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        if (controller.axesOn):
            # Drawing axes (no texture)
            glUseProgram(colorShaderProgram.shaderProgram)
            glUniformMatrix4fv(glGetUniformLocation(
                colorShaderProgram.shaderProgram, "model"), 1, GL_TRUE, tr.identity())
            colorShaderProgram.drawCall(gpuAxis, GL_LINES)

        # Since we're mixing pipelines, let's just cheat!
        
        glUseProgram(textureShaderProgram.shaderProgram)
        sg.drawSceneGraphNode(dibujo, textureShaderProgram, "model")
        
        glUseProgram(colorShaderProgram.shaderProgram)
        sg.drawSceneGraphNode(dibujo_necos, colorShaderProgram, "model")

        # Once the drawing is rendered, buffers are swap so an uncomplete drawing is never seen.
        glfw.swap_buffers(window)

    # freeing GPU memory
    gpuAxis.clear()
    dibujo.clear()

    glfw.terminate()

    return 0


if __name__ == "__main__":
    main()
