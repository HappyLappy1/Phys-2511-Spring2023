# -*- coding: utf-8 -*-
"""
Created on Wed Feb 15 12:09:33 2023

@author: parke
"""
import matplotlib.pyplot as plt
import numpy as np
import random as rn
# Need to guess the proper answer to actually use the debug. Capital Y, lowercase e, capital S.
bot_intelligent = False
enable_debug = False
if input("Enable debug? (Ill advised for automatic input): ") == "YeS":
    enable_debug = True
manual_aim = False
if input("Would you like to shoot the target manually? (Y/N): ") == "Y":
    print("Cool, here's your bow and arrow. Good luck!")
    manual_aim = True
elif input("That's unfortunate. I think I'll ask my pet snake to do it. Should I use my pet Python? If not, I will use my pet Anaconda... (Y/N): ") == "Y":
    print("Consider it done...")
    bot_intelligent = True
    attempts = 0
    feedback = []
else:
    print("This should be entertaining...")
    attempts = 0
    feedback = []
    pos = []
    v_max = 1000
    v_min = 0
    target_min = 0
# I will be using this to generate random targets, which are most likely to be in the center.
target_center = rn.triangular(0,1000.00000001)
g = 9.81 # m / s**2
step_size = 0.001
# I will be using a triangular random b value as well. between 0 and 10, of course. 
b = rn.triangular(1,10.00000001)
if enable_debug:    
    print("Target Center is at: " + str(target_center)+" m")
    print("The air resistance constant is: " + str(b))
while 1 > 0:    
    if manual_aim:
        v_init = float(input("Initial Velocity (m/s): "))
        # error-prevention, I will not be dealing with an archer shooting backwards or into the floor.
        fire_angle = float(input("Initial Angle (In Degrees): ")) % 90 
        # I have no problem with the archer shooting at a negative initial position, so no issue there.
        x_init = max(min(float(input("Initial Horizontal Position: ")),1000),-1000)
        # error-prevention, I will not have my archer shoot from below the floor.
        y_init = abs(int(input("Initial Vertical Position: ")))
    elif bot_intelligent:
        # Knowing that b is constant, and that the target is always to the right of the bow, there is no real need to aim anything but the x_init.
        # This intelligent-yet-boring bot will always land precisely in the center of the target in 3 shots, with a 50% chance to do so in 2. Not really blind, is it?
        v_init = 10
        fire_angle = 45
        y_init = 0
        # Fire from -10 initially, as the target might be exactly on 0. 
        if attempts == 0:
            x_init = -10
        elif attempts == 1:
            x_init = -10 + feedback[0]
        else:
            x_init = -10 - feedback[0]
    else:
        # It would be much more interesting if the bot had an x_init and y_init locked to 0, and was forced to modify only the v_init and fire_angle.
        x_init = 0
        y_init = 0
        # It is harder to code a "learning" bot with 2 variables than with one. Besides, this way it doesn't hit 90 and shoot itself.
        fire_angle = 45
        # I want the fire strength to be reasonable, but also completely random, becoming fine-tuned on subsequent attempts. 
        if attempts == 0:
            v_store = []
            repeat = False
            adjust_max = False
        else: 
            if repeat:
                if feedback[attempts - 1] > feedback[attempts - 2]:
                # Overshot! Now things get complicated!
                    adjust_max = True
                    v_max = v_store[attempts - 1]
                elif feedback[attempts - 1] < feedback[attempts - 2]:
                # Undershot!
                    v_min = max(v_store[attempts - 1],v_min)
                repeat = False
            # Assume vacuum pos is approximately accurate to air resistance pos. This assumption can be wildly wrong, but Anaconda needs the help...
            # is it impossible for us to undershoot? The target must be between 0 and 1000.
            elif pos[attempts - 1] - feedback[attempts - 1] < target_min:
            # Assume we undershot. Air resistance decreases our distance, so this condition is true regardless of b.
                v_min = max(v_store[attempts - 1],v_min)
            elif feedback[attempts - 1] < feedback[attempts - 2]:
                # We managed to hit further away than last time. We need more info to find out why that is. 
                repeat = True
            if repeat:
                # This attempt will be spent determining if the previous attempt was above or below the target.
                print("Min:",v_min,"Repeat!")
                v_init = v_store[attempts - 1] + 0.00001
            else:
                print("Min:",v_min)
                v_init = rn.triangular(v_min,(v_min + 1000)*(1-adjust_max)+(v_max*adjust_max),(v_min + 1000)*(1-adjust_max)+((v_max+v_min)/2)*adjust_max)
        v_store.append(v_init)
    vx_init = v_init * np.cos(fire_angle * np.pi/180)
    vy_init = v_init * np.sin(fire_angle * np.pi/180)
    # Calculate x first, so that we know when to stop for y
