from FGAme import *

class Character(RegularPoly):
	def __init__(self, N, length, pos, vel, omega, color, mass, **kwargs):
		self.in_dash = 'off'
		super(Character, self).__init__(N=N, length=length, pos=pos, vel=vel, omega=omega, color=color, 
											mass=mass, inertia='inf', **kwargs)
											
	#def objmove(self, dx, dy):
	#	if self.in_dash == 'off':
	#		self.vel+=(dx,dy)
	#	else: 
	#		self.vel=self.vel
		