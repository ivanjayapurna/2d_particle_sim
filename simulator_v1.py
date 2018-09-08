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
		drone_pos[i] = (w, h + start_sep*np.floor((i+1)/2)*(-1)**(i+1))
	return drone_pos


def main(num_drones):
	pygame.init()
	size = width, height = 1000, 600
	screen = pygame.display.set_mode(size)
	pygame.display.set_caption("2D Drone Simulator")
	clock = pygame.time.Clock()

	drones = []
	drone_rects = []
	drone_pos = spawn_uav(num_drones, size)
	drone_vels = []
	for i in range(num_drones):
		drones.append(pygame.transform.scale(pygame.image.load("hector_quadrotor.png"),(30,20)))
		drone_rects.append(drones[i].get_rect(center=drone_pos[i]))
		drone_vels.append([1+i, 1+i])

	while 1:
		for event in pygame.event.get():
			if event.type == pygame.QUIT: sys.exit()

		screen.fill((255,255,255))
		for i in range(num_drones):
			drone_rects[i] = drone_rects[i].move(drone_vels[i])
			if drone_rects[i].left < 0 or drone_rects[i].right > width:
				drone_vels[i][0] = - drone_vels[i][0]
			if drone_rects[i].top < 0 or drone_rects[i].bottom > height:
				drone_vels[i][1] = - drone_vels[i][1]
			for j in range(num_drones):
				if j != i:
					if drone_rects[i].colliderect(drone_rects[j]):
						drone_vels[i][0] = - drone_vels[i][0]
						drone_vels[i][1] = - drone_vels[i][1]
						drone_vels[j][0] = - drone_vels[j][0]
						drone_vels[j][1] = - drone_vels[j][1]

			screen.blit(drones[i], drone_rects[i])
		pygame.display.flip()
		clock.tick(60)


##################
##    SCRIPT    ##
##################
main(10)