# With air res... In hindsight this should probably have been a function... 
    y_curr = y_init
    y_list = [y_init]
    vy_curr = vy_init
    vy_list = [vy_init]
    vy_prev = 0
    ay_curr = -g
    ay_list = [-g]
    t_curr = 0
    t_list = [t_curr]
    while ((y_curr > 0) or (t_curr == 0)):
        y_curr = y_curr + vy_curr * step_size
        y_list.append(y_curr)
        vy_prev = vy_curr
        vy_curr = vy_curr + ay_curr * step_size
        vy_list.append(vy_curr)
        ay_curr = -g - b * vy_prev
        ay_list.append(ay_curr)
        t_curr = t_curr + step_size
        t_list.append(t_curr)
    t_max = t_curr
    # If no air res...
    y_curr_vacuum = y_init
    y_list_vacuum = [y_init]
    vy_curr_vacuum = vy_init
    vy_list_vacuum = [vy_init]
    vy_prev_vacuum = 0
    ay_curr_vacuum = -g
    ay_list_vacuum = [-g]
    t_curr_vacuum = 0
    t_list_vacuum = [t_curr]
    while ((y_curr_vacuum > 0) or (t_curr_vacuum == 0)):
        y_curr_vacuum = y_curr_vacuum + vy_curr_vacuum * step_size
        y_list_vacuum.append(y_curr_vacuum)
        vy_prev_vacuum = vy_curr_vacuum
        vy_curr_vacuum = vy_curr_vacuum + ay_curr_vacuum * step_size
        vy_list_vacuum.append(vy_curr_vacuum)
        ay_curr_vacuum = -g
        ay_list_vacuum.append(ay_curr_vacuum)
        t_curr_vacuum = t_curr_vacuum + step_size
        t_list_vacuum.append(t_curr_vacuum)
    t_max_vacuum = t_curr_vacuum
    if enable_debug:
        # The Y acceleration jumping like that concerns me, but I think it's correct.
        fig, ax = plt.subplots()
        ax.set_xlabel("Time (s)")
        ax.set_title("Y position, Velocity, and Acceleration over Time (with and without Air Res.)")
        ax.plot(t_list,y_list,"r-",label = "True Y-Position (m)")
        ax.plot(t_list,vy_list,"g-", label = "True Y-Velocity (m/s)")
        ax.plot(t_list,ay_list,"b-", label = "True Y-Acceleration (m/s)")
        ax.legend()
        plt.show()
    x_curr = x_init
    x_list = [x_init]
    vx_curr = vx_init
    vx_list = [vx_init]
    vx_prev = 0
    ax_curr = 0
    ax_list = [0]
    t_curr = 0
    t_list = [t_curr]
    while (t_curr <= t_max):
        x_curr = x_curr + vx_curr * step_size
        x_list.append(x_curr)
        vx_prev = vx_curr
        vx_curr = vx_curr + ax_curr * step_size
        vx_list.append(vx_curr)
        ax_curr = - b * vx_prev
        ax_list.append(ax_curr)
        t_curr = t_curr + step_size
        t_list.append(t_curr)
        x_final = x_curr
    x_final_vacuum = x_init + vx_init * t_max_vacuum
    if enable_debug:
        fig, ax1 = plt.subplots()
# Not in the mood to debug whatever the heck was wrong with my copy/paste when I set b = 0. will just use constant velocity formula.
        ax1.set_xlabel("Time (s)")
        ax1.set_title("X position, Velocity, and Acceleration over Time (with and without Air Res.)")
        ax1.plot(t_list,x_list,"r-",label = "True X-Position (m)")
        ax1.plot(t_list,vx_list,"g-", label = "True X-Velocity (m/s)")
        ax1.plot(t_list,ax_list,"b-", label = "True X-Acceleration (m/s)")
        ax1.legend()
        plt.show()
    print("The shot landed " + str(abs(x_init - x_final)) + "m away, and " + str(max(abs(x_final-target_center),0.5)) + " m away from the target!")
    attempts = attempts + 1
    if enable_debug:
        print("the shot landed at " + str(x_final) + " m")
        print("If there were no air resistance, the shot would have landed at " + str(x_final_vacuum) + " m instead")
    if abs(x_final - target_center) < 0.5:
        print("The the target has been hit!")
        print("It took " + str(attempts) + " arrows to hit it!")
        break
    if manual_aim:    
        if input("Would you like to shoot again? (Y/N): ") == "Y":
            continue
        else:
            break
# I need less feedback for the smart bot
    elif bot_intelligent:
        feedback.append(abs(x_final - target_center))
    else:
# I think it would be fair to give the bot the final position from the bow, since I'm also giving that to the player.
        feedback.append(abs(x_final - target_center))
        pos.append(abs(x_init - x_final))