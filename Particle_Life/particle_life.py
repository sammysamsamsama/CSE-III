import math
import threading

import pygame

from particle_universe import *

pygame.init()

universe = Universe()

particles = []
for i in range(universe.num_types):
    particles.append(0)
for p in universe.particles:
    particles[p.p_type] += 1
print(particles)

particles = universe.particles


def calculate(a=0, b=len(particles)):
    # update forces and velocities
    for i in range(a, b):
        # current particle
        p = particles[i]

        for j in range(len(particles)):
            # other particle
            q = particles[j]

            # if x or y coincide
            # if p.x == q.x and p.y == q.y:
            #     p.vx = -p.vx
            #     q.vx = -q.vx
            #     p.vy = -p.vy
            #     q.vy = -q.vy

            # delta x and delta y
            dx = q.x - p.x
            dy = q.y - p.y
            # if the world wraps around, find the shorter distance
            if universe.wrap_around:
                if dx > universe.width * 0.5:
                    dx -= universe.width
                elif dx < -universe.width * 0.5:
                    dx += universe.width

                if dy > universe.height * 0.5:
                    dy -= universe.height
                elif dy < -universe.height * 0.5:
                    dy += universe.height

            # distance squared
            r2 = (dx ** 2) + (dy ** 2)
            minr = universe.types[p.p_type][2][q.p_type]
            maxr = universe.types[p.p_type][3][q.p_type]

            # if distance is too extreme, ignore particle
            if r2 > maxr ** 2:
                continue
            # if r2 < minr ** 2:
            #     print(dx, dy, math.sqrt(r2), minr)
            #     continue

            # normalize displacement
            # r is exact distance
            # dx and dy now fractions of r
            r = math.sqrt(r2)
            if r != 0:
                dx /= r
                dy /= r

            # calculate force
            if r > minr:
                # print(r, minr)
                # numerator = 2 * |distance - avg(maxr, minr)|
                #           =   0 @ distance = avg(maxr, minr)
                #           = max @ distance ~ minr or maxr
                numer = 2 * abs(r - 0.5 * (maxr + minr))
                # denomenator = distance between minr and maxr
                denom = maxr - minr
                # (1 - numer / denom) = 1 @ avg dist
                #                     = 0 @ minr or maxr
                f = universe.types[p.p_type][1][q.p_type] * (1 - numer / denom)
            else:
                f = 5 * universe.R_SMOOTH * minr * ((1 / (minr + universe.R_SMOOTH)) - (1 / (r + universe.R_SMOOTH)))
                # f = 1 - r / minr
                # print(2, f)

            # apply force
            p.vx += f * dx
            p.vy += f * dy

            # # calculate position
            # px = p.x + p.vx
            # py = p.y + p.vy
            # qx = q.x + q.vx
            # qy = q.y + q.vy
            #
            # # check wall collision
            # if universe.wrap_around:
            #     if px < 0:
            #         px = universe.width - universe.RADIUS
            #     elif px > universe.width:
            #         px = universe.RADIUS
            #
            #     if py < 0:
            #         py = universe.height - universe.RADIUS
            #     elif py > universe.height:
            #         py = universe.RADIUS
            #
            #     if qx < 0:
            #         qx = universe.width - universe.RADIUS
            #     elif qx > universe.width:
            #         qx = universe.RADIUS
            #
            #     if qy < 0:
            #         qy = universe.height - universe.RADIUS
            #     elif qy > universe.height:
            #         qy = universe.RADIUS
            #
            # else:
            #     # only edge can touch the wall
            #     if px < universe.RADIUS:
            #         px = universe.RADIUS
            #     elif px > universe.width - universe.RADIUS:
            #         px = universe.width - universe.RADIUS
            #
            #     if py < universe.RADIUS:
            #         py = universe.RADIUS
            #     elif py > universe.height - universe.RADIUS:
            #         py = universe.height - universe.RADIUS
            #
            #     if qx < universe.RADIUS:
            #         qx = universe.RADIUS
            #     elif qx > universe.width - universe.RADIUS:
            #         qx = universe.width - universe.RADIUS
            #
            #     if qy < universe.RADIUS:
            #         qy = universe.RADIUS
            #     elif qy > universe.height - universe.RADIUS:
            #         qy = universe.height - universe.RADIUS
            #
            # # bigger = greater abs value of attr
            # bigger = universe.types[p.p_type][1][q.p_type] if abs(universe.types[p.p_type][1][q.p_type]) > abs(
            #     universe.types[q.p_type][1][p.p_type]) else universe.types[q.p_type][1][p.p_type]
            # c = RED if bigger < 0 else GREEN
            # pygame.draw.aaline(screen, c, [px, py], [qx, qy])


size = (universe.width, universe.height)
screen = pygame.display.set_mode(size)

pygame.display.set_caption("Particle Life")

# for looping purposes
done = False

# for managing screen update speed
clock = pygame.time.Clock()

while not done:
    for event in pygame.event.get():
        # if the user clicked close
        if event.type == pygame.QUIT:
            # we are done, exit loop
            done = True

    # BLANK SCREEN for new drawing
    screen.fill(BLACK)

    # calculate all forces and velocities
    thread1 = threading.Thread(target=calculate(0, len(particles) // 4))
    thread2 = threading.Thread(target=calculate(1 * len(particles) // 4, 2 * len(particles) // 4))
    thread3 = threading.Thread(target=calculate(2 * len(particles) // 4, 3 * len(particles) // 4))
    thread4 = threading.Thread(target=calculate(3 * len(particles) // 4, len(particles)))

    thread1.start()
    thread2.start()
    thread3.start()
    thread4.start()

    # update positions
    for i in range(len(particles)):
        p = particles[i]

        # update position and velocity
        p.x += p.vx
        p.y += p.vy
        p.vx *= 1 - universe.FRICTION
        p.vy *= 1 - universe.FRICTION

        # check wall collision
        if universe.wrap_around:
            if p.x < 0:
                p.x = universe.width - universe.RADIUS
            elif p.x > universe.width:
                p.x = universe.RADIUS

            if p.y < 0:
                p.y = universe.height - universe.RADIUS
            elif p.y > universe.height:
                p.y = universe.RADIUS

        else:
            # only edge can touch the wall
            if p.x < universe.RADIUS:
                p.x = universe.RADIUS
                p.vx = -p.vx
            elif p.x > universe.width - universe.RADIUS:
                p.x = universe.width - universe.RADIUS
                p.vx = -p.vx

            if p.y < universe.RADIUS:
                p.y = universe.RADIUS
                p.vy = -p.vy
            elif p.y > universe.height - universe.RADIUS:
                p.y = universe.height - universe.RADIUS
                p.vy = -p.vy

    # drawing code goes here
    for i in range(len(universe.particles)):
        color = universe.types[universe.particles[i].p_type][0]
        x = int(universe.particles[i].x)
        y = int(universe.particles[i].y)
        pygame.draw.circle(screen, color, [x, y], universe.RADIUS)

    # update screen drawing
    pygame.display.flip()

    # limit 60 fps
    clock.tick(60)

pygame.quit()
