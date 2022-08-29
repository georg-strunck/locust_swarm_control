#! C:\Own_Programs\Anaconda\envs\AIRR python 3.8
# -*- coding: utf-8 -*-
# 

import matplotlib.pyplot as plt
import numpy as np
import random

max_time    = 100
dt          = 0.1
t           = 0
display_x   = 100                           # environment length
display_y   = display_x                     # environment width
display_z   = display_x                     # environment height

max_l_speed = 10                            # max locust speed
max_p_speed = 10                            # max predator speed
# l_agility   = 0.2                           # 1 would allow instantaneous change of direction and velocity
# p_agility   = 0.05                          # 1 would allow instantaneous change of direction and velocity
det_range   = 80                            # visible range of locust
det_rng_pred= 40                            # Visible range of predator
anxiety     = 3.0                           # changes how far away the flock can be until individual speeds up to stay with them (larger number --> keep flock closer)
avoid_loc   = 0.1                          # looming cue threshold when avoidance kicks in
avoid_pred  = 0.01                          # looming cue threshold when avoidance of predators kicks in
cent_rate   = 0.4                           # Centroid rate = how much the centroid vs the alignment direction weighs of flocking
avoi_rate   = 0.4                           # Avoid rate = how much the Avoidance vs the flocking direction weighs desired direction
loc_rate    = 0.6                           # Locust rate = how much the locust speed vs the desired speed weighs
flee_rate   = 0.6                           # Flee rate = how much the predator avoid speed vs the ... speed weighs
n_locusts   = 50
n_predators = 10
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

