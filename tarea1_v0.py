import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy
import sys
import math

__author__ = "Ivan Sipiran"
__license__ = "MIT"

# We will use 32 bits data, so an integer has 4 bytes
# 1 byte = 8 bits
SIZE_IN_BYTES = 4

# Quería poder apretar espacio para ver las aristas como en el AUX 2
# A class to store the application control
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


def crear_dama(x,y,r,g,b,radius):
    circle = []
    for angle in range(0,360,10):
        circle.extend([x, y, 0.0, r, g, b])
        circle.extend([x+numpy.cos(numpy.radians(angle))*radius, 
                       y+numpy.sin(numpy.radians(angle))*radius, 
                       0.0, r, g, b])
        circle.extend([x+numpy.cos(numpy.radians(angle+10))*radius, 
                       y+numpy.sin(numpy.radians(angle+10))*radius, 
                       0.0, r, g, b])

    # Pongamos un poco más de detalle...
    # La típica indentación de las damas
    for angle in range(0,360,10):
        circle.extend([x, y, 0.0, r-0.05, g-0.05, b-0.05])
        circle.extend([x+numpy.cos(numpy.radians(angle))*radius/1.75, 
                       y+numpy.sin(numpy.radians(angle))*radius/1.75, 
                       0.0, r-0.05, g-0.05, b-0.05])
        circle.extend([x+numpy.cos(numpy.radians(angle+10))*radius/1.75, 
                       y+numpy.sin(numpy.radians(angle+10))*radius/1.75, 
                       0.0, r-0.05, g-0.05, b-0.05])
    # Y un logo (una corona al centro, son solo 3 triángulos)
    circle.extend([x,y-radius/1.75/2,0.0, r-0.15,g-0.15,b-0.15])
    circle.extend([x-radius/2/1.75,y-radius/1.75/2+radius/1.75,0.0, r-0.15,g-0.15,b-0.15])
    circle.extend([x-radius/2/1.75,y-radius/1.75/2,0.0, r-0.15,g-0.15,b-0.15])
    circle.extend([x,y-radius/1.75/2,0.0, r-0.15,g-0.15,b-0.15])
    circle.extend([x+radius/2/1.75,y-radius/1.75/2+radius/1.75,0.0, r-0.15,g-0.15,b-0.15])
    circle.extend([x+radius/2/1.75,y-radius/1.75/2,0.0, r-0.15,g-0.15,b-0.15])
    circle.extend([x+radius/4/1.75,y-radius/1.75/2,0.0, r-0.15,g-0.15,b-0.15])
    circle.extend([x,y-radius/1.75/2+radius/1.75,0.0, r-0.15,g-0.15,b-0.15])
    circle.extend([x-radius/4/1.75,y-radius/1.75/2,0.0, r-0.15,g-0.15,b-0.15])

    return numpy.array(circle, dtype = numpy.float32)


def crear_cuadrado(pos, a, color):
    '''
    Crea un solo cuadrado con origen en pos = [x,y], arista a, color = [r,g,b]
    pos = [x,y]
    arista a
    color = [r,g,b]

    retorna un arreglo numpy

    0   3___________ 5
     | \ \           |
     |   \ \         |
     |     \ \       |
     |       \ \     |
     |         \ \   |
     |___________\ \_|
    1            2   4
    0->1->2->0, 3->4->5->3
    '''
    cuadrado = numpy.array([

        #POS                         RGB
        # x     , y       , z  ,     r       , g       , b
        pos[0]  , pos[1]  , 0.0,     color[0], color[1], color[2], #0
        pos[0]  , pos[1]-a, 0.0,     color[0], color[1], color[2], #1
        pos[0]+a, pos[1]-a, 0.0,     color[0], color[1], color[2], #2

        pos[0]  , pos[1]  , 0.0,     color[0], color[1], color[2], #3, o sea 0
        pos[0]+a, pos[1]-a, 0.0,     color[0], color[1], color[2], #4, o sea 2
        pos[0]+a, pos[1]  , 0.0,     color[0], color[1], color[2], #5
        
    ], dtype = numpy.float32)

    return cuadrado


