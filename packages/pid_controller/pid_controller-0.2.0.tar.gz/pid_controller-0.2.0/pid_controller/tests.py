#!/usr/bin/python
from __future__ import print_function

import unittest
import random
from math import pi, sin, cos, tan

from six.moves import range

from .pid import PID, twiddle

class Robot(object):

    # --------
    # init: 
    #    creates robot and initializes location/orientation to 0, 0, 0
    #

    def __init__(self, length=20.0):
        self.x = 0.0
        self.y = 0.0
        self.orientation = 0.0
        self.length = length
        self.steering_noise = 0.0
        self.distance_noise = 0.0
        self.steering_drift = 0.0

    # --------
    # set: 
    #    sets a robot coordinate
    #

    def set(self, new_x, new_y, new_orientation):

        self.x = float(new_x)
        self.y = float(new_y)
        self.orientation = float(new_orientation) % (2.0 * pi)


    # --------
    # set_noise: 
    #    sets the noise parameters
    #

    def set_noise(self, new_s_noise, new_d_noise):
        # makes it possible to change the noise parameters
        # this is often useful in particle filters
        self.steering_noise = float(new_s_noise)
        self.distance_noise = float(new_d_noise)

    # --------
    # set_steering_drift: 
    #    sets the systematical steering drift parameter
    #

    def set_steering_drift(self, drift):
        self.steering_drift = drift
        
    # --------
    # move: 
    #    steering = front wheel steering angle, limited by max_steering_angle
    #    distance = total distance driven, most be non-negative

    def move(self, steering, distance, 
        tolerance=0.001, max_steering_angle=pi/4.0):

        if steering > max_steering_angle:
            steering = max_steering_angle
        if steering < -max_steering_angle:
            steering = -max_steering_angle
        if distance < 0.0:
            distance = 0.0

        # make a new copy
        res = type(self)()
        res.length = self.length
        res.steering_noise = self.steering_noise
        res.distance_noise = self.distance_noise
        res.steering_drift = self.steering_drift

        # apply noise
        steering2 = random.gauss(steering, self.steering_noise)
        distance2 = random.gauss(distance, self.distance_noise)

        # apply steering drift
        steering2 += self.steering_drift

        # Execute motion
        turn = tan(steering2) * distance2 / res.length

        if abs(turn) < tolerance:

            # approximate by straight line motion

            res.x = self.x + (distance2 * cos(self.orientation))
            res.y = self.y + (distance2 * sin(self.orientation))
            res.orientation = (self.orientation + turn) % (2.0 * pi)

        else:

            # approximate bicycle model for motion

            radius = distance2 / turn
            cx = self.x - (sin(self.orientation) * radius)
            cy = self.y + (cos(self.orientation) * radius)
            res.orientation = (self.orientation + turn) % (2.0 * pi)
            res.x = cx + (sin(res.orientation) * radius)
            res.y = cy - (cos(res.orientation) * radius)

        return res

    def __repr__(self):
        return '[x=%.5f y=%.5f orient=%.5f]'  % (self.x, self.y, self.orientation)

def run_robot(p, i, d, verbose=False):
    pid = PID(p=p, i=i, d=d)
    
    # We want to drive the robot towards the 0 on the y-axis.
    pid.target = 0
    
    robot = Robot()
    robot.set(0.0, 1.0, 0.0)
    speed = 1.0 # 1 unit/sec, motion distance is equal to speed (we assume time = 1)
    N = 300
    
    # 10 degree bias, this will be added in by the move function, you do not need to add it below!
    robot.set_steering_drift(10.0 / 180.0 * pi)
    
    for step in range(N):
        #Y = robot.y - 0 # error
        #cte_sum += Y#should be here?
        #alpha = -tau_p * Y - tau_d * (Y - Y_last) - tau_i * cte_sum
        alpha = pid(feedback=robot.y, curr_tm=step*speed)
        robot = robot.move(steering=alpha, distance=speed)
        if verbose:
            print('robot:', robot, alpha, pid.error)

    return pid.error

class Tests(unittest.TestCase):
    
    def setUp(self):
        pass

    def test_robot_steering(self):
        
        initial_guess = (0.2, 0.004, 3.0)
        err0 = run_robot(*initial_guess, verbose=False)
        
        
        best_params = twiddle(
            evaluator=run_robot,
            params=3,
            tol=0.001,
            initial_guess=(0.2, 0.004, 3.0))
        err1 = run_robot(*best_params, verbose=True)
        print(best_params, err1)
        
        print('err0:', err0)
        print('err1:', err1)
    
        self.assertTrue(abs(err1) < abs(err0))
        