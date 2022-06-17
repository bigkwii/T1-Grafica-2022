# coding=utf-8
"""Tarea 2"""
"""
Nombre: Álvaro Morales T.
RUT: 20.265.040-6

Escogí la BICICLETA #30
"""

import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy as np
import sys
import os.path

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import libs.transformations as tr
import libs.basic_shapes as bs
import libs.scene_graph as sg
import libs.easy_shaders as es
import libs.performance_monitor as pm



def createNecoArcNode(pipeline, name):
    '''
    bura nyaaaaaaaaaaa
    '''
    assert(isinstance(pipeline, es.SimpleModelViewProjectionShaderProgram))

    white_cylinder = bs.createColorCylinder(1,1,1)
    gpuWhiteCylinder = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuWhiteCylinder)
    gpuWhiteCylinder.fillBuffers(
        white_cylinder.vertices, white_cylinder.indices, GL_STATIC_DRAW
    )

    dress_cone = bs.createColorCone(0.388235, 0.0, 0.1294117)
    gpuDressCone = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuDressCone)
    gpuDressCone.fillBuffers(
        dress_cone.vertices, dress_cone.indices, GL_STATIC_DRAW
    )

    white_sphere = bs.createColorSphere(1,1,1)
    gpuWhiteSphere = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuWhiteSphere)
    gpuWhiteSphere.fillBuffers(
        white_sphere.vertices, white_sphere.indices, GL_STATIC_DRAW
    )

    tan_sphere = bs.createColorSphere(255/255, 211/255, 158/255)
    gpuTanSphere = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuTanSphere)
    gpuTanSphere.fillBuffers(
        tan_sphere.vertices, tan_sphere.indices, GL_STATIC_DRAW
    )

    tan_cylinder = bs.createColorCylinder(255/255, 211/255, 158/255)
    gpuTanCylinder = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuTanCylinder)
    gpuTanCylinder.fillBuffers(
        tan_cylinder.vertices, tan_cylinder.indices, GL_STATIC_DRAW
    )

    pupil_sphere = bs.createColorSphere(38/255, 0, 13/255)
    gpuPupilSphere = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuPupilSphere)
    gpuPupilSphere.fillBuffers(
        pupil_sphere.vertices, pupil_sphere.indices, GL_STATIC_DRAW
    )

    blonde_cone = bs.createColorCone(255/255, 192/255, 74/255)
    gpuBlondeCone = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuBlondeCone)
    gpuBlondeCone.fillBuffers(
        blonde_cone.vertices, blonde_cone.indices, GL_STATIC_DRAW
    )

    pink_cone = bs.createColorCone(255/255, 84/255, 135/255)
    gpuPinkCone = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuPinkCone)
    gpuPinkCone.fillBuffers(
        pink_cone.vertices, pink_cone.indices, GL_STATIC_DRAW
    )

    blonde_sphere = bs.createColorSphere(255/255, 192/255, 74/255)
    gpuBlondeSphere = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuBlondeSphere)
    gpuBlondeSphere.fillBuffers(
        blonde_sphere.vertices, blonde_sphere.indices, GL_STATIC_DRAW
    )

    blonde_cylinder = bs.createColorCylinder(255/255, 192/255, 74/255)
    gpuBlondeCylinder = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuBlondeCylinder)
    gpuBlondeCylinder.fillBuffers(
        blonde_cylinder.vertices, blonde_cylinder.indices, GL_STATIC_DRAW
    )

    black_cube = bs.createColorCube(0,0,0)
    gpuBlackCube = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuBlackCube)
    gpuBlackCube.fillBuffers(
        black_cube.vertices, black_cube.indices, GL_STATIC_DRAW
    )

    black_cylinder = bs.createColorCylinder(0,0,0)
    gpuBlackCylinder = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuBlackCylinder)
    gpuBlackCylinder.fillBuffers(
        black_cylinder.vertices, black_cylinder.indices, GL_STATIC_DRAW
    )

    #---------------------------------------------------------------------

    eyeball = sg.SceneGraphNode('eyeball')
    eyeball.transform = tr.scale(0.5, 0.35, 0.1)
    eyeball.childs += [gpuWhiteSphere]

    pupil = sg.SceneGraphNode('pupil')
    pupil.transform = tr.matmul([tr.translate(0,0,0.1), tr.scale(0.1, 0.36, 0.1)])
    pupil.childs += [gpuPupilSphere]

    eye = sg.SceneGraphNode('eye')
    eye.childs += [eyeball, pupil]

    head = sg.SceneGraphNode('head')
    head.transform = tr.scale(0.8, 0.75, 0.6)
    head.childs += [gpuTanSphere]

    # SMILE
    smile_piece = sg.SceneGraphNode('piece')
    smile_piece.transform = tr.scale(0.1, 0.2, 0.05)
    smile_piece.childs += [gpuBlackCylinder]

    smile_pieces = []
    r = 0.5
    n = 8
    for i in range(0, n):
        theta = np.pi*(i)/(n)
        current_x = r*np.cos(np.pi + theta)
        current_y = r*np.sin(np.pi + theta)

        smile_pieces += [sg.SceneGraphNode('smile_piece_'+str(i+1))]
        smile_pieces[i].transform = tr.matmul([tr.translate(current_x,current_y,0.0), tr.rotationZ(np.pi+theta)])
        smile_pieces[i].childs += [smile_piece]
    
    smile = sg.SceneGraphNode('smile')
    smile.childs += smile_pieces

    left_eye = sg.SceneGraphNode('left eye')
    left_eye.transform = tr.translate(0.5, 0.2, 0.6)
    left_eye.childs += [eye]

    right_eye = sg.SceneGraphNode('right eye')
    right_eye.transform = tr.translate(-0.5, 0.2, 0.6)
    right_eye.childs += [eye]

    left_smile = sg.SceneGraphNode('left smile')
    left_smile.transform = tr.matmul([tr.translate(0.24,-0.3, 0.5), tr.rotationX(np.pi/30), tr.uniformScale(0.48)])
    left_smile.childs += [smile]

    right_smile = sg.SceneGraphNode('right smile')
    right_smile.transform = tr.matmul([tr.translate(-0.24,-0.3, 0.5), tr.rotationX(np.pi/30), tr.uniformScale(0.48)])
    right_smile.childs += [smile]

    head_w_face = sg.SceneGraphNode('head with face')
    head_w_face.childs+= [head, left_eye, right_eye, left_smile, right_smile]

    # PELO
    hair_piece = sg.SceneGraphNode('hair piece')
    hair_piece.transform = tr.matmul([tr.translate(np.cos(np.pi+np.pi*1/10),0.0, np.sin(np.pi+np.pi*1/10)), tr.rotationZ(-np.pi/10), tr.rotationZ(np.pi), tr.scale(0.35,0.7,0.35)])
    hair_piece.childs += [gpuBlondeCone]

    hair_pieces = []
    r = 1
    n = 10
    for i in range(1, n):
        theta = np.pi*(i+1)/(n) + np.pi*1/40

        hair_pieces += [sg.SceneGraphNode('smile_piece_'+str(i+1))]
        hair_pieces[i-1].transform = tr.matmul([tr.rotationY(np.pi + theta)])
        hair_pieces[i-1].childs += [hair_piece]

    hair_back = sg.SceneGraphNode('hair back')
    hair_back.transform = tr.matmul([tr.translate(0,-0.4,0.3), tr.scale(1.05,1.1,0.8)])
    hair_back.childs += hair_pieces

    hair_top = sg.SceneGraphNode('hair top')
    hair_top.transform = tr.matmul([tr.translate(0,0.45,0), tr.scale(1.15, 0.8, 0.6)])
    hair_top.childs += [gpuBlondeSphere]

    hair = sg.SceneGraphNode('hair')
    hair.childs = [hair_top, hair_back]

    # OREJAS
    ear_frame = sg.SceneGraphNode('left ear frame')
    ear_frame.transform = tr.scale(1,1,0.2)
    ear_frame.childs += [gpuBlondeCone]

    left_ear_stuff1 = sg.SceneGraphNode('left ear stuff 1')
    left_ear_stuff1.transform = tr.matmul([tr.translate(-0.3,-0.3,0.15), tr.rotationZ(np.pi/2-np.pi/6), tr.scale(0.4, 0.5, 0.01)])
    left_ear_stuff1.childs += [gpuPinkCone]
    left_ear_stuff2 = sg.SceneGraphNode('left ear stuff 2')
    left_ear_stuff2.transform = tr.matmul([tr.translate(-0.15,-0.6,0.2), tr.rotationZ(np.pi/2), tr.scale(0.4, 0.5, 0.01)])
    left_ear_stuff2.childs += [gpuPinkCone]
    left_ear_stuff3 = sg.SceneGraphNode('left ear stuff 3')
    left_ear_stuff3.transform = tr.matmul([tr.translate(0.15,-0.9,0.25), tr.rotationZ(np.pi/2+np.pi/6), tr.scale(0.4, 0.5, 0.01)])
    left_ear_stuff3.childs += [gpuPinkCone]

    right_ear_stuff1 = sg.SceneGraphNode('right ear stuff 1')
    right_ear_stuff1.transform = tr.matmul([tr.translate(0.3,-0.3,0.15), tr.rotationZ(-np.pi/2+np.pi/6), tr.scale(0.4, 0.5, 0.01)])
    right_ear_stuff1.childs += [gpuPinkCone]
    right_ear_stuff2 = sg.SceneGraphNode('right ear stuff 2')
    right_ear_stuff2.transform = tr.matmul([tr.translate(0.15,-0.6,0.2), tr.rotationZ(-np.pi/2), tr.scale(0.4, 0.5, 0.01)])
    right_ear_stuff2.childs += [gpuPinkCone]
    right_ear_stuff3 = sg.SceneGraphNode('right ear stuff 3')
    right_ear_stuff3.transform = tr.matmul([tr.translate(-0.15,-0.9,0.25), tr.rotationZ(-np.pi/2-np.pi/6), tr.scale(0.4, 0.5, 0.01)])
    right_ear_stuff3.childs += [gpuPinkCone]

    left_ear = sg.SceneGraphNode('left ear')
    left_ear.transform = tr.matmul([tr.rotationZ(40*np.pi/180), tr.translate(0,1.7,0), tr.uniformScale(0.6)])
    left_ear.childs = [ear_frame, left_ear_stuff1, left_ear_stuff2, left_ear_stuff3]

    right_ear = sg.SceneGraphNode('right ear')
    right_ear.transform = tr.matmul([tr.rotationZ(-40*np.pi/180), tr.translate(0,1.7,0), tr.uniformScale(0.6)])
    right_ear.childs = [ear_frame, right_ear_stuff1, right_ear_stuff2, right_ear_stuff3]

    ears = sg.SceneGraphNode('ears')
    ears.transform = tr.rotationX(15*np.pi/180)
    ears.childs += [left_ear, right_ear]

    head_complete = sg.SceneGraphNode('head complete')
    head_complete.transform = tr.translate(0,2,0)
    head_complete.childs += [head_w_face, hair, ears]

    torso = sg.SceneGraphNode('torso')
    torso.transform = tr.matmul([tr.translate(0, 0.65, 0), tr.scale(0.4, 0.5, 0.35)])
    torso.childs += [gpuWhiteCylinder]

    neck = sg.SceneGraphNode('neck')
    neck.transform = tr.matmul([tr.translate(0, 1.2, 0), tr.scale(0.1, 0.5, 0.1)])
    neck.childs += [gpuWhiteCylinder]

    skirt = sg.SceneGraphNode('skirt')
    skirt.transform = tr.matmul([tr.translate(0, 0.3, 0), tr.scale(0.7, 1, 0.6)])
    skirt.childs += [gpuDressCone]

    forearm = sg.SceneGraphNode('forearm')
    forearm.transform = tr.matmul([tr.rotationZ(np.pi/2), tr.scale(0.2, 0.8, 0.2)])
    forearm.childs += [gpuWhiteCylinder]

    wrist = sg.SceneGraphNode('wrist')
    wrist.transform = tr.matmul([tr.translate(-1.05+0.2, 0, 0), tr.rotationZ(np.pi/2), tr.uniformScale(0.1)])
    wrist.childs += [gpuTanCylinder]

    hand = sg.SceneGraphNode('hand')
    hand.transform = tr.matmul([tr.translate(-1.05-0.3+0.2, 0, 0), tr.uniformScale(0.3)])
    hand.childs += [gpuTanSphere]

    arm = sg.SceneGraphNode('arm')
    arm.childs += [hand, wrist, forearm]

    left_arm = sg.SceneGraphNode('left arm')
    left_arm.transform = tr.translate(-0.9, 0.9, 0)
    left_arm.childs += [arm]

    right_arm = sg.SceneGraphNode('right arm')
    right_arm.transform = tr.matmul([tr.translate(0.9, 0.9, 0), tr.rotationZ(np.pi)])
    right_arm.childs += [arm]

    lower_leg = sg.SceneGraphNode('lower leg')
    lower_leg.transform = tr.scale(0.1, 0.8, 0.1)
    lower_leg.childs += [gpuBlackCylinder]

    foot = sg.SceneGraphNode('foot')
    foot.transform = tr.matmul([tr.translate(0, -0.8, 0.2), tr.scale(0.15, 0.1, 0.3)])
    foot.childs += [gpuBlackCube]

    leg = sg.SceneGraphNode('leg')
    leg.childs += [lower_leg, foot]

    left_leg = sg.SceneGraphNode('left leg')
    left_leg.transform = tr.translate(0.3, -1, 0)
    left_leg.childs += [leg]

    right_leg = sg.SceneGraphNode('right leg')
    right_leg.transform = tr.translate(-0.3, -1, 0)
    right_leg.childs += [leg]

    tail = sg.SceneGraphNode('tail')
    tail.transform = tr.matmul([tr.translate(0, 0.1, -1.75), tr.rotationX(-np.pi/2), tr.scale(0.15, 1.5, 0.15)])
    tail.childs += [gpuBlondeCylinder]

    body = sg.SceneGraphNode('body')
    body.childs += [torso, neck, skirt, left_arm, right_arm, left_leg, right_leg, tail]

    neco_arc = sg.SceneGraphNode(name)
    neco_arc.transform = tr.matmul([tr.uniformScale(0.15)])
    neco_arc.childs += [head_complete, body]


    return neco_arc

