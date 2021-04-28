"""
Various datasets for experiments

@author: HENRI DE PLAEN
@copyright: KU LEUVEN
@license: MIT
@date: March 2021
"""

import numpy as np
import math
from sklearn import datasets

class data():
    @staticmethod
    def gaussians():
        size = 100
        s1, m1 = .7, (2, 1)
        s2, m2 = 1.2, (-2, -3)

        g1 = np.random.normal(m1, s1, (size, 2))
        g2 = np.random.normal(m2, s2, (size, 2))

        x = np.concatenate((g1[:, 0], g2[:, 0]))
        y = np.concatenate((g1[:, 1], g2[:, 1]))
        c = np.concatenate((np.repeat(0, size), np.repeat(1, size)))

        input = np.concatenate((g1, g2))
        target = np.concatenate((np.repeat(-1, size), np.repeat(1, size)))

        return input, target

    @staticmethod
    def spiral():
        def spiral_xy(i, spiral_num):
            """
            Create the data for a spiral.

            Arguments:
                i runs from 0 to 96
                spiral_num is 1 or -1
            """
            φ = i / 16 * math.pi
            r = 70 * ((104 - i) / 104)
            x = (r * math.cos(φ) * spiral_num) / 13 + 0.5
            y = (r * math.sin(φ) * spiral_num) / 13 + 0.5
            return (x, y)

        def spiral(spiral_num):
            return [spiral_xy(i, spiral_num) for i in range(97)]

        s1 = spiral(1)
        s2 = spiral(-1)

        input = np.concatenate((s1, s2))
        target = np.concatenate((np.repeat(-1, 97), np.repeat(1, 97)))
        r = (-5, 6, -5, 5)

        return input, target, r

    @staticmethod
    def two_moons(n_samples=350):
        input, output = datasets.make_moons(n_samples, noise=.1)
        output = np.where(output == 0, -1, 1)
        range = (-4, 7, -4, 4)
        return 2.5 * input, output, range

    @staticmethod
    def usps():
        digits = datasets.load_digits(2)
        x = digits['data']
        y = digits['target']
        y = np.where(y == 0, -1, 1)
        r = (0, 1, 0, 1)
        return x, y, r