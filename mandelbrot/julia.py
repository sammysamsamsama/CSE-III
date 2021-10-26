import pygame
from pygame.locals import *


def main():
    width, height = 400, 400
    screen = pygame.display.set_mode((width, height), DOUBLEBUF)
    xaxis = width / 2
    yaxis = height / 2
    scale = 130
    iterations = 20

    while True:
        event = pygame.event.poll()
        if (event.type == QUIT or
                (event.type == KEYDOWN and event.key == K_ESCAPE)):
            break
        mx, my = pygame.mouse.get_pos()
        mx, my = (mx - width / 2) / scale, (my - height / 2) / scale
        print('Calculating Julia set for ' + str(complex(mx, my)))
        for iy in range(height // 2 + 1):
            for ix in range(width):
                z = complex(float(ix - xaxis) / scale, float(iy - yaxis) / scale)
                c = complex(mx, my)
                # print(c)
                for i in range(iterations):
                    z = z ** 2 + c
                    if abs(z) > 2:
                        v = 765 * i / iterations
                        if v > 510:
                            color = (255, 255, v % 255)
                        elif v > 255:
                            color = (255, v % 255, 0)
                        else:
                            color = (v % 255, 0, 0)
                        break
                    else:
                        color = (0, 0, 0)

                screen.set_at((ix, iy), color)
                screen.set_at((width - ix, height - iy), color)

        pygame.display.update()


if __name__ == "__main__":
    main()
