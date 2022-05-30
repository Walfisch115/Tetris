# import and initialization
import pygame
import random

from pygame.locals import *

pygame.init()

#Display configuration
fps = 30
screen_width = 600
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
screen.fill((125, 93, 76))
pygame.display.set_caption('Tetris')

#Entities

#Klassen können später ausgelagert werden, find's für den Anfang nur einfacher so zu arbeiten

class Shape:
    #Tetrominoes aka Spielsteine
    O = [[[0,1,1],
          [0,1,1]],
         [[0,1,1],
          [0,1,1]]]

    S = [[[0,1,1],
          [1,1,0]],
         [[0,1,0],
          [0,1,1],
          [0,0,1]],
         [[0,0,0],
          [0,1,1],
          [1,1,0]],
         [[1,0],
          [1,1],
          [0,1]]]

    Z = [[[1,1,0],
          [0,1,1]],
         [[0,0,1],
          [0,1,1],
          [0,1,0]],
         [[0,0,0],
          [1,1,0],
          [0,1,1]],
         [[0,1],
          [1,1],
          [1,0]]]

    I = [[[0,0,0,0],
          [1,1,1,1]],
         [[0,0,1],
          [0,0,1],
          [0,0,1],
          [0,0,1]],
         [[0,0,0,0],
          [0,0,0,0],
          [1,1,1,1]],
         [[0,1],
          [0,1],
          [0,1],
          [0,1]]]

    J = [[[1,0,0],
          [1,1,1]],
         [[0,1,1],
          [0,1,0],
          [0,1,0]],
         [[0,0,0],
          [1,1,1],
          [0,0,1]],
         [[0,1],
          [0,1],
          [1,1]]]

    L = [[[0,0,1],
          [1,1,1]],
         [[0,1,0],
          [0,1,0],
          [0,1,1]],
         [[0,0,0],
          [1,1,1],
          [1,0,0]],
         [[1,1],
          [0,1],
          [0,1]]]

    T = [[[0,1,0],
          [1,1,1]],
         [[0,1,0],
          [0,1,1],
          [0,1,0]],
         [[0,0,0],
          [1,1,1],
          [0,1,0]],
         [[0,1],
          [1,1],
          [0,1]]]

    #Zugriff auf alle Formen über diese Liste
    shapes = [O, S, Z, I, J, L, T]

    x = 0
    y = 0

    #Damit anfangs ein ein nächstes und gegenwärtiges Stück initialisiert werden
    next = -1


    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.bag = []
        self.rotation = 0
        #self.piece = -1

        #Beutelprinzip
        if len(self.bag) == 0:
            self.bag = ["O", "S", "Z", "I", "J", "L", "T"]

        #Falls schon ein nächstes Stück initatlisiert ist wird das übernommen und ein neues "nächstes" Stück initiallisiert
        if self.next >= 0:
            self.type = self.next
            self.figure = self.next_figure

            self.next = (random.randint(1, len(self.bag)))-1
            self.next_figure = self.bag[self.type]
            self.bag.pop(self.next)

        #Initatliersiert eine neues gegenwätiges und nächstes stück falls es noch kein nächstes gibt (wird also eigentlich nur beim Ersten mal aufgerufen)
        else:
            self.type = (random.randint(1, len(self.bag)))-1
            #print(self.type)
            self.figure = self.bag[self.type]
            #print(self.figure)
            self.bag.pop(self.type)

            self.next = (random.randint(1, len(self.bag)))-1
            self.next_figure = self.bag[self.next]
            self.bag.pop(self.next)

        #Zuweisung der Spielfigur
        if self.figure == "O":
            self.piece = 0
        elif self.figure == "S":
            self.piece = 1
        elif self.figure == "Z":
            self.piece = 2
        elif self.figure == "I":
            self.piece = 3
        elif self.figure == "J":
            self.piece = 4
        elif self.figure == "L":
            self.piece = 5
        elif self.figure == "T":
            self.piece = 6

    #Rotationen noch nicht getestet!!!
    def rotate_right(self):
        self.rotation = (self.rotation+1) % len(self.shapes[self.piece])
    def rotate_left(self):
        self.rotation = (self.rotation-1) % len(self.shapes[self.piece])

    #Gibt gegenwätige Figur zurück
    def get_image(self):
        return self.shapes[self.piece][self.rotation]

    #Gibt die zugewisene Farbe der gegenwärtigen Figur
    def get_color(self):
        return self.figure

