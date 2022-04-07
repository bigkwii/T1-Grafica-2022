'''
Tarea 1 parte 1
'''
import sys
import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy as np
import tr
import es

if len(sys.argv) !=4:
    tuNombre = 'Álvaro'
    iniciales = "AM"
    rut = 20_265_040
else:
    tuNombre = sys.argv[1]
    iniciales = sys.argv[2]
    rut = int(sys.argv[3])

# IMPORTANT
# change this int for scale of the box and logo
# you may want it to be bigger or smaller depending on your monitor
SCREEN_SIZE = 4

width = 800
height = 600
ar = width/height # aspect ratio
screen_width = 160*SCREEN_SIZE
screen_height = 120*SCREEN_SIZE

l = len(tuNombre)
_r = (ord(tuNombre[0%l])*ord(tuNombre[1%l]))%255
_g = (ord(tuNombre[2%l])*ord(tuNombre[3%l]))%255
_b = (ord(tuNombre[4%l])*ord(tuNombre[5%l]))%255
alpha = ord(iniciales[0])*ord(iniciales[1])
# IMPORTANT
# In order for the speed to stay consistent at different screen sizes,
# dx and dy must be multiplied by SCREEN_SIZE.
# This speed ended up being too fast for my taste.
# Feel free to un-comment the *SCREEN_SIZE in the following 2 lines
dx = 350 * np.cos(alpha)#*SCREEN_SIZE
dy = 350 * np.sin(alpha)#*SCREEN_SIZE
S = (rut/20_000_000)**(3*6) # on april 7th 2022, a true bruh momemt happened.
                            # let me explain: the scale factor needed to be cubed
                            # in order for the change to be noticeable.
                            # HOWEVER, in my case this didn't change much.
                            # Things really only got noticeable at around **15
                            # My scale factor is too close to 1.0
                            # So I just slapped a *6 multiplier in there.
                            # Feel free to remove it.
logo_size = 25*SCREEN_SIZE

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

