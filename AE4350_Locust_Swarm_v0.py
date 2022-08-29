#! C:\Own_Programs\Anaconda\envs\AIRR python 3.8
# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import numpy as np
import random

max_time    = 100
dt          = 0.1
t           = 0

n_locusts   = 50
n_predators = 2

display_x   = 100                           # environment length
display_y   = display_x                     # environment width
display_z   = display_x                     # environment height
max_l_speed = 5                #            # max locust speed
max_p_speed = 50                            # max predator speed
l_agility   = 0.2                           # 1 would allow instantaneous change of direction and velocity
p_agility   = 0.05                          # 1 would allow instantaneous change of direction and velocity
det_range   = 80                #            # visible range of locust
anxiety     = 1.5                           # changes how far away the flock can be until individual speeds up to stay with them (larger number --> keep flock closer)
avoid_thr   = 0.08                          # looming cue threshold when avoidance kicks in
cent_rate   = 0.01                           # Centroid rate = how much the centroid vs the alignment direction weighs of flocking
avoi_rate   = 0.9                           # Avoid rate = how much the Avoidance vs the flocking direction weighs desired direction
loc_rate    = 0.4                 #          # Locust rate = how much the locust speed vs the desired speed weighs



locusts     = []
predators   = []

#region -- Populate locust and predator position and velocities
for i in range(n_locusts):
    # create array of size 3x2 filled with ones
    l = np.ones((3,2))
    # random position between 0 and display_x
    l[:, 0] = l[:, 0] * np.random.rand(1,3) * display_x
    # random velocity between -max_l_speed and +max_l_speed
    l[:, 1] = l[:, 1] * np.random.uniform(-1,1, size=3) * max_l_speed
    locusts.append(l)

for j in range(n_predators):
    p = np.ones((3,2))
    p[:, 0] = p[:, 0] * np.random.rand(1,3) * display_x
    p[:, 1] = p[:, 1] * np.random.uniform(-1,1, size=3) * max_p_speed
    predators.append(p)
# endregion



fig = plt.figure()
ax = plt.axes(projection ='3d')

# ax.scatter([item[0,0] for item in predators],
#             [item[1,0] for item in predators],
#             [item[2,0] for item in predators])



