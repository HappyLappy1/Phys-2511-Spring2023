# -*- coding: utf-8 -*-
"""
Created on Tue Feb 21 13:57:03 2023

@author: parke
"""
import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
# f1_x is -0.5x + 4.0
# f2_x is -0.29x^2 -x + 12.5
# f3_x is 1.0 + 10(x+1.0)*Exp[-x^2]

def generate_delta_x(mini,maxi,step_size):
    return np.arange(mini,maxi,step_size)

def f1(x):
    return -0.5*x + 4.0

def f2(x):
    return -0.29 * x * x - x + 12.5

def f3(x):
    return 1 + 10 * (x + 1.0) * np.exp(-1 * x*x)

def f_of_x(x,case):
    if case == 1:
        return f1(x)
    elif case == 2:
        return f2(x)
    else:
        return f3(x)

def F_of_x(delta_x,case,a,b):
    # delta_x is a dummy input only used for the loop. Has no purpose in this function
    if case == 1:
        return sp.integrate.quadrature(f1,a,b)
    elif case == 2:
        return sp.integrate.quadrature(f2,a,b)
    else:
        return sp.integrate.quadrature(f3,a,b)

def left_hand_sum(delta_x,a,b,case):
    x_array = np.arange(a, b, delta_x)
    y_array = f_of_x(x_array,case)
    area_individual = y_array*delta_x
    return np.sum(area_individual)

def right_hand_sum(delta_x,a,b,case):
    x_array = np.arange(a+delta_x, b+delta_x, delta_x)
    y_array = f_of_x(x_array,case)
    area_individual = y_array*delta_x
    return np.sum(area_individual)

def midpoint_sum(delta_x,a,b,case):
    x_array = np.arange(a+(delta_x/2), b+(delta_x/2), delta_x)
    y_array = f_of_x(x_array,case)
    area_individual = y_array*delta_x
    return np.sum(area_individual)

try:
    a = float(input("a value (leave blank for default -5): "))
except: 
    a = -5
try:
    b = float(input("b value (leave blank for default 5): "))
except:
    b = 5
try:
    delta_x_min = float(input("\u0394x Min (leave blank for default 0.001): "))
except:
    delta_x_min = 0.001
try:
    delta_x_max = float(input("\u0394x Max (leave blank for default 1): "))
except:
    delta_x_max = 1
try:
    delta_delta_x = float(input("\u0394x step size (leave blank for default 0.0005): "))
except:
    delta_delta_x = 0.0005

delta_x = generate_delta_x(delta_x_min, delta_x_max,delta_delta_x)
print("f1: y = 0.5x + 4.0 \nf2: y = -0.29x\u00B2 - x + 12.5\nf3: y = 1 + 10(x + 1.0)e\u207B\u02E3\u207D\u02E3\u207E")
try:
    case = int(input("Which function would you like to see the Rieman sums of? select with (1/2/3, leave blank for default 3): "))
except:
    case = 3
lhs = []
rhs = []
mps = []
quadr_estimate = []
for i in delta_x:
    lhs.append(left_hand_sum(i,a,b,case))
    rhs.append(right_hand_sum(i,a,b,case))
    mps.append(midpoint_sum(i,a,b,case))
    quadr_estimate.append(F_of_x(i,case,a,b)[0])
reeman_estimate = []
for i in range(len(lhs)):
    reeman_estimate.append((lhs[i]+rhs[i]+mps[i])/3)
# Now to calculate percent error between Reimann and Quadrature. 
# This will tell me how close my estimate is to scipy's
reeman_error = []
for i in range(len(reeman_estimate)):
    reeman_error.append(abs(quadr_estimate[i]-reeman_estimate[i])/quadr_estimate[i])
reeman_error_np = np.asarray(reeman_error)
fig, ax1 = plt.subplots()
ax1.plot(reeman_estimate,quadr_estimate)
ax1.plot(reeman_estimate,quadr_estimate)
ax1.set_ylabel("Quadrature Estimate")
ax1.set_xlabel("Riemann Sum Estimate")
ax1.set_title("Riemann Sums vs. Quadrature Sums (Equation f" + str(case) + ")")
plt.show()
fig, ax = plt.subplots()
ax.plot(delta_x,reeman_error_np)
ax.set_ylabel("Error for Average of Riemann Sums")
ax.set_xlabel("\u0394x value used in Riemann Sums")
ax.set_title("Riemann Sums Step Size vs. Error Value (Equation f" + str(case) + ")")
plt.show()