def createLogo(l, x=0.0,y=0.0,r=1.0,g=1.0,b=1.0):
    '''
    Here's the logo
    Keep in mind the entire thing will be scaled down to fit the aspect ratio,
    so if these x,y,z values seem too large, that's why. 

    l is the size of the "box" containing the logo.
    x , y are the initial coords (will likely remain at 0,0).
    r,g,b are the color.

    As for the logo itself, I picked the Seele logo from the critically acclaimed japanese anime
    series Neon Genesis Evangelion, for a few reasons:
    -It's an asymetric design, so rotations are noticable.
    -It's relatively simple, while still beign quite challenging to make.
    -I like Evangelion.
    -As of March 30th, It's Rei Ayanami's birthday and she's my favorite character from NGE.
      AYANAMI REI                           __.-"..--,__
                               __..---"  | _|    "-_|
                        __.---"          | V|::.-"-._D
                   _--"".-.._   ,,::::::'"\/""'-:-:/
              _.-""::_:_:::::'-8b---"            "'
           .-/  ::::<  |\::::::"\|
           \/:::/::::'\|\| |:::b::|
           /|::/:::/::::-::b:%b:\|
            \/::::d:|8:::b:"%%%%%\|
            |\:b:dP:d.:::%%%%%"""-,
             \:\.V-/ _\|%P_   /  .-._
             '|T\   "%j d:::--\.(    "-.
             ::d<   -" d%|:::do%P"-:.   "-,
             |:I _    /%%%o::o8P    "\.    "\|
              \8b     d%%%%%%P""-._ _ \::.    \|
              \%%8  _./Y%%P/      .::'-oMMo    )
                H"'|V  |  A:::...:odMMMMMM(  ./
                H /_.--"JMMMMbo:d##########b/
             .-'o      dMMMMMMMMMMMMMMP""
           /" /       YMMMMMMMMM|
         /   .   .    "MMMMMMMM/
         :..::..:::..  MMMMMMM:|
          \:/ \::::::::JMMMP":/
           :Ao ':__.-'MMMP:::Y
           dMM"./:::::::::-.Y
          _|b::od8::/:YM::/
          I HMMMP::/:/"Y/"
           \|'""  '':|
    '''
    l = l - l/8 # small adjustment, one of the eyes ended up hanging outside the square
    t = 3.0 # t for thickness
    sqrt3 = np.sqrt(3)
    a = t/sqrt3 # some small distance i needed. it took some high school level geometry to get
    c = t/np.sin(np.pi/6) # another one of such distances
    d = t/np.sin(np.pi/3) # yet another one of such distances, just trust me on this one

    vertexData = np.array([
        # POS                          RGB
        #x     y            z          r       g       b
         l,    l,           0.0,       r/255,  g/255 , b/255, # 0
        -l+a,  l-t,         0.0,       r/255,  g/255 , b/255, # 1
         l-a,  l-t,         0.0,       r/255,  g/255 , b/255, # 2
        -l,    l,           0.0,       r/255,  g/255 , b/255, # 3

        0.0,  -l*sqrt3/2,   0.0,       r/255,  g/255 , b/255, # 4
        0.0,  -l*sqrt3/2+c, 0.0,       r/255,  g/255 , b/255, # 5
       -l+a+d, l-t,         0.0,       r/255,  g/255 , b/255, # 6
        l-a-d, l-t,         0.0,       r/255,  g/255 , b/255, # 7

       -t/2,   l-t,         0.0,       r/255,  g/255,  b/255, # 8
        t/2,   l-t,         0.0,       r/255,  g/255,  b/255, # 9
       -t/2,   -l*sqrt3/2+c,0.0,       r/255,  g/255,  b/255, # 10
        t/2,   -l*sqrt3/2+c,0.0,       r/255,  g/255,  b/255, # 11
       # let's make some eyes
       # EYE 1/7
       -l/2+ l/2,   l/2+ 0.0        ,0.0,       r/255,  g/255,  b/255, # 12
       -l/2+ 0.0,   l/2+ l/4        ,0.0,       r/255,  g/255,  b/255, # 13
       -l/2+ 0.0,   l/2+ l/4-d      ,0.0,       r/255,  g/255,  b/255, # 14
       -l/2+ l/2-c, l/2+ 0.0        ,0.0,       r/255,  g/255,  b/255, # 15
       -l/2+-l/2,   l/2+ 0.0        ,0.0,       r/255,  g/255,  b/255, # 16
       -l/2+-l/2+c, l/2+ 0.0        ,0.0,       r/255,  g/255,  b/255, # 17
       -l/2+ 0.0,   l/2+-l/4        ,0.0,       r/255,  g/255,  b/255, # 18
       -l/2+ 0.0,   l/2+-l/4+d      ,0.0,       r/255,  g/255,  b/255, # 19
       -l/2+ l/16,   l/2+ l/4-d      ,0.0,       r/255,  g/255,  b/255, # 20
       -l/2+ l/16,   l/2+-l/4+d      ,0.0,       r/255,  g/255,  b/255, # 21
       -l/2+-l/16,   l/2+ l/4-d      ,0.0,       r/255,  g/255,  b/255, # 22
       -l/2+-l/16,   l/2+-l/4+d      ,0.0,       r/255,  g/255,  b/255, # 23
       # EYE 2/7
       -l/2+ l/2,    0.0        ,0.0,       r/255,  g/255,  b/255, # 24
       -l/2+ 0.0,    l/4        ,0.0,       r/255,  g/255,  b/255, # 25
       -l/2+ 0.0,    l/4-d      ,0.0,       r/255,  g/255,  b/255, # 26
       -l/2+ l/2-c,  0.0        ,0.0,       r/255,  g/255,  b/255, # 27
       -l/2+-l/2,    0.0        ,0.0,       r/255,  g/255,  b/255, # 28
       -l/2+-l/2+c,  0.0        ,0.0,       r/255,  g/255,  b/255, # 29
       -l/2+ 0.0,   -l/4        ,0.0,       r/255,  g/255,  b/255, # 30
       -l/2+ 0.0,   -l/4+d      ,0.0,       r/255,  g/255,  b/255, # 31
       -l/2+ l/16,    l/4-d      ,0.0,       r/255,  g/255,  b/255, # 32
       -l/2+ l/16,   -l/4+d      ,0.0,       r/255,  g/255,  b/255, # 33
       -l/2+-l/16,    l/4-d      ,0.0,       r/255,  g/255,  b/255, # 34
       -l/2+-l/16,   -l/4+d      ,0.0,       r/255,  g/255,  b/255, # 35
       # EYE 3/7
       -l/2+ l/2,   -l/2+ 0.0        ,0.0,       r/255,  g/255,  b/255, # 36
       -l/2+ 0.0,   -l/2+ l/4        ,0.0,       r/255,  g/255,  b/255, # 37
       -l/2+ 0.0,   -l/2+ l/4-d      ,0.0,       r/255,  g/255,  b/255, # 38
       -l/2+ l/2-c, -l/2+ 0.0        ,0.0,       r/255,  g/255,  b/255, # 39
       -l/2+-l/2,   -l/2+ 0.0        ,0.0,       r/255,  g/255,  b/255, # 40
       -l/2+-l/2+c, -l/2+ 0.0        ,0.0,       r/255,  g/255,  b/255, # 41
       -l/2+ 0.0,   -l/2+-l/4        ,0.0,       r/255,  g/255,  b/255, # 42
       -l/2+ 0.0,   -l/2+-l/4+d      ,0.0,       r/255,  g/255,  b/255, # 43
       -l/2+ l/16,   -l/2+ l/4-d      ,0.0,       r/255,  g/255,  b/255, # 44
       -l/2+ l/16,   -l/2+-l/4+d      ,0.0,       r/255,  g/255,  b/255, # 45
       -l/2+-l/16,   -l/2+ l/4-d      ,0.0,       r/255,  g/255,  b/255, # 46
       -l/2+-l/16,   -l/2+-l/4+d      ,0.0,       r/255,  g/255,  b/255, # 47
       # EYE 4/7
       l/2+ l/2,   l/2+ 0.0        ,0.0,       r/255,  g/255,  b/255, # 48
       l/2+ 0.0,   l/2+ l/4        ,0.0,       r/255,  g/255,  b/255, # 49
       l/2+ 0.0,   l/2+ l/4-d      ,0.0,       r/255,  g/255,  b/255, # 50
       l/2+ l/2-c, l/2+ 0.0        ,0.0,       r/255,  g/255,  b/255, # 51
       l/2+-l/2,   l/2+ 0.0        ,0.0,       r/255,  g/255,  b/255, # 52
       l/2+-l/2+c, l/2+ 0.0        ,0.0,       r/255,  g/255,  b/255, # 53
       l/2+ 0.0,   l/2+-l/4        ,0.0,       r/255,  g/255,  b/255, # 54
       l/2+ 0.0,   l/2+-l/4+d      ,0.0,       r/255,  g/255,  b/255, # 55
       l/2+ l/16,   l/2+ l/4-d      ,0.0,       r/255,  g/255,  b/255, # 56
       l/2+ l/16,   l/2+-l/4+d      ,0.0,       r/255,  g/255,  b/255, # 57
       l/2+-l/16,   l/2+ l/4-d      ,0.0,       r/255,  g/255,  b/255, # 58
       l/2+-l/16,   l/2+-l/4+d      ,0.0,       r/255,  g/255,  b/255, # 59
       # EYE 5/7
       l/2+ l/2,    0.0        ,0.0,       r/255,  g/255,  b/255, # 60
       l/2+ 0.0,    l/4        ,0.0,       r/255,  g/255,  b/255, # 61
       l/2+ 0.0,    l/4-d      ,0.0,       r/255,  g/255,  b/255, # 62
       l/2+ l/2-c,  0.0        ,0.0,       r/255,  g/255,  b/255, # 63
       l/2+-l/2,    0.0        ,0.0,       r/255,  g/255,  b/255, # 64
       l/2+-l/2+c,  0.0        ,0.0,       r/255,  g/255,  b/255, # 65
       l/2+ 0.0,   -l/4        ,0.0,       r/255,  g/255,  b/255, # 66
       l/2+ 0.0,   -l/4+d      ,0.0,       r/255,  g/255,  b/255, # 67
       l/2+ l/16,    l/4-d      ,0.0,       r/255,  g/255,  b/255, # 68
       l/2+ l/16,   -l/4+d      ,0.0,       r/255,  g/255,  b/255, # 69
       l/2+-l/16,    l/4-d      ,0.0,       r/255,  g/255,  b/255, # 70
       l/2+-l/16,   -l/4+d      ,0.0,       r/255,  g/255,  b/255, # 71
       # EYE 6/7
       l/2+ l/2,   -l/2+ 0.0        ,0.0,       r/255,  g/255,  b/255, # 72
       l/2+ 0.0,   -l/2+ l/4        ,0.0,       r/255,  g/255,  b/255, # 73
       l/2+ 0.0,   -l/2+ l/4-d      ,0.0,       r/255,  g/255,  b/255, # 74
       l/2+ l/2-c, -l/2+ 0.0        ,0.0,       r/255,  g/255,  b/255, # 75
       l/2+-l/2,   -l/2+ 0.0        ,0.0,       r/255,  g/255,  b/255, # 76
       l/2+-l/2+c, -l/2+ 0.0        ,0.0,       r/255,  g/255,  b/255, # 77
       l/2+ 0.0,   -l/2+-l/4        ,0.0,       r/255,  g/255,  b/255, # 78
       l/2+ 0.0,   -l/2+-l/4+d      ,0.0,       r/255,  g/255,  b/255, # 79
       l/2+ l/16,   -l/2+ l/4-d      ,0.0,       r/255,  g/255,  b/255, # 80
       l/2+ l/16,   -l/2+-l/4+d      ,0.0,       r/255,  g/255,  b/255, # 81
       l/2+-l/16,   -l/2+ l/4-d      ,0.0,       r/255,  g/255,  b/255, # 82
       l/2+-l/16,   -l/2+-l/4+d      ,0.0,       r/255,  g/255,  b/255, # 83
       # EYE 7/7
       l/2+ l/2,   -l+ 0.0        ,0.0,       r/255,  g/255,  b/255, # 84
       l/2+ 0.0,   -l+ l/4        ,0.0,       r/255,  g/255,  b/255, # 85
       l/2+ 0.0,   -l+ l/4-d      ,0.0,       r/255,  g/255,  b/255, # 86
       l/2+ l/2-c, -l+ 0.0        ,0.0,       r/255,  g/255,  b/255, # 87
       l/2+-l/2,   -l+ 0.0        ,0.0,       r/255,  g/255,  b/255, # 88
       l/2+-l/2+c, -l+ 0.0        ,0.0,       r/255,  g/255,  b/255, # 89
       l/2+ 0.0,   -l+-l/4        ,0.0,       r/255,  g/255,  b/255, # 90
       l/2+ 0.0,   -l+-l/4+d      ,0.0,       r/255,  g/255,  b/255, # 91
       l/2+ l/16,   -l+ l/4-d      ,0.0,       r/255,  g/255,  b/255, # 92
       l/2+ l/16,   -l+-l/4+d      ,0.0,       r/255,  g/255,  b/255, # 93
       l/2+-l/16,   -l+ l/4-d      ,0.0,       r/255,  g/255,  b/255, # 94
       l/2+-l/16,   -l+-l/4+d      ,0.0,       r/255,  g/255,  b/255, # 95


    ], dtype=np.float32)

    indexData = np.array(
        [
            # TOP SIDE
            0,1,2,
            0,3,1,
            # LEFT SIDE
            1,4,5,
            5,6,1,
            # RIGHT SIDE
            4,2,5,
            2,7,5,
            # HEIGHT
            9,8,10,
            9,10,11,
            # EYE 1/7
            12,13,14,
            14,15,12,
            13,16,17,
            17,14,13,
            19,17,16,
            16,18,19,
            18,12,15,
            15,19,18,
            13,20,21,
            21,19,13,
            13,19,23,
            23,22,13,
            # EYE 2/7
            12+12,13+12,14+12,
            14+12,15+12,12+12,
            13+12,16+12,17+12,
            17+12,14+12,13+12,
            19+12,17+12,16+12,
            16+12,18+12,19+12,
            18+12,12+12,15+12,
            15+12,19+12,18+12,
            13+12,20+12,21+12,
            21+12,19+12,13+12,
            13+12,19+12,23+12,
            23+12,22+12,13+12,
            # EYE 3/7
            12+24,13+24,14+24,
            14+24,15+24,12+24,
            13+24,16+24,17+24,
            17+24,14+24,13+24,
            19+24,17+24,16+24,
            16+24,18+24,19+24,
            18+24,12+24,15+24,
            15+24,19+24,18+24,
            13+24,20+24,21+24,
            21+24,19+24,13+24,
            13+24,19+24,23+24,
            23+24,22+24,13+24,
            # EYE 4/7
            12+36,13+36,14+36,
            14+36,15+36,12+36,
            13+36,16+36,17+36,
            17+36,14+36,13+36,
            19+36,17+36,16+36,
            16+36,18+36,19+36,
            18+36,12+36,15+36,
            15+36,19+36,18+36,
            13+36,20+36,21+36,
            21+36,19+36,13+36,
            13+36,19+36,23+36,
            23+36,22+36,13+36,
            # EYE 5/7
            12+48,13+48,14+48,
            14+48,15+48,12+48,
            13+48,16+48,17+48,
            17+48,14+48,13+48,
            19+48,17+48,16+48,
            16+48,18+48,19+48,
            18+48,12+48,15+48,
            15+48,19+48,18+48,
            13+48,20+48,21+48,
            21+48,19+48,13+48,
            13+48,19+48,23+48,
            23+48,22+48,13+48,
            # EYE 6/7
            12+60,13+60,14+60,
            14+60,15+60,12+60,
            13+60,16+60,17+60,
            17+60,14+60,13+60,
            19+60,17+60,16+60,
            16+60,18+60,19+60,
            18+60,12+60,15+60,
            15+60,19+60,18+60,
            13+60,20+60,21+60,
            21+60,19+60,13+60,
            13+60,19+60,23+60,
            23+60,22+60,13+60,
            # EYE 7/7
            12+72,13+72,14+72,
            14+72,15+72,12+72,
            13+72,16+72,17+72,
            17+72,14+72,13+72,
            19+72,17+72,16+72,
            16+72,18+72,19+72,
            18+72,12+72,15+72,
            15+72,19+72,18+72,
            13+72,20+72,21+72,
            21+72,19+72,13+72,
            13+72,19+72,23+72,
            23+72,22+72,13+72
        ], dtype=np.uint32)
    
    return vertexData , indexData

