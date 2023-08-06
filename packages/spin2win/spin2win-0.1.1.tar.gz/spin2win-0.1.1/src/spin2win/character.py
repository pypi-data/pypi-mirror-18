from FGAme import *
from spin2win.music import Music
import os
_ROOT = os.path.abspath(os.path.dirname(__file__))
from spin2win.text import message_display

#blueGlobalHealth = 100
#redGlobalHealth = 100
class Character(RegularPoly):
	def __init__(self, name, health,armor,in_dash=False,dash_cd=False,defense_cd=False, is_force_on = 1,*args, **kwargs):
		self.name = name
		self.in_dash = in_dash
		self.is_force_on = is_force_on
		self.dash_cd= dash_cd
		self.defense_cd= defense_cd
		super(Character, self).__init__(inertia='inf', *args, **kwargs)
		on('pre-collision').do(self.sound_col)
		self.health=health
		self.armor=armor
		self.damage=0
		self.dx=0
		self.dy=0  
											
	def move_character(self, dx, dy):
		if self.in_dash == False:
			self.vel+=(dx,dy)
			self.dx=dx
			self.dy=dy
		else: 
			pass
	
	def dash(self, r_mass, r_color,r_armor):
		if self.dash_cd == False:	
			dash_sound = os.path.join(_ROOT, 'sounds/dash.wav')
			Music.play_sound(dash_sound)
			self.is_force_on = 0
			attack_mass = 5000
			self.color = 'orange'
			self.in_dash = True
			self.armor*=2.5
			self.vel= vec(self.dx,self.dy)*50
			self.mass=attack_mass
			schedule(.5, self.nodash, r_mass=r_mass, r_color=r_color,r_armor=r_armor)
			self.dash_cd = True
			
		else:
			pass
	def dash_out_cd(self):
		self.dash_cd= False
		
	def nodash(self, r_mass, r_color,r_armor):
		self.in_dash = False
		self.is_force_on = 1
		self.color = r_color
		self.mass = r_mass
		self.armor = r_armor
		schedule(3,self.dash_out_cd)
		
		
	def defense(self, r_mass, r_color,r_armor):
		if self.defense_cd == False:	
			defense_sound = os.path.join(_ROOT, 'sounds/defense.wav')
			Music.play_sound(defense_sound)
			defense_mass = 30000
			self.vel=vec(0,0)
			self.is_force_on = 0
			self.mass=defense_mass
			self.color = 'black'
			self.armor *= 10
			schedule(1, self.nodefense, r_mass=r_mass, r_color=r_color,r_armor=r_armor)
			self.defense_cd = True
			
		else:
			pass
			
	def defense_out_cd(self):
		self.defense_cd = False
	
	def nodefense(self, r_mass, r_color,r_armor):
		self.mass = r_mass
		self.color = r_color
		self.armor = r_armor
		self.is_force_on = 1
		schedule(3, self.defense_out_cd)
		
	#FIX-ME ele fala que estamos passando 3 argumentos, então estamos pedindo 3 tbm
	def sound_col(self,col,dx):
		sound_col = os.path.join(_ROOT, 'sounds/collision_small.wav')
		Music.play_sound(sound_col)
		
	
	def check_lose(self):
		if self.x < 0 or self.x > 800 or self.y < 0 or self.y > 600:
			print("%s PERDEU" % self.name)
			exit()
		elif self.health <= 0:
			print("%s PERDEU" % self.name)
			exit()

	@listen('post-collision')
	def detect_colision(arena, col):
		A, B = col
		if isinstance(A, Character) and isinstance(B, Character):
			A.deal_damage()
			B.deal_damage()
			
	#FIX-ME: O unico jeito de atualizar a vida foi usando variavel global, 
	#parece que o frame-enter pega os valores iniciais do objeto, por isso o uso de globais
	def deal_damage(self):
		self.health-=50/self.armor
		print(self.name)
		print(self.health)
		print('----------')
		#if(self.name == 'Azul'):
		#	global blueGlobalHealth
		#	blueGlobalHealth = self.health
		#elif(self.name == 'Vermelho'):
		#	global redGlobalHealth
		#	redGlobalHealth = self.health
	
	#@listen('frame-enter')
	#def show_pontuaction(self):
	#	message_display(50, 625, str(blueGlobalHealth))
	#	message_display(750, 625, str(redGlobalHealth))
