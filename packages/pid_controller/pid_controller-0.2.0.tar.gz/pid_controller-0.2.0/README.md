PID Controller
==============

This implements a basic pure-Pyton PID controller (http://en.wikipedia.org/wiki/PID_controller).

Installation
------------

Run:

    pip install pid_controller
    
Usage
-----

    from pid_controller.pid import PID
    pid = PID(p=0.1, i=0.004, d=3.0)
    output = pid(feedback=get_feedback())

Development
-----------

Run unittests:

    export TESTNAME=; tox

To run a specific unittest:

    export TESTNAME=.test_robot_steering; tox
    
To run tests for a specific environment (e.g. Python 2.7 with Django 1.4):
    
    export TESTNAME=; tox -e py27
