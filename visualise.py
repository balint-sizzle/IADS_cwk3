import pygame
import os
from random import sample
pygame.init()

p = 60
canvas = pygame.display.set_mode((500,500))
canvas.fill((100,100,100))
things = os.listdir("./ant/")
for t in things:
    os.remove("./ant/"+t)
points = [(sample(range(10, 490), k=1)[0], sample(range(10, 490), k=1)[0]) for i in range(p)]
#points = [[137, 263], [376, 231], [401, 440], [289, 294], [66, 117], [445, 213], [242, 441], [151, 74], [312, 396], [71, 404], [365, 465], [393, 343], [304, 48], [190, 48], [328, 152], [67, 218], [429, 445], [78, 424], [370, 351], [120, 347], [81, 88], [181, 85], [271, 435], [351, 312], [369, 103], [221, 74], [70, 254], [282, 134], [294, 354], [159, 452], [190, 142], [239, 206], [282, 272], [275, 297], [165, 172], [241, 375], [112, 358], [313, 74], [367, 363], [119, 317], [371, 256], [30, 320], [106, 421], [296, 424], [397, 380], [42, 435], [293, 239], [163, 393], [211, 228], [380, 418]]
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
    # ants = len(os.listdir("./ant/"))
    # pygame.image.save(canvas, "ant/a{:04d}.jpg".format(ants))

def hold():
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        pygame.display.update()