class Game:
    height = 0
    width = 0
    tile = 20 #Feldgröße

    #Obere linke ecke des Spielfeldes
    x_base = screen_width//2-5*tile
    y_base = screen_height//2-10*tile

    #Matrix
    matrix = []

    #Score und Spielzustand für später
    score = 0
    state = "play"

    #Initiallisierung der Matrix (auf 0) als Liste aus Listen
    #Eine Liste entspricht immer einer Zeile
    def __init__(self, height, width, tile):
        self.height = height
        self.width = width
        self.tile = tile * self.tile

        #Spawnzone zwei Felder über der Spielfeld (muss im fertigen Spiel nicht mit angezeigt werden)
        for i in range (2):
            line = []
            for j in range(width):
                line.append(0)
            self.matrix.append(line)

        #Spielfeld
        for i in range (height):
            line = []
            for j in range(width):
                line.append(0)
            self.matrix.append(line)


    #Fügt Spielfigur in die Matrix ein (als 1)
    def create_shape(self):
        self.shape = Shape(3, 0)
        self.piece = self.shape.get_image()
        self.color = self.shape.get_color()
        self.set_1(0,0)

    #Steuerung
    def down(self):
        self.set_0()
        self.set_1(0,1)

    def left(self):
        self.set_0()
        self.set_1(-1,0)

    def right(self):
        self.set_0()
        self.set_1(1,0)

    #Festsetzen der Steine
    def freeze(self):
        run_x = 0
        run_y = 0
        matrix_x = self.shape.x
        matrix_y = self.shape.y
        for i in range(len(self.piece)):
            run_x = 0
            matrix_x = self.shape.x
            for j in range(len(self.piece[run_y])):
                if self.piece[run_y][run_x] == 1:
                    self.matrix[matrix_y][matrix_x] = 2
                run_x += 1
                matrix_x += 1
            run_y += 1
            matrix_y += 1
        self.create_shape()

    #Kollision der x Werte testen
    def collision_x(self, x):
        collision_x = x
        border_x = len(self.matrix[0])
        if len(self.piece[0]) + collision_x > border_x:
            return True
        elif collision_x < 0:
            for i in range(len(self.piece)):
                if self.piece[i][0] == 1:
                    return True
        return False

    #Kollision der y Werte Testen
    def collision_y(self, y):
        collision_y = y
        border_y = len(self.matrix)
        if len(self.piece) + collision_y > border_y:
            return True
        return False

    #Kollision mit anderen Figuren testen
    def collision_shape(self, x, y):
        collision_x = x
        collision_y = y
        run_x = 0
        run_y = 0
        for i in range(len(self.piece)):
            run_x = 0
            collision_x = x
            for j in range(len(self.piece[run_y])):
                if self.piece[run_y][run_x] == 1 and self.matrix[collision_y][collision_x] == 2:
                    return True
                run_x += 1
                collision_x += 1
            run_y += 1
            collision_y += 1
        return False

    #Figur auf 0 setzen
    def set_0(self):
        run_x = 0
        run_y = 0
        matrix_x = self.shape.x
        matrix_y = self.shape.y
        for i in range(len(self.piece)):
            run_x = 0
            matrix_x = self.shape.x
            for j in range(len(self.piece[run_y])):
                if self.matrix[matrix_y][matrix_x] == 1:
                    self.matrix[matrix_y][matrix_x] = 0
                run_x += 1
                matrix_x += 1
            run_y += 1
            matrix_y += 1

    #Figur initialisieren (auf 1 setzen)
    def set_1(self, offset_x, offset_y):
        x = offset_x
        y = offset_y
        run_x = 0
        run_y = 0
        matrix_x = self.shape.x + x
        matrix_y = self.shape.y + y
        col_x = self.collision_x(matrix_x)
        col_y = self.collision_y(matrix_y)
        if col_x:
            self.set_1(0,0)
        elif col_y:
            self.set_1(0,0)
            self.freeze()
        else:
            col_shape = self.collision_shape(matrix_x, matrix_y)
            if col_shape:
                self.set_1(0,0)
                self.freeze()
            else:
                for i in range(len(self.piece)):
                    run_x = 0
                    matrix_x = self.shape.x + x
                    for j in range(len(self.piece[run_y])):
                        if self.piece[run_y][run_x] == 1 and self.matrix[matrix_y][matrix_x] != 2:
                            self.matrix[matrix_y][matrix_x] = 1
                        run_x += 1
                        matrix_x += 1
                    run_y += 1
                    matrix_y += 1
                self.shape.x += x
                self.shape.y += y

    #Zeichnet Spielfeld und Spielfiguren
    def draw(self):
        x = self.x_base
        y = self.y_base - 2*self.tile
        matrix_x = 0
        matrix_y = 0

        #Spwazone
        for i in range (2):
            matrix_x = 0
            x = self.x_base
            for j in range(len(self.matrix[matrix_y])):
                if self.matrix[matrix_y][matrix_x] == 0:
                    tetromino = pygame.draw.rect(screen, GREY, pygame.Rect(x, y, self.tile, self.tile))
                elif self.matrix[matrix_y][matrix_x] == 1:
                    spawn = pygame.draw.rect(screen, colors[self.color], pygame.Rect(x, y, self.tile, self.tile))
                spawn = pygame.draw.rect(screen, BLACK, pygame.Rect(x, y, self.tile, self.tile), 1)
                matrix_x += 1
                x += self.tile
            matrix_y += 1
            y += self.tile

        #Spielfeld
        for i in range (len(self.matrix)-2):
            matrix_x = 0
            x = self.x_base
            for j in range(len(self.matrix[matrix_y])):
                if self.matrix[matrix_y][matrix_x] == 0:
                    tetromino = pygame.draw.rect(screen, WHITE, pygame.Rect(x, y, self.tile, self.tile))
                elif self.matrix[matrix_y][matrix_x] == 1:
                    game = pygame.draw.rect(screen, colors[self.color], pygame.Rect(x, y, self.tile, self.tile))
                game = pygame.draw.rect(screen, BLACK, pygame.Rect(x, y, self.tile, self.tile), 1)
                matrix_x += 1
                x += self.tile
            matrix_y += 1
            y += self.tile
        box = pygame.draw.rect(screen, BLACK, pygame.Rect(self.x_base, self.y_base, self.width*self.tile, self.height*self.tile), 3)




