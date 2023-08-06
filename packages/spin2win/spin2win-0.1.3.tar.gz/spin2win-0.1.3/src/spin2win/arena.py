from FGAme import *
from spin2win.character import Character
from spin2win.music import Music
import os
_ROOT = os.path.abspath(os.path.dirname(__file__))

class Arena(World):
	def init(self):
		self.blue = Character('Azul', N=6,length=40,pos=(200,400),vel=(300,0),omega=2*6.28, color = 'blue', mass=2500,health=100,armor=10)
		self.red = Character('Vermelho', N=5, length=40, pos=(600,200), vel=(-300, 0), omega=3*6.28, color = 'red', mass=1500,health=100,armor=10)
		self.add([self.blue, self.red])
		self.red.force = lambda v: -100*self.red.is_force_on*abs(self.red.pos-pos.middle)*(self.red.pos-pos.middle)
		self.blue.force =  lambda t: -100*self.blue.is_force_on*abs(self.blue.pos-pos.middle)*(self.blue.pos-pos.middle)
		self.damping=0.9
		
		main_sound = os.path.join(_ROOT, 'sounds/battle_theme.mp3')
		Music.play_music(main_sound)
		
		self.draw_walls()
		
		#FIX-ME: Pensar em um jeito melhor de fazer isso
		on('long-press', 'left').do(self.blue.move_character, -15, 0)
		on('long-press', 'right').do(self.blue.move_character, 15, 0)
		on('long-press', 'up').do(self.blue.move_character, 0, 15)
		on('long-press', 'down').do(self.blue.move_character, 0, -15,)
		on('long-press', 'a').do(self.red.move_character, -20, 0)
		on('long-press', 'd').do(self.red.move_character, 20, 0)
		on('long-press', 'w').do(self.red.move_character, 0, 20)
		on('long-press', 's').do(self.red.move_character, 0, -20)
		on('key-down','return').do(self.blue.dash, self.blue.mass, self.blue.color,self.blue.armor)
		on('key-down', 'space').do(self.red.dash, self.red.mass, self.red.color,self.red.armor)
		on('key-down', 'p').do(self.blue.defense, self.blue.mass, self.blue.color,self.blue.armor)
		on('key-down', 'x').do(self.red.defense, self.red.mass, self.red.color,self.red.armor)
		
		on('frame-enter').do(self.red.check_lose)
		on('frame-enter').do(self.blue.check_lose)
		
	def draw_walls(self):
		width=40
		height=220
		self.leftwall = self.add.aabb(shape=(width, height), pos=(0,300), mass='inf')
		self.rigthwall = self.add.aabb(shape=(width, height), pos=(800,300), mass='inf')
		self.topwall = self.add.aabb(shape=(height, width), pos=(400,600), mass='inf')
		self.botwall = self.add.aabb(shape=(height, width), pos=(400,0), mass='inf')