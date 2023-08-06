from FGAme import *

class Arena(World):

	def start(object=[]):
		world.damping=0.9
		world.add(object[0])
		world.add(object[1])
		
	def draw_walls():
		width=40
		height=220
		leftwall = world.add.aabb(shape=(width, height), pos=(0,300), mass='inf')
		rigthwall = world.add.aabb(shape=(width, height), pos=(800,300), mass='inf')
		topwall = world.add.aabb(shape=(height, width), pos=(400,600), mass='inf')
		botwall = world.add.aabb(shape=(height, width), pos=(400,0), mass='inf')
		
Arena.draw_walls()