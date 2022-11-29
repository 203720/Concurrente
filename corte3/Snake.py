import pygame
import sys
import random
import threading
import time

mutex = threading.Lock()

class Snake(threading.Thread):
    def __init__(self):
        super(Snake, self).__init__()
        self.length = 1
        self.positions = [((screen_width/2), (screen_height/2))]
        self.direction = random.choice([up, down, left, right])
        self.color = (255, 255, 255)
        self.score = 0

    def get_head_position(self):
        return self.positions[0]

    def turn(self, point):
        if self.length > 1 and (point[0]*-1, point[1]*-1) == self.direction:
            return
        else:
            self.direction = point

    def move(self):
        cur = self.get_head_position()
        x,y = self.direction
        new = (((cur[0]+(x*gridsize))%screen_width), (cur[1]+(y*gridsize))%screen_height)
        if len(self.positions) > 2 and new in self.positions[2:]:
            self.reset()
        else:
            self.positions.insert(0,new)
            if len(self.positions) > self.length:
                self.positions.pop()

    def reset(self):
        self.length = 1
        self.positions = [((screen_width/2), (screen_height/2))]
        self.direction = random.choice([up, down, left, right])
        self.score = 0
        time.sleep(1)

    def draw(self,surface):
        for p in self.positions:
            r = pygame.Rect((p[0], p[1]), (gridsize,gridsize))
            pygame.draw.rect(surface, self.color, r)
            pygame.draw.rect(surface, (93,216, 228), r, 1)

    def handle_keys(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.turn(up)
                elif event.key == pygame.K_DOWN:
                    self.turn(down)
                elif event.key == pygame.K_LEFT:
                    self.turn(left)
                elif event.key == pygame.K_RIGHT:
                    self.turn(right)

    def handle_keys2(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == ord('w'):
                    self.turn(up)
                elif event.key == ord('s'):
                    self.turn(down)
                elif event.key == ord('a'):
                    self.turn(left)
                elif event.key == ord('d'):
                    self.turn(right)

    def run(self):
        print('Entró')
        with mutex:
            print('mutex')
            pygame.init()
            clock = pygame.time.Clock()
            screen = pygame.display.set_mode((screen_width, screen_height), 0, 32)

            surface = pygame.Surface(screen.get_size())
            surface = surface.convert()
            drawGrid(surface)
            
            myfont = pygame.font.SysFont("sans-serif",18)
            food = Food()

        while(True):
            clock.tick(10)
            drawGrid(surface)
            self.draw(surface)
            self.handle_keys()
            self.move()
            if self.get_head_position() == food.position:
                self.length += 1
                self.score += 1
                food.randomize_position()
            food.draw(surface)
            screen.blit(surface, (0,0))
            text = myfont.render("Score {0}".format(self.score), 1, (255,255,255))
            screen.blit(text, (5,10))
            pygame.display.update()

class Food():
    def __init__(self):
        self.position = (0,0)
        self.color = (255, 255, 0)
        self.randomize_position()

    def randomize_position(self):
        self.position = (random.randint(0, grid_width-1)*gridsize, random.randint(0, grid_height-1)*gridsize)

    def draw(self, surface):
        r = pygame.Rect((self.position[0], self.position[1]), (gridsize, gridsize))
        pygame.draw.rect(surface, self.color, r)
        pygame.draw.rect(surface, (93, 216, 228), r, 1)

def drawGrid(surface):
    for y in range(0, int(grid_height)):
        for x in range(0, int(grid_width)):
            r = pygame.Rect((x*gridsize, y*gridsize), (gridsize,gridsize))
            pygame.draw.rect(surface,(0,0,0), r)
            
                
screen_width = 480
screen_height = 480

gridsize = 20
grid_width = screen_width/gridsize
grid_height = screen_height/gridsize

up = (0,-1)
down = (0,1)
left = (-1,0)
right = (1,0)

def main():

    arreglo = []

    for i in range(1):
        arreglo.append(Snake())
        print(i+1)

    for t in arreglo:
        t.start()
        print('Thread iniciado')

main()