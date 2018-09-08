import time
import simpy
import simpy.rt
import random
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

def main():
	num_drones = 10
	num_frames = 100	
	range_x = (-100, 100)
	range_y = (-100, 100)
	drone_pos_x = []
	drone_pos_y = []

	for i in range(num_drones):
		drone_pos_x.append(0)
		drone_pos_y.append(5*np.floor((i+1)/2)*(-1)**(i+1))

	fig = plt.figure()
	scat = plt.scatter(drone_pos_x, drone_pos_y)

	ani = animation.FuncAnimation(fig, update_pos, frames=range(num_frames), fargs=(scat))
	plt.show()

def update_pos(i, data, scat):
	scat.set_array(data[i])
	return scat,
	'''
	for i in range(num_drones):
		move_x = random.choice(-1, 0, 1)
		move_y = random.choice(-1, 0, 1)
		drone_pos_x[i] += move_x
		drone_pos_y[i] += move_y
		return drone_pos_x, drone_pos_y
	'''
main()

#fig = plt.plot(drone_pos_x, drone_pos_y,'o', markersize=2)
#plt.axis([range_x[0], range_x[1], range_y[0], range_y[1]])




'''
def point(env, name, bcs, driving_time, charge_duration):
	yield env.timeout(driving_time)

	print('%s arriving at %d' % (name, env.now))
	with bcs.request() as req:
		yield req
		print('%s starting to charge at %s' % (name, env.now))
		yield env.timeout(charge_duration)
		print('%s leaving the bcs at %s' % (name, env.now))

env = simpy.rt.Environment()
bcs = simpy.Resource(env, capacity=2)

for i in range(4):
	env.process(point(env, 'Point %d' % i, bcs, i*2, 5))

env.run()
'''

