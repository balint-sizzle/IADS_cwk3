import pygame
import math
from random import sample
pygame.init()

p = 12
canvas = pygame.display.set_mode((1200,800))
canvas.fill((100,100,100))

points = [(sample(range(10, 1200), k=1)[0], sample(range(10, 800), k=1)[0]) for i in range(p)]

#points = [(186, 533), (543, 678), (354, 80), (454, 248), (329, 448), (331, 590), (265, 481), (565, 678), (234, 314), (27, 575), (638, 405), (141, 276)]
with open("newtown", "w") as f:
    for P in points:
        f.write(str(P[0])+"  "+str(P[1])+"\n")
f.close()


def draw_towns():
    for i in points:
        pygame.draw.circle(canvas, (150,0,0), i, 10)

def draw_best(path):
    canvas.fill((100,100,100))
    for t in range(len(path)-1):
        start = points[path[t]]
        end = points[path[t+1]]
        pygame.draw.line(canvas, (0,0,0),start, end, 3)
    pygame.draw.line(canvas, (0, 100,0), points[path[0]], points[path[-1]], 4)

def draw_pheromones(phers):
    canvas.fill((100,100,100))

    for i in range(len(phers)):
        for j in range(len(phers[i])):
            start = points[i]
            end = points[j]
            strength = int(phers[i][j]*255)
            pygame.draw.line(canvas, (strength,0,0), start, end, 2)

def update_screen():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
    pygame.display.update()

def hold():
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        pygame.display.update()