while t <= max_time:
    # keep track of where we are
    locust_count = 0
    captain = locusts[0][:, 1]
    for locust in locusts:
        
        #region -- Don't exceed borders of screen:
        # don't exceed the small x border
        if locust[0,0] < 0:
            locust[0,0] = 0
            #if the vel is in the wrong direction, redirect in other direction
            if locust[0,1] < 0:
                locust[0,1] = locust[0,1]*(-1)
        # don't exceed the large x border
        elif locust[0,0] > display_x:
            locust[0,0] = display_x
            #if the vel is in the wrong direction, redirect in other direction
            if locust[0,1] > 0:
                locust[0,1] = locust[0,1]*(-1)
        # don't exceed the small y border
        if locust[1,0] < 0:
            locust[1,0] = 0
            #if the vel is in the wrong direction, redirect in other direction
            if locust[1,1] < 0:
                locust[1,1] = locust[1,1]*(-1)
        # don't exceed the large y border
        elif locust[1,0] > display_y:
            locust[1,0] = display_y
            #if the vel is in the wrong direction, redirect in other direction
            if locust[1,1] > 0:
                locust[1,1] = locust[1,1]*(-1)
        # don't exceed the small z border
        if locust[2,0] < 0:
            locust[2,0] = 0
            #if the vel is in the wrong direction, redirect in other direction
            if locust[2,1] < 0:
                locust[2,1] = locust[2,1]*(-1)
        # don't exceed the large z border
        elif locust[2,0] > display_z:
            locust[2,0] = display_z
            #if the vel is in the wrong direction, redirect in other direction
            if locust[2,1] > 0:
                locust[2,1] = locust[2,1]*(-1)
        #endregion

        #region -- Create array with relative displacement and velocity:
        rel_locusts = locusts - locust
        # delete own '0' entry
        rel_locusts = np.delete(rel_locusts, locust_count, 0)
        # update count
        locust_count += 1
        #endregion

        #region -- Store which locusts are closeby within visible/detection range:
        close_locusts = []
        for i in rel_locusts:
            # if the other locust is within visible detection_range, store its info
            if np.sqrt(i[0, 0]*i[0, 0]+i[1, 0]*i[1, 0]+i[2, 0]*i[2, 0]) <= det_range:
                close_locusts.append(i)
        #endregion
        
        #region -- Create normalized relative displacement and velocity of closeby locusts
        if len(close_locusts) == 0:
            close_loc_norm = 0
        else:
            temp_norm = np.linalg.norm(close_locusts, axis=1)
            close_loc_norm = []
            for nor in range(len(close_locusts)):
                close_loc_norm.append(close_locusts[nor] / temp_norm[nor])
        #endregion

        #region -- Calc next position of closeby locusts:
        fut_locations = []
        for j in close_locusts:
            new = np.zeros([3,1])
            new[0,0] = j[0,0] + j[0,1]*dt
            new[1,0] = j[1,0] + j[1,1]*dt
            new[2,0] = j[2,0] + j[2,1]*dt
            fut_locations.append(new)
        #endregion

        #region -- Calc current and future total relative distance of closeby locusts:
        cur_tot_dist = []
        fut_tot_dist = []
        for k in close_locusts:
            cur_tot_dist.append(np.sqrt(k[0, 0]*k[0, 0]+k[1, 0]*k[1, 0]+k[2, 0]*k[2, 0]))
        for m in fut_locations:
            fut_tot_dist.append(np.sqrt(m[0, 0]*m[0, 0]+m[1, 0]*m[1, 0]+m[2, 0]*m[2, 0]))
        #endregion
        
        # Subtract the future distance from current distance --> if positive = incoming, larger number = faster
        cur_tot_dist = np.asarray(cur_tot_dist)
        fut_tot_dist = np.asarray(fut_tot_dist)
        incoming_cue = cur_tot_dist - fut_tot_dist
        
        # Calculate looming_cue, consisting of how fast object is approaching and how close it is
        looming_cue_unnorm = incoming_cue/cur_tot_dist
        # normalise looming_cue
        looming_cue = looming_cue_unnorm / np.linalg.norm(looming_cue_unnorm)
        
        #region -- Avoidance: Calculate direction in which to avoid all incoming, very close locusts --> with looming_cue > "0.05"/threshold
        # Array to store/add up the directions
        avoid_dir = np.zeros([1,3])
        # loop through every close contact
        for n in range(len(close_locusts)):
            # If only one entry, use non normalised looming cue (otherwise it is 1)
            if looming_cue.size == 1:
                avoid_dir += -close_loc_norm[n][:, 0] * looming_cue_unnorm[n]
            # Only take dangerous incomers --> larger looming_cue
            elif looming_cue[n] >= avoid_thr:
                # Add all the negative (for avoiding) directions * with looming cue for weighting together
                avoid_dir += -close_loc_norm[n][:, 0] * looming_cue[n]
        # Normalize the direction for simple speed multiplication later, only if nonzero, otherwise bad division
        if len(close_locusts)>0:
            avoid_dir = avoid_dir / np.linalg.norm(avoid_dir)
        #endregion

        #region -- Alignment: Calculate averaage swarm speed and direction, use norm for direction, not actual speed
        alignment_dir = np.zeros([1, 3])
        if close_loc_norm == 0:
            pass
        else:
            for o in close_loc_norm:
                alignment_dir += o[:, 1]
            # Divide by number of locusts to get average
            alignment_dir/= (len(close_loc_norm))
        #endregion
        
        #region -- Centroid: Calculate the average centroid of the swarm
        centroid = np.zeros([1, 3])
        if close_loc_norm == 0:
            centroid_dir = centroid
            pass
        else:
            for p in close_locusts:
                centroid += p[:, 0]
            # Divide by number of locusts to get average
            centroid = centroid/(len(close_locusts))
            centroid_dir = centroid/np.linalg.norm(centroid)
        #endregion

        #region -- Speed: Calculate desired speed magnitude
        speed_mag = 0
        # If more than two incoming dangerous points, increase speed to that speed
        if looming_cue.size >1 and np.max(looming_cue) >= avoid_thr:
            # ac    = close_locusts[looming_cue.argmax(axis=0)][:, 1]
            # speed_mag = (np.sqrt(ac[0]**2 + ac[1]**2 + ac[2]**2))
            speed_mag = close_locusts[looming_cue.argmax(axis=0)][:, 1]
        # If there are no closeby locusts, stay at same speed
        elif len(close_locusts) == 0:
            speed_mag = locust[:, 1]
        # if no danger and others detected, adjust speed to their speed
        else:
            for q in close_locusts:
                speed_mag += q[:, 1]
            # Anxiety: speed up of others are too far away
            if np.sqrt(centroid[0][0]**2 + centroid[0][1]**2 + centroid[0][2]**2) >= (det_range/anxiety) and np.sqrt(speed_mag[0]**2 + speed_mag[1]**2 + speed_mag[2]**2) < max_l_speed:
                speed_mag += (max_l_speed/3)
            speed_mag /= len(close_locusts)
        #endregion

        # Calc flocking direction, weighting centroid vs alignment
        flocking_dir = cent_rate * centroid_dir + (1-cent_rate) * alignment_dir

        #region Calc desired speed direction
        # If no one close by --> keep old direction
        if len(close_locusts) == 0:
            speed_dir = locust[:, 1]/np.linalg.norm(locust[:, 1])
        # If others nearby and danger --> flock to others and avoid danger
        elif np.max(looming_cue) >= avoid_thr:
            speed_dir = avoi_rate * avoid_dir + (1-avoi_rate) * flocking_dir
        # Else, all nearby others are safe:
        else:
            speed_dir = flocking_dir
        #endregion

        # region -- only LC +pos
        #print(incoming_cue)
        locust[:, 1] = (- np.sum(looming_cue) * centroid * (1-loc_rate) + loc_rate* (locust[:, 1]/(np.linalg.norm(locust[:, 1]))))*max_l_speed
        #distance to centroid
        # dtc = np.sqrt(centroid[0][0]**2 + centroid[0][1]**2 + centroid[0][2]**2)
        # if dtc <(det_range*(1/3.5)):
        #     locust[:, 1] = locust[:, 1]
        # else:
        #     locust[:, 1] = (- np.sum(looming_cue) * centroid * (1-loc_rate) + loc_rate* (locust[:, 1]/(np.linalg.norm(locust[:, 1]))))*max_l_speed

        
        #endregion

        # Update speed of locust
        # print('loc', locust[:, 1])
        # print(speed_dir*speed_mag)
        #locust[:, 1] = loc_rate * locust[:, 1] + (1-loc_rate)* speed_dir*speed_mag
        # new position based on old position and previous velocity*timestep
        locust[:, 0] += locust[:, 1] * dt

        # random behaviour/predator
        if np.random.uniform(-1,1)>= 0:
            index = random.randint(0, n_locusts-1)
            locust[:, 0] += det_range * 0.01
    #locusts[0][:, 1]=captain# * (1-l_agility) + np.ones((1,3)) * np.random.uniform(-1,1, size=3) * max_l_speed * l_agility

    # set limits anew, because everything cleared
    ax.set_xlim(-50, display_x + 50)
    ax.set_ylim(-50, display_y + 50)
    ax.set_zlim(-50, display_z + 50)   
    # plot new positions 
    ax.scatter([item[0,0] for item in locusts],
            [item[1,0] for item in locusts],
            [item[2,0] for item in locusts])
    # wait to see image
    plt.pause(0.01)
    # clear all data for next positions
    ax.clear()
    # update time
    t += dt

plt.show()

# TODO: beware of being the only one in the list and flying towards yourself...
# TODO: instead of sqrt do np.öinalg.norm()
# TODO: limit max speed specifically