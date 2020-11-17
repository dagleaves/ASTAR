import pygame
import numpy as np
import astar

pygame.init()

WIDTH = 800
HEIGHT = 800
SCALE = 25

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('A* Search')
white = [255, 255, 255]
black = [0, 0, 0]


def setup():
    screen.fill(white)
    for i in range(WIDTH):
        if i % (WIDTH / SCALE) == 0:
            pygame.draw.line(screen, black, (i, 0), (i, HEIGHT), 1)
    for i in range(HEIGHT):
        if i % (HEIGHT / SCALE) == 0:
            pygame.draw.line(screen, black, (0, i), (WIDTH, i), 1)
    pygame.display.update()
    createNodes()


def createNodes():
    y_step_size = int(HEIGHT / SCALE)
    x_step_size = int(WIDTH / SCALE)
    print(x_step_size)
    print(y_step_size)
    tile_range = []
    for i in range(y_step_size // 2, HEIGHT, y_step_size):
        print(f'Rows: {i}')
        tile_range.append(i)
    tile_domain = []
    for i in range(x_step_size // 2, WIDTH, x_step_size):
        print(f'Columns: {i}')
        tile_domain.append(i)

    for y in tile_range:
        for x in tile_domain:
            screen.set_at((x, y), black)
    pygame.display.update()

    # startX = np.random.randrange(tile_domain[0], tile_domain[-1], x_step_size)
    # startY = np.random.randrange(tile_range[0], tile_range[-1], y_step_size)

    # goalX = np.random.randrange(tile_domain[0], tile_domain[-1], x_step_size)
    # goalY = np.random.randrange(tile_range[0], tile_range[-1], y_step_size)

    startX = 784
    startY = 784

    goalX = 16
    goalY = 16

    for y in tile_range:
        for x in tile_domain:
            nodes.append(astar.Node(x_step_size, y_step_size,
                                    x, y, startX, startY, goalX, goalY))


nodes = []

setup()
crashed = False
while not crashed:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True

pygame.quit()
quit()