def crear_tablero(pos,a,n,color1,color2):
    '''
    Simplemente pone un un montón de cuadrados en patrón de ajedrez,
    es decir, formando un cuadrado intercalando colores

    pos = [x, y]
    a = arista
    n = int, número de cuadritos
    color1 = [r,g,b]
    color2 = [r,g,b]

    retorna un arreglo numpy con todo esto.

    +-+-+-+-+
    |>|>|>|>|
    +-+-+-+-+
    |>|>|>|>|
    +-+-+-+-+
    |>|>|>|>|
    +-+-+-+-+
    |>|>|>|x|
    +-+-+-+-+
    '''
    tablero = [] # vamos a llenar esto
    poner_color1 = True # FLAG para ir alternando colores
    for row in range(0, n): # FILA <= n
        for col in range(0,n): # COLUMNA <= n
            if poner_color1:
                tablero.extend(
                    crear_cuadrado([pos[0]+col*a, pos[1]-row*a], a, color1)
                )
            else:
                tablero.extend(
                    crear_cuadrado([pos[0]+col*a, pos[1]-row*a], a, color2)
                )
            # flip color
            poner_color1 = not poner_color1
        # hay que hacer otro flip al pasar a otra fila
        poner_color1 = not poner_color1
    
    # Ya que estamos acá, hagámosle un borde al tablero (no será costumizable, perdón)
    # Me disculpo por adelantado por la siguiente pared de extends.
    cafecito = [0.43137254902, 0.15686274509, 0]
    # TOP
    tablero.extend([pos[0]-a/2, pos[1]+a/2, 0.0, cafecito[0], cafecito[1], cafecito[2]])
    tablero.extend([pos[0]-a/2, pos[1], 0.0, cafecito[0], cafecito[1], cafecito[2]])
    tablero.extend([pos[0]+n*a, pos[1]+a/2, 0.0, cafecito[0], cafecito[1], cafecito[2]])
    tablero.extend([pos[0]+n*a, pos[1]+a/2, 0.0, cafecito[0], cafecito[1], cafecito[2]])
    tablero.extend([pos[0]-a/2, pos[1], 0.0, cafecito[0], cafecito[1], cafecito[2]])
    tablero.extend([pos[0]+n*a, pos[1], 0.0, cafecito[0], cafecito[1], cafecito[2]])
    # RIGHT
    tablero.extend([pos[0]+n*a+a/2, pos[1]+a/2, 0.0, cafecito[0], cafecito[1], cafecito[2]])
    tablero.extend([pos[0]+n*a, pos[1]+a/2, 0.0, cafecito[0], cafecito[1], cafecito[2]])
    tablero.extend([pos[0]+n*a+a/2, pos[1]-n*a, 0.0, cafecito[0], cafecito[1], cafecito[2]])
    tablero.extend([pos[0]+n*a, pos[1]+a/2, 0.0, cafecito[0], cafecito[1], cafecito[2]])
    tablero.extend([pos[0]+n*a, pos[1]-n*a, 0.0, cafecito[0], cafecito[1], cafecito[2]])
    tablero.extend([pos[0]+n*a+a/2, pos[1]-n*a, 0.0, cafecito[0], cafecito[1], cafecito[2]])
    # BOTTOM
    tablero.extend([pos[0]+n*a+a/2, pos[1]-n*a-a/2, 0.0, cafecito[0], cafecito[1], cafecito[2]])
    tablero.extend([pos[0]+n*a+a/2, pos[1]-n*a, 0.0, cafecito[0], cafecito[1], cafecito[2]])
    tablero.extend([pos[0], pos[1]-n*a-a/2, 0.0, cafecito[0], cafecito[1], cafecito[2]])
    tablero.extend([pos[0]+n*a+a/2, pos[1]-n*a, 0.0, cafecito[0], cafecito[1], cafecito[2]])
    tablero.extend([pos[0], pos[1]-n*a, 0.0, cafecito[0], cafecito[1], cafecito[2]])
    tablero.extend([pos[0], pos[1]-n*a-a/2, 0.0, cafecito[0], cafecito[1], cafecito[2]])
    # LEFT
    tablero.extend([pos[0], pos[1]-n*a-a/2, 0.0, cafecito[0], cafecito[1], cafecito[2]])
    tablero.extend([pos[0]-a/2, pos[1], 0.0, cafecito[0], cafecito[1], cafecito[2]])
    tablero.extend([pos[0]-a/2, pos[1]-n*a-a/2, 0.0, cafecito[0], cafecito[1], cafecito[2]])
    tablero.extend([pos[0], pos[1], 0.0, cafecito[0], cafecito[1], cafecito[2]])
    tablero.extend([pos[0]-a/2, pos[1], 0.0, cafecito[0], cafecito[1], cafecito[2]])
    tablero.extend([pos[0], pos[1]-n*a-a/2, 0.0, cafecito[0], cafecito[1], cafecito[2]])

    return numpy.array(tablero, dtype = numpy.float32)


