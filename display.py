import pygame

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


setup()
crashed = False
while not crashed:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True

pygame.quit()
quit()