def createScreen():
    '''
    Screen that sits behind the logo
    '''
    vertexData = np.array([
    # POS                   RGB
        #x                    y                      z          r        g        b
        -screen_width/width, -screen_height/height,  0.0,       10/255,  10/255 , 10/255,
         screen_width/width, -screen_height/height,  0.0,       10/255,  10/255 , 10/255,
         screen_width/width,  screen_height/height,  0.0,       10/255,  10/255 , 10/255,
        -screen_width/width,  screen_height/height,  0.0,       10/255,  10/255 , 10/255
    ], dtype=np.float32)

    indexData = np.array(
        [
            0,1,2,
            2,3,0
        ], dtype=np.uint32)
    
    return vertexData , indexData

if __name__ == "__main__":

    # Initialize glfw
    window = None
    if not glfw.init():
        glfw.set_window_should_close(window, True)

    window = glfw.create_window(width, height, "SEELE DVD PLAYER", None, None)

    if not window:
        glfw.terminate()
        glfw.set_window_should_close(window, True)

    glfw.make_context_current(window)
    glfw.set_key_callback(window, on_key)
 
    # Creating our shader program and telling OpenGL to use it
    pipeline = es.SimpleTransformShaderProgram()
    glUseProgram(pipeline.shaderProgram)

    # Setting up the clear screen color
    glClearColor(0.0, 0.0, 0.0, 1.0)

    # Creating shapes on GPU memory
    #SCREEN
    screen = createScreen()
    gpuScreen = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuScreen)
    gpuScreen.fillBuffers(screen[0], screen[1], GL_STATIC_DRAW)
    # LOGO
    logo = createLogo(logo_size, 0 , 0, _r, _g, _b)
    gpuThing = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuThing)
    gpuThing.fillBuffers(logo[0], logo[1], GL_STATIC_DRAW)

    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

    t0 = glfw.get_time()
    x0 = 0
    y0 = 0
    Scale = 1.0
    rot = 0.0

    while not glfw.window_should_close(window):
        # counting time
        t1 = glfw.get_time()
        dt = t1 - t0
        t0 = t1
        
        # counting position
        x1 = x0 + dx*dt
        y1 = y0 + dy*dt
        x0, y0 = x1, y1

        # collisions
        if x1 >= (screen_width - logo_size*S) or x1 <= -(screen_width - logo_size*S):
            dx *= -1
            if Scale == 1.0:
                Scale = S
            else:
                Scale = 1.0
            rot = (rot + np.pi/2)%(2*np.pi)
        if y1 >= (screen_height - logo_size*S) or y1 <= -(screen_height - logo_size*S):
            dy *= -1
            if Scale == 1.0:
                Scale = S
            else:
                Scale = 1.0
            rot = (rot + np.pi/2)%(2*np.pi)


        # Using GLFW to check for input events
        glfw.poll_events()

        # Filling or not the shapes depending on the controller state
        if (controller.fillPolygon):
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        else:
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

        # Clearing the screen in both, color and depth
        glClear(GL_COLOR_BUFFER_BIT)

        # SCREEN RENDERING
        # Transformations for Screen
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "transform"), 1, GL_TRUE, tr.matmul(
            [tr.translate(0, 0, 0),
            tr.scale(1.0, 1.0, 1.0),
            tr.rotationZ(0.0)]
        ))
        # Drawing the screen
        pipeline.drawCall(gpuScreen)

        # LOGO RENDERING
        # Transformations for logo
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "transform"), 1, GL_TRUE, tr.matmul(
            [tr.translate(x1/width, y1/height, 0),
            tr.scale(Scale/width, Scale/height, 1.0),
            tr.rotationZ(rot)]
        ))
        # Drawing the logo
        pipeline.drawCall(gpuThing)

        # Once the render is done, buffers are swapped, showing only the complete scene.
        glfw.swap_buffers(window)

    # freeing GPU memory
    gpuThing.clear()
    gpuScreen.clear()

    glfw.terminate()