import numpy

from particle import Particle


def rand_attr(attract_mean, attract_std):
    # attrs = numpy.random.normal(attract_mean, attract_std, 100)
    # return attrs[int(numpy.random.random() * 100)]
    return numpy.random.normal(attract_mean, attract_std)


def rand_minr(minr_lower, minr_upper):
    d = minr_upper - minr_lower
    return numpy.random.random() * d + minr_lower


def rand_maxr(maxr_lower, maxr_upper):
    d = maxr_upper - maxr_lower
    return numpy.random.random() * d + maxr_lower


# standard colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (125, 0, 0)
GREEN = (0, 125, 0)
BLUE = (0, 0, 125)


class Universe:
    def __init__(self, width=1700, height=860, rad=4, friction=0.03, num_types=4, num_particles=250,
                 minr_upper=16, maxr_lower=10, maxr_upper=80, attr_mean=0.2, attr_std=0.4, wrap_around=True):
        self.width = width
        self.height = height

        # particle radii
        self.RADIUS = rad
        self.DIAMETER = 2 * self.RADIUS
        self.R_SMOOTH = 2

        self.center_x = self.width * 0.5
        self.center_y = self.height * 0.5

        self.FRICTION = friction

        # types of particles
        self.num_types = num_types
        # particle count
        self.num_particles = num_particles

        # minr = how close particles can approach before repelling
        # maxr = how close particles will be affected until minr
        # minr range
        self.minr_lower = self.DIAMETER
        self.minr_upper = minr_upper
        # maxr range
        self.maxr_lower = maxr_lower
        self.maxr_upper = maxr_upper

        # attraction mean and standard deviation
        self.attr_mean = attr_mean
        self.attr_std = attr_std

        # world wrap
        self.wrap_around = wrap_around

        # types color attr minr maxr
        # 1st index = type number
        # 2nd index = list number
        # 3rd index = value
        # [(number)[color], [attr to each type], [minr to each type], [maxr to each type]]
        # [i][0][0] = (r, g, b)
        # [i][1][j] = attr to j
        # [i][2][j] = minr to j
        # [i][3][j] = maxr to j
        self.types = []

        # fill types with empty values
        for i in range(num_types):
            self.types.append([(0, 0, 0), [], [], []])
            for j in range(num_types):
                self.types[i][1].append(0)
                self.types[i][2].append(0)
                self.types[i][3].append(0)

        # set random types
        for i in range(num_types):
            print("type " + str(i), end="")

            # set color w/ arbitrary color distribution
            self.types[i][0] = (int(numpy.random.random() * 128 + 40),
                                int(numpy.random.random() * 128 + 40),
                                int(numpy.random.random() * 128 + 40))
            print(".", end="")  # color set
            for j in range(num_types):
                if i == j:
                    # always repel self (by negative attraction)
                    self.types[i][1][j] = -abs(rand_attr(attr_mean, attr_std * 2) * 0.5 + attr_std)
                    self.types[i][2][j] = self.DIAMETER
                else:
                    # set attraction between types i & j
                    rand = rand_attr(attr_mean, attr_std)
                    self.types[i][1][j] = rand
                    # set minr >= DIAMETER
                    self.types[i][2][j] = max(rand_minr(self.minr_lower, self.minr_upper), self.DIAMETER)
                # set maxr >= minr
                self.types[i][3][j] = max(rand_maxr(self.maxr_lower, self.maxr_upper), self.types[i][2][j])

                # make attr radii symmetric
                self.types[j][2][i] = self.types[i][2][j]
                self.types[j][3][i] = self.types[i][3][j]
                print(".", end="")  # type interaction set
                # print(self.types[i][1])
            print(" set.")

        for i in range(len(self.types)):
            print(i, self.types[i])

        self.particles = []
        # set random particles
        for i in range(num_particles):
            p_type = int(numpy.random.random() * len(self.types))
            p_x = (numpy.random.random() * 0.3) * self.width + (0.25 * self.width)
            p_y = (numpy.random.random() * 0.3) * self.height + (0.25 * self.height)
            p_vx = numpy.random.normal(0, 1)
            p_vy = numpy.random.normal(0, 1)
            self.particles.append(Particle(p_x, p_y, p_vx, p_vy, p_type))
