# 2d_particle_sim
A 2D particle simulator created using pygame to be connected to OpenWSN or similar network simulator to test micro-robot control functions and algorithms. Run simulator_v1.py.

# TODO:
0. there is a bug where keyboard inputs do not work on Mac OS python3, on Linux there should be no issue, need to test & implement this on linux later.
1. update physics to get accurate acceleration and deceleration consistent with that of hector quadrotor (for slowdown and speedup when avoiding collisions)
2. connect to https://bitbucket.org/6tisch/simulator to send commands to change velocity and stuff