# Action --> ALTER
# Assign Variables


#Standardfarben
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (128, 128, 128)

#Farben der Spielsteine
colors = {
    'I': (0, 255, 255),  # LIGHT_BLUE
    'J': (0, 0, 255),    # BLUE
    'L': (255, 128, 0),  # ORANGE
    'O': (255, 255, 0),  # YELLOW
    'S': (0, 255, 0),    # GREEN
    'T': (255, 0, 255),  # PURPLE
    'Z': (255, 0, 0)     # RED
}

#Initialiseierungswerte
height = 20
width = 10
tile = 1

#Testinitalisierung des Spiels
game = Game(height, width, tile)
game.create_shape()
game.draw()


keepGoing = True

clock = pygame.time.Clock()


#Eigentliches Spiel noch nicht benutzung

#Loop
while keepGoing:

    #Timer
    clock.tick(fps)

    # Event Handeling
    for event in pygame.event.get():

        if event.type == QUIT:
            keepGoing = False
            break

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                game.down()
                game.draw()
            elif event.key == pygame.K_LEFT:
                game.left()
                game.draw()
            elif event.key == pygame.K_RIGHT:
                game.right()
                game.draw()
            elif event.key == pygame.K_a:
                game.shape.rotate_right()
                game.set_0()
                game.shape.get_image()
                game.set_1(0,0)
                game.draw()
            elif event.key == pygame.K_s:
                game.shape.rotate_right()
                game.set_0()
                game.shape.get_image()
                game.set_1(0,0)
                game.draw()

    # Redisplay
    pygame.display.flip()
