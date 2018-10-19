import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
import numpy as np
import sys


def animate(i):
	for i in range(num_drones):
		if (i != 0):
			x_i = np.ones((num_drones - 1)) * drone_pos[i][0]
			x_j = np.array([drone_pos[j][0] for j in range(num_drones) if j != i])
			y_i = np.ones((num_drones - 1)) * drone_pos[i][1]
			y_j = np.array([drone_pos[j][1] for j in range(num_drones) if j != i])
			z_i = np.ones((num_drones - 1, 2)) * drone_pos[i]
			z_j = np.array([drone_pos[j] for j in range(num_drones) if j != i])
			norm = np.linalg.norm(z_i - z_j)**2

			# repulsion
			R = 1
			rep_x = R*np.sum(x_i - x_j)/(norm**2)
			rep_y = R*np.sum(y_i - y_j)/(norm**2)

			# attraction
			A = 0.00000001
			'''mathematically correct but not working:
			atr_x = 4*A*A*norm*np.sum(x_i - x_j)*np.exp(A*(norm)**2)
			atr_y = 4*A*A*norm*np.sum(y_i - y_j)*np.exp(R*(norm)**2)
			'''

			atr_x = 4*A*norm*np.sum(x_i - x_j)*np.exp(A*(norm)**2)
			atr_y = 4*A*norm*np.sum(y_i - y_j)*np.exp(R*(norm)**2)

			# clip velocities before upating
			drone_vels[i][0] = - np.clip(rep_x + atr_x, -10, 10)
			drone_vels[i][1] = - np.clip(rep_y + atr_y, -10, 10)

			# for plotting repuslive and attractive velocity contributions on drone 1
			if (i == 1):
				rep_xs.append(rep_x)
				atr_xs.append(atr_x)

	for i in range(num_drones):
		# update position
		drone_pos[i][0] += drone_vels[i][0]
		drone_pos[i][1] += drone_vels[i][1]

	# PLOTTING.
	ax1.clear()
	ax2.clear()

	for i in range(num_drones):
		label = "drone " + str(i)
		ax1.scatter(drone_pos[i][0], drone_pos[i][1], s=2, label=label)

	ax1.set_ylabel('all uav pos')
	ax2.plot(np.arange(len(rep_xs)), rep_xs, label="rep_x")
	ax2.set_ylabel('uav1 rep')
	ax3.plot(np.arange(len(atr_xs)), atr_xs, label="atr_x")
	ax3.set_ylabel('uav1 atr')
	ax1.set_xlim(0,width)
	ax1.set_ylim(0,height)


# spawn "num_drones" uav's into 2D world as points.
# each point represented by x,y tuple in dict "drone_pos"
# first uav initialized at (0,0)
# subsequent uav's at "start_sep" apart in +/- x direction
def spawn_uav(num_drones, world_size, start_sep=50):
	drone_pos = {}
	center = w, h = world_size[0]/2 , world_size[1]/2

	for i in range(num_drones):
		drone_pos[i] = [w, h + start_sep*np.floor((i+1)/2)*(-1)**(i+1)]
	return drone_pos
		

##################
##    SCRIPT    ##
##################

num_drones = 5
size = width, height = 1000, 300

#style.use('fivethirtyeight')

fig, (ax1, ax2, ax3) = plt.subplots(3, 1, gridspec_kw = {'height_ratios':[2, 1, 1]})
fig.tight_layout()

drones = []
drone_rects = []
drone_pos = spawn_uav(num_drones, size)
drone_vels = []
for i in range(num_drones):
	if (i == 0):
		drone_vels.append([5.1, 0.0])
	else:
		drone_vels.append([0.0, 0.0])

rep_xs = []
atr_xs = []
while 1:
	ani = animation.FuncAnimation(fig, animate, interval=1)
	plt.show()
	plt.close()
	sys.exit()




