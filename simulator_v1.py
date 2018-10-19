import matplotlib.pyplot as plt
import numpy as np
import sys, pygame


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


def main(num_drones):
	pygame.init()
	size = width, height = 1200, 600
	screen = pygame.display.set_mode(size)
	pygame.display.set_caption("2D Drone Simulator")
	clock = pygame.time.Clock()

	drones = []
	drone_rects = []
	drone_pos = spawn_uav(num_drones, size)
	drone_vels = []
	for i in range(num_drones):
		drones.append(pygame.transform.scale(pygame.image.load("hector_quadrotor.png"),(10,4)))
		drone_rects.append(drones[i].get_rect(center=drone_pos[i]))
		# drone_vels.append([1+i, 1+i])
		if (i == 0):
			drone_vels.append([1.1, 0.0])
		else:
			drone_vels.append([0.0, 0.0])

	while 1:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()
		
		screen.fill((255,255,255))
		for i in range(num_drones):
			'''
			OLD NAIVE VERSION
			# stay near main drone
			drone_rects[i] = drone_rects[i].move(drone_vels[i])
			if (i != 0):
				if ( np.sqrt( abs(drone_rects[0][0] - drone_rects[i][0]) ** 2 + abs(drone_rects[0][1] - drone_rects[i][1]) ** 2 ) >= 200):
					drone_vels[i][0] = drone_vels[0][0]
					drone_vels[i][1] = drone_vels[0][1]

			# boundry check
			if drone_rects[i].left < 0 or drone_rects[i].right > width:
				drone_vels[i][0] = - drone_vels[i][0]
			if drone_rects[i].top < 0 or drone_rects[i].bottom > height:
				drone_vels[i][1] = - drone_vels[i][1]

			# avoid collisions
			for j in range(num_drones):
				if j != i:
					#if drone_rects[i].colliderect(drone_rects[j]):	
					if (np.sqrt(abs(drone_rects[i][0] - drone_rects[j][0]) ** 2 + abs(drone_rects[i][1] - drone_rects[j][1]) ** 2) < 20):				
						print("Possible collision detected")
						drone_vels[i][0] = - drone_vels[i][0]
						drone_vels[i][1] = - drone_vels[i][1]
			'''

			#### NEW VERSION
			if (i != 0):
				Q = 100000000000
				R = 0.0000001
				x_i = np.ones((num_drones - 1)) * drone_pos[i][0]
				x_j = np.array([drone_pos[j][0] for j in range(num_drones) if j != i])
				y_i = np.ones((num_drones - 1)) * drone_pos[i][1]
				y_j = np.array([drone_pos[j][1] for j in range(num_drones) if j != i])
				z_i = np.ones((num_drones - 1, 2)) * drone_pos[i]
				z_j = np.array([drone_pos[j] for j in range(num_drones) if j != i])
				norm = np.linalg.norm(z_i - z_j, axis=1)**2

				drone_vels[i][0] = np.clip( - np.sum( Q*np.sum((x_i - x_j)/(norm**2)) + 4*R*R*norm*np.sum((x_i - x_j)*np.exp(R*(norm)**2)) ), -20, 20)
				drone_vels[i][1] = np.clip( - np.sum( Q*np.sum((y_i - y_j)/(norm**2)) + 4*R*R*norm*np.sum((y_i - y_j)*np.exp(R*(norm)**2)) ), -20, 20)

				print("x_diff", (x_i - x_j))
				print("y_diff", (y_i - y_j))
				print("norm", norm)
				print("vel drone_1", drone_vels[1])

		for i in range(num_drones):
			# update position
			drone_pos[i][0] += drone_vels[i][0]
			drone_pos[i][1] += drone_vels[i][1]

			drone_rects[i].x = drone_pos[i][0]
			drone_rects[i].y = drone_pos[i][1]

			# plot lines
			if (i != 0):
				pygame.draw.line(screen, (0,0,0), (drone_rects[i].center), (drone_rects[0].center))
			screen.blit(drones[i], drone_rects[i])
		pygame.display.flip()
		clock.tick(60)


##################
##    SCRIPT    ##
##################
main(3)
