import pygame
from pygame.locals import *


def main():
    width, height = 1000, 1000
    screen = pygame.display.set_mode((width, height), DOUBLEBUF)
    xaxis = width / 1.5 + 140
    yaxis = height / 2
    scale = 400
    iterations = 50

    for iy in range(height // 2 + 1):
        for ix in range(width):
            z = 0 + 0j
            c = complex(float(ix - xaxis) / scale, float(iy - yaxis) / scale)
            for i in range(iterations):
                z = z ** 2 + c
                if abs(z) > 2:
                    v = (3 * 255) * i / iterations
                    if v > (2 * 255):
                        color = (255, 255, v % 255)
                    elif v > 255:
                        color = (255, v % 255, 0)
                    else:
                        color = (v % 255, 0, 0)
                    break
                else:
                    color = (0, 0, 0)

            screen.set_at((ix, iy), color)
            screen.set_at((ix, height - iy), color)

    pygame.display.update()

    while True:
        event = pygame.event.poll()
        if (event.type == QUIT or
                (event.type == KEYDOWN and event.key == K_ESCAPE)):
            break


if __name__ == "__main__":
    main()
