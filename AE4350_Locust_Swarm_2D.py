#! C:\Own_Programs\Anaconda\envs\AIRR python 3.8
# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import numpy as np
import random

max_time    = 100
dt          = 0.1
t           = 0

n_locusts   = 20
display_x   = 100                           # environment length
display_y   = display_x                     # environment width
display_z   = display_x                     # environment height
max_l_speed = 30                            # max locust speed
max_p_speed = 50                            # max predator speed
l_agility   = 0.2                           # 1 would allow instantaneous change of direction and velocity
p_agility   = 0.05                          # 1 would allow instantaneous change of direction and velocity
det_range   = 20                            # visible range of locust

locusts_pos     = []
locusts_vel     = []

#region -- Populate locust and predator position and velocities
for i in range(n_locusts):
    # random position between 0 and display_x
    pos =  np.random.rand(1,2) * display_x
    # random velocity between -max_l_speed and +max_l_speed
    vel = np.random.uniform(-1,1, size=2) * max_l_speed
    locusts_pos.append(pos)
    locusts_vel.append(vel)
#print(locusts_vel)
# endregion

fig = plt.figure()
ax = plt.axes()

while t <= max_time:

    for loc_ind in range(n_locusts):
        # New position of locusts:
        # Wasn't able to nicely multiply in while loop, so did position here bit by bit in for loop
        locusts_pos[loc_ind] = locusts_pos[loc_ind] + locusts_vel[loc_ind]*dt

        #print('before', locusts_vel)
        # New velocity of locust: 
        # TODO: beetje raar, vgm verandert die array size niet, maar if uncommented werkt de border niet meer/error
        locusts_vel[loc_ind] = locusts_vel[loc_ind] * (1-l_agility) + np.ones((1,2)) * np.random.uniform(-1,1, size=2) * max_l_speed * l_agility
        #print('after', locusts_vel)

        #region -- Don't exceed borders of screen:
        # don't exceed the small x border
        if locusts_pos[loc_ind][0, 0] < 0:
            locusts_pos[loc_ind][0, 0] = 0
            #if the vel is in the wrong direction, redirect in other direction
            if locusts_vel[loc_ind][0, 0] < 0:
                locusts_vel[loc_ind][0, 0] *= -1
        # don't exceed the large x border
        elif locusts_pos[loc_ind][0, 0] > display_x:
            locusts_pos[loc_ind][0, 0] = display_x
            #if the vel is in the wrong direction, redirect in other direction
            if locusts_vel[loc_ind][0, 0] > 0:
                locusts_vel[loc_ind][0, 0] *= -1
        # don't exceed the small y border
        if locusts_pos[loc_ind][0, 1] < 0:
            locusts_pos[loc_ind][0, 1] = 0
            #if the vel is in the wrong direction, redirect in other direction
            if locusts_vel[loc_ind][0, 1] < 0:
                locusts_vel[loc_ind][0, 1] *= -1
        # don't exceed the large y border
        elif locusts_pos[loc_ind][0, 1] > display_y:
            locusts_pos[loc_ind][0, 1] = display_y
            #if the vel is in the wrong direction, redirect in other direction
            if locusts_vel[loc_ind][0, 1] > 0:
                locusts_vel[loc_ind][0, 1] *= -1
        #endregion


    # set limits anew, because everything cleared
    ax.set_xlim(-5, display_x + 5)
    ax.set_ylim(-5, display_y + 5)
    # ax.set_zlim(-5, display_z + 5)   
    # plot new positions 
    ax.scatter([item[0,0] for item in locusts_pos],
               [item[0,1] for item in locusts_pos])
    # wait to see image
    plt.pause(0.01)
    # clear all data for next positions
    ax.clear()
    # update time
    t += dt

plt.show()