while t <= max_time:
    # keep track of where we are
    locust_count = 0
    for locust in locusts:
        
        #region -- Don't exceed borders of screen #DO NOT USE!!?:
        # # don't exceed the small x border
        # if locust[0,0] < 0:
        #     locust[0,0] = 0
        #     #if the vel is in the wrong direction, redirect in other direction
        #     if locust[0,1] < 0:
        #         locust[0,1] = locust[0,1]*(-1)
        # # don't exceed the large x border
        # elif locust[0,0] > display_x:
        #     locust[0,0] = display_x
        #     #if the vel is in the wrong direction, redirect in other direction
        #     if locust[0,1] > 0:
        #         locust[0,1] = locust[0,1]*(-1)
        # # don't exceed the small y border
        # if locust[1,0] < 0:
        #     locust[1,0] = 0
        #     #if the vel is in the wrong direction, redirect in other direction
        #     if locust[1,1] < 0:
        #         locust[1,1] = locust[1,1]*(-1)
        # # don't exceed the large y border
        # elif locust[1,0] > display_y:
        #     locust[1,0] = display_y
        #     #if the vel is in the wrong direction, redirect in other direction
        #     if locust[1,1] > 0:
        #         locust[1,1] = locust[1,1]*(-1)
        # # don't exceed the small z border
        # if locust[2,0] < 0:
        #     locust[2,0] = 0
        #     #if the vel is in the wrong direction, redirect in other direction
        #     if locust[2,1] < 0:
        #         locust[2,1] = locust[2,1]*(-1)
        # # don't exceed the large z border
        # elif locust[2,0] > display_z:
        #     locust[2,0] = display_z
        #     #if the vel is in the wrong direction, redirect in other direction
        #     if locust[2,1] > 0:
        #         locust[2,1] = locust[2,1]*(-1)
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
        #region -- Calculate looming cue and incoming cue
        # Subtract the future distance from current distance --> if positive = incoming, larger number = faster
        cur_tot_dist = np.asarray(cur_tot_dist)
        fut_tot_dist = np.asarray(fut_tot_dist)
        incoming_cue = cur_tot_dist - fut_tot_dist
        
        # Calculate looming_cue, consisting of how fast object is approaching and how close it is
        looming_cue_unnorm = incoming_cue/cur_tot_dist
        # normalise looming_cue
        looming_cue = looming_cue_unnorm / np.linalg.norm(looming_cue_unnorm)
        #endregion
        #region -- Avoidance: Calculate direction in which to avoid all incoming, very close locusts --> with looming_cue > "0.05"/threshold
        # Array to store/add up the directions
        avoid_dir = np.zeros([1,3])
        # loop through every close contact
        for n in range(len(close_locusts)):
            # If only one entry, use non normalised looming cue (otherwise it is 1)
            if looming_cue.size == 1:
                avoid_dir += -close_loc_norm[n][:, 0] * looming_cue_unnorm[n]
            # Only take dangerous incomers --> larger looming_cue
            elif looming_cue[n] >= avoid_loc:
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
        if looming_cue.size >1 and np.max(looming_cue) >= avoid_loc:
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
        # If faster then max speed, set back to max speed
        if True:#(np.sqrt(speed_mag[0]**2 + speed_mag[1]**2 + speed_mag[2]**2)) > max_l_speed:
            speed_mag = max_l_speed * (speed_mag/np.linalg.norm(speed_mag))
        #endregion
        #region -- Calculate flocking direction and then speed direction:
        # Calc flocking direction, weighting centroid vs alignment
        flocking_dir = cent_rate * centroid_dir + (1-cent_rate) * alignment_dir

        #region Calc desired speed direction
        # If no one close by --> keep old direction
        if len(close_locusts) == 0:
            speed_dir = locust[:, 1]/np.linalg.norm(locust[:, 1])
        # If others nearby and danger --> flock to others and avoid danger
        elif np.max(looming_cue) >= avoid_loc:
            speed_dir = avoi_rate * avoid_dir + (1-avoi_rate) * flocking_dir
        # Else, all nearby others are safe:
        else:
            speed_dir = flocking_dir
        #endregion
        #endregion

        #region -- Avoid predators:

        #region - Calculate relative distance to predators:
        rel_pred = predators - locust
        #endregion
        #region - Calculate detectable predators
        close_pred = []
        for preda in rel_pred:
            if (np.sqrt(preda[0, 0]**2 + preda[1, 0]**2 + preda[2, 0]**2)) <= det_range:
                close_pred.append(preda)
        close_pred_norm = close_pred/(np.linalg.norm(close_pred))
        #endregion
        #region - Calculate future location of predators:
        fut_loc_pred = []
        for fut_l in close_pred:
            new_l = np.zeros([3,1])
            new_l[0,0] = fut_l[0,0] + fut_l[0,1]*dt
            new_l[1,0] = fut_l[1,0] + fut_l[1,1]*dt
            new_l[2,0] = fut_l[2,0] + fut_l[2,1]*dt
            fut_loc_pred.append(new_l)
        #endregion
        #region - Calculate current and future distances:
        cur_tot_dist_pred = []
        fut_tot_dist_pred = []
        for r in close_pred:
            cur_tot_dist_pred.append(np.sqrt(r[0, 0]*r[0, 0]+r[1, 0]*r[1, 0]+r[2, 0]*r[2, 0]))
        for s in fut_loc_pred:
            fut_tot_dist_pred.append(np.sqrt(s[0, 0]*s[0, 0]+s[1, 0]*s[1, 0]+s[2, 0]*s[2, 0]))
        #endregion
        #region - Calculate incoming cue of predators:
        cur_tot_dist_pred = np.asarray(cur_tot_dist_pred)
        fut_tot_dist_pred = np.asarray(fut_tot_dist_pred)
        incoming_cue_pred = cur_tot_dist_pred - fut_tot_dist_pred
        #endregion
        #region - Calculate looming cue of predators:
        lc_pred_unnorm = incoming_cue_pred/cur_tot_dist_pred
        # normalise looming_cue
        lc_pred = lc_pred_unnorm / np.linalg.norm(lc_pred_unnorm)
        #endregion
        #region - Calculate speed direction and magnitude:
        flee_dir = np.zeros([1, 3])
        pred_count = 0
        for t in range(len(close_pred)):
            if lc_pred[t] >= avoid_pred:
                flee_dir -= close_pred_norm[t][:, 0]
                pred_count +=1
        if np.sum(flee_dir) == 0:
            pass
        else:
            flee_dir /= pred_count
            flee_dir/(np.linalg.norm(flee_dir))
        if (np.linalg.norm(locust[:, 1])) < max_l_speed:
            flee_speed = max_l_speed
        else:
            flee_speed = np.linalg.norm(locust[:, 1])
        #endregion
        #endregion

        #region -- Option A or B: Simple LC +  centroid only, or, A+move away if too close:
        # locust[:, 1] = (- np.sum(looming_cue) * centroid * (1-loc_rate) + loc_rate* (locust[:, 1]/(np.linalg.norm(locust[:, 1]))))*max_l_speed
        # velo = (- np.sum(looming_cue) * centroid * (1-loc_rate) + loc_rate* (locust[:, 1]/(np.linalg.norm(locust[:, 1]))))*max_l_speed
        # #distance to centroid
        # dtc = np.sqrt(centroid[0][0]**2 + centroid[0][1]**2 + centroid[0][2]**2)
        # if dtc <(det_range*(1/3)):
        #     locust[:, 1] = - velo
        # else:
        #     locust[:, 1] = velo

        # New speed, avoiding predators:
        if pred_count !=0:
            zw = (- np.sum(looming_cue) * centroid * (1-loc_rate) + loc_rate* (locust[:, 1]/(np.linalg.norm(locust[:, 1]))))*max_l_speed
            locust[:, 1] = (1-flee_rate) * zw + flee_rate*flee_dir*flee_speed
        else:
            locust[:, 1] = (- np.sum(looming_cue) * centroid * (1-loc_rate) + loc_rate* (locust[:, 1]/(np.linalg.norm(locust[:, 1]))))*max_l_speed

        # new position based on old position and previous velocity*timestep
        locust[:, 0] += locust[:, 1] * dt

        #region -- Option C: New speed based on avoidance, alignment, flocking, centroid rules:
        # Update speed of locust
        #locust[:, 1] = loc_rate * locust[:, 1] + (1-loc_rate)* speed_dir*speed_mag
        #endregion
        #     
        # # random behaviour/predator
        # if np.random.uniform(-1,1)>= 0:
        #     index = random.randint(0, n_locusts-1)
        #     locust[:, 0] += det_range * 0.01

    for predator in predators:

        #region
        # Calculate locusts/prey relative speed and position:
        rel_prey = locusts - predator
        # Calculate closeby prey
        close_prey = []
        for prey in rel_prey:
            if np.linalg.norm(prey[:, 0]) <= det_rng_pred:
                close_prey.append(prey)
        
        # Find closest prey/locust:
        my_prey_dir = predator[:, 0]
        cl_count = 0
        for prey in rel_prey:
            prey_dist = np.linalg.norm(prey[:, 0])
            if prey_dist <= det_rng_pred:
                if cl_count == 0:
                    my_prey_dir = prey[:, 0]
                elif cl_count > 0 and np.linalg.norm(my_prey_dir[:]) > prey_dist :
                    my_prey_dir = prey[:, 0]
                cl_count += 1
        my_prey_dir /= np.linalg.norm(my_prey_dir)

        # Calculate centroid of prey swarm
        prey_centroid = np.zeros([1, 3])
        for u in close_prey:
            prey_centroid += u[:, 0]
        prey_centroid /= len(close_prey)
        prey_centroid /= np.linalg.norm(prey_centroid)
        #endregion

        # Update preadator direction and go at max speed:
        predator[:, 1] = my_prey_dir * max_p_speed              # go for closest locust
        # predator[:, 1] = prey_centroid * max_p_speed          # go for swarm/where most prey is

        # Update position
        predator[:, 0] += predator[:, 1] * dt


    # set limits anew, because everything cleared
    # ax.set_xlim(-display_x*3, display_x *3)
    # ax.set_ylim(-display_y*3, display_y *3)
    # ax.set_zlim(-display_z*3, display_z *3)   
    # plot new positions 
    ax.scatter([item[0,0] for item in locusts],
            [item[1,0] for item in locusts],
            [item[2,0] for item in locusts])
    
    ax.scatter([item[0,0] for item in predators],
            [item[1,0] for item in predators],
            [item[2,0] for item in predators])
    # wait to see image
    plt.pause(0.5)
    # clear all data for next positions
    ax.clear()
    # update time
    t += dt

plt.show()

# TODO: beware of being the only one in the list and flying towards yourself...
# TODO: instead of sqrt do np.öinalg.norm()
# TODO: limit max speed specifically