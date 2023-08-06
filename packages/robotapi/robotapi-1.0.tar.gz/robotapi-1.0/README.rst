===============================================
roboapi - Python API for mobile robot control
===============================================
.. image:: https://travis-ci.org/travis-ci/travis-web.svg?branch=master
    :target: https://travis-ci.org/travis-ci/travis-web

.. image:: https://coveralls.io/repos/github/sauravshandilya/SDES-2016-Project2/badge.svg
:target: https://coveralls.io/github/sauravshandilya/SDES-2016-Project2


Write a Python API for controlling a mobile robot.

This project uses `Raspberry Pi`_ as controller of `Firebird V`_, a mobile robotic platform. The API is designed to allow user write program python language on Raspberry Pi. Raspberry Pi is connected to mobile robot via USB link. The API give abstaction to users over Embedded C program required for using the robot. User make relevant function calls inside API written in Python to control various peripherals of the robot. 

Raspberry Pi is used as small computer, running a debian OS. It enhances the feature of robot by providing faster and efficient on-board processing capabilities (for example: running image processing on robot is not possible because of lower processing efficiency of microcontroller). 

Thus objective of API is to provide user ability to control hardware and perform high end processing using a single language - Python.

.. _Raspberry Pi: https://www.raspberrypi.org/
.. _Firebird V: http://www.nex-robotics.com/products/fire-bird-v-robots/fire-bird-v-atmega2560-robotic-research-platform.html

Documentation
===============

Documentation and details about project is hosted on `Read the Docs`_

.. _Read the Docs: http://sdes-2016-project2.readthedocs.io
