# AE4350 Locust Swarm control
# by Georg Strunck

import numpy as np
import matplotlib.pyplot as plt

class SetUp:

    def __init__(self, display_x, display_y, display_z, number_locusts):

        self.display_x = display_x
        self.display_y = display_y
        self.display_z = display_z
        self.n_locusts = number_locusts
        self.locusts_pos
        print('Initialized')

    def plot(self):

        fig = plt.figure()
        ax = plt.axes(projection ='3d')
        ax.set_xlim(0, self.display_x)
        ax.set_ylim(0, self.display_y)
        ax.set_zlim(0, self.display_z)

        plt.show()