def crear_damas(pos, a, n, r, color1, color2):
    '''
    Crea un montón de damas dependiendo de el tamaño del tablero donde irán puestas,
    respetando el prden que deben seguir en posición inicial del juego.
    pos = [x,y]
    arista a = float32
    n = int, cuantos cuadros hay por lado del tablero
    color1 = [r,g,b] damas de arriba
    color2 = [r,g,b] damas de abajo

    (ver imagen del enunciado)
    '''
    damas = [] # vamos a llenar esto
    corrida_por_1 = False # False: |o| |o| |o| |, True: | |o| |o| |o|
    # DAMAS DE ARRIBA (color1)
    for row in range(0,3): # siempre tener 3 corridas
        for col in range(0, n): # ir de 2 en 2 por columna
            if corrida_por_1 and col%2 != 0:
                damas.extend(crear_dama(pos[0]+col*a+a/2, pos[1]-row*a-a/2, color1[0], color1[1], color1[2], r))
            if not corrida_por_1 and col%2 == 0:
                damas.extend(crear_dama(pos[0]+col*a+a/2, pos[1]-row*a-a/2, color1[0], color1[1], color1[2], r))
            else: pass
        corrida_por_1 = not corrida_por_1
    # en caso de que el tablero no sea par, hay que flipear el corrido de damas para que siempre queden sobre las "negras"
    if n%2 != 0:
        corrida_por_1 = not corrida_por_1
    # DAMAS DE ABAJO (color2)
    for row in range(0,3): # siempre tener 3 corridas
        for col in range(0, n): # ir de 2 en 2 por columna
            if corrida_por_1 and col%2 != 0:
                damas.extend(crear_dama(pos[0]+col*a+a/2, pos[1]-a*(n-3)-row*a-a/2, color2[0], color2[1], color2[2], r))
            if not corrida_por_1 and col%2 == 0:
                damas.extend(crear_dama(pos[0]+col*a+a/2, pos[1]-a*(n-3)-row*a-a/2, color2[0], color2[1], color2[2], r))
            else: pass
        corrida_por_1 = not corrida_por_1
   
    return numpy.array(damas, dtype = numpy.float32)


if __name__ == "__main__":

    # Maldito subrayado amarillo
    window = None

    # Initialize glfw
    if not glfw.init():
        glfw.set_window_should_close(window, True)

    width = 600
    height = 600

    window = glfw.create_window(width, height, "Tarea One", None, None)

    if not window:
        glfw.terminate()
        glfw.set_window_should_close(window, True)

    glfw.make_context_current(window)
    glfw.set_key_callback(window, on_key) 

    # Crear tablero
    tablero = crear_tablero([-0.8,0.8], 0.2, 8, [0.175,0.175,0.175], [0.8,0.175,0.175]) # Prefiero colores más suaves para el tablero
    # Crear primer set de damas
    damas = crear_damas([-0.8,0.8], 0.2, 8, 0.075, [0.8,0.1,0.1], [0.1,0.1,0.1]) # damas rojas y negras porque nunca he visto damas azules
    # Juntando las 2 figuras. Esto no es una forma elegante de hacerlo, pero funciona.
    figura_final = []
    figura_final.extend(tablero)
    figura_final.extend(damas)
    figura_final = numpy.array(figura_final, dtype=numpy.float32)


    # Defining shaders for our pipeline
    vertex_shader = """
    #version 330
    in vec3 position;
    in vec3 color;

    out vec3 newColor;
    void main()
    {
        gl_Position = vec4(position, 1.0f);
        newColor = color;
    }
    """

    fragment_shader = """
    #version 330
    in vec3 newColor;

    out vec4 outColor;
    void main()
    {
        outColor = vec4(newColor, 1.0f);
    }
    """

    # Binding artificial vertex array object for validation
    VAO = glGenVertexArrays(1)
    glBindVertexArray(VAO)

    # Assembling the shader program (pipeline) with both shaders
    shaderProgram = OpenGL.GL.shaders.compileProgram(
        OpenGL.GL.shaders.compileShader(vertex_shader, GL_VERTEX_SHADER),
        OpenGL.GL.shaders.compileShader(fragment_shader, GL_FRAGMENT_SHADER))

    # Each shape must be attached to a Vertex Buffer Object (VBO)
    vbo = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, vbo)
    glBufferData(GL_ARRAY_BUFFER, len(figura_final) * SIZE_IN_BYTES, figura_final, GL_STATIC_DRAW)


    # Telling OpenGL to use our shader program
    glUseProgram(shaderProgram)

    # Setting up the clear screen color
    glClearColor(0.0,0.0, 0.0, 0.0)

    glClear(GL_COLOR_BUFFER_BIT)

    positionDamas = glGetAttribLocation(shaderProgram, "position")
    glVertexAttribPointer(positionDamas, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(0))
    glEnableVertexAttribArray(positionDamas)

    colorDamas = glGetAttribLocation(shaderProgram, "color")
    glVertexAttribPointer(colorDamas, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(12))
    glEnableVertexAttribArray(colorDamas)
    
    # It renders a scene using the active shader program (pipeline) and the active VAO (shapes)

    glDrawArrays(GL_TRIANGLES, 0, int(len(figura_final)/6))

    # Moving our draw to the active color buffer
    glfw.swap_buffers(window)

    # Waiting to close the window
    while not glfw.window_should_close(window):
        # Getting events from GLFW
        glfw.poll_events()

        # Filling or not the shapes depending on the controller state
        if (controller.fillPolygon):
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        else:
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

        # Clearing the screen in both, color and depth
        glClear(GL_COLOR_BUFFER_BIT)

        # Drawing the Quad as specified in the VAO without indices
        glBindVertexArray(VAO)
        #            draw_mode,   pointer=0, vertex_count 
        glDrawArrays(GL_TRIANGLES, 0, int(len(figura_final)/6))

        # Once the render is done, buffers are swapped, showing only the complete scene.
        glfw.swap_buffers(window)

    # freeing GPU memory
    glDeleteBuffers(1, [vbo])
    glDeleteVertexArrays(1, [VAO])

    glfw.terminate()

