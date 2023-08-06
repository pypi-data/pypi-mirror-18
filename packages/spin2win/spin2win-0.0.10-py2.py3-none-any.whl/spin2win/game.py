from FGAme import *
import pygame	
from spin2win.music import Music
from spin2win.arena import Arena
from spin2win.character import Character

#Verificar quais dados é possível tirar desse main	
normalmass=1500
defense = normalmass*10
attack = normalmass*3

blue = Character(N=6,length=40,pos=(200,300),vel=(300,0),omega=20, color = 'blue', mass=normalmass*2)
red = Character(N=5, length=40, pos=(600,300), vel=(-300, 0), omega=25, color = 'red', mass=normalmass)

Arena.start([blue, red])

dx=0
dy=0
is_force_blue_on=1
is_force_red_on=1
blue_in_dash='off'
red_in_dash='off'

Music.play_music("sounds/battle_theme.mp3")
red.force = lambda v: -10000*(red.pos-pos.middle)*is_force_red_on
blue.force =  lambda t: -10000*(blue.pos-pos.middle)*is_force_blue_on

@listen('long-press', 'left',dx=-5,dy=0)
@listen('long-press', 'right',dx=5,dy=0)
@listen('long-press', 'up',dy=5,dx=0)
@listen('long-press', 'down',dy=-5,dx=0)
def bluemove(dx, dy):
	if blue_in_dash == 'off':
		blue.vel+=(dx,dy)
	else: 
		blue.vel=blue.vel

@listen('long-press', 'a',d2x=-10,d2y=0)
@listen('long-press', 'd',d2x=10,d2y=0)
@listen('long-press', 'w',d2y=10,d2x=0)
@listen('long-press', 's',d2y=-10,d2x=0)
def redmove(d2x,d2y):
	if red_in_dash == 'off':
		red.vel+=(d2x,d2y)
	else: 
		red.vel=red.vel

@listen ('key-down','return')
@listen ('key-down','space')
def dashsound():
	Music.play_sound("dash.wav")
		
@listen('key-down','return')
def bluedash():
	global is_force_blue_on
	is_force_blue_on=0
	global blue_in_dash
	blue_in_dash='on'
	blue.vel*=1.1
	blue.mass=attack
	blue.color='orange'
	schedule(1,nodashblue)	

	
def nodashblue():
	global blue_in_dash
	blue_in_dash='off'
	global is_force_blue_on
	is_force_blue_on = 1
	blue.color='blue'
	blue.mass=normalmass

@listen('long-press','space')
def reddash():
	global is_force_red_on
	is_force_red_on=0
	global red_in_dash
	red_in_dash='on'
	red.vel*=1.1
	red.mass=attack
	red.color='orange'
	schedule(1,nodashred)

def nodashred():
	global red_in_dash
	red_in_dash='off'
	global is_force_red_on
	is_force_red_on = 1
	red.color='red'
	red.mass=2*normalmass


@listen('key-down', 'p')	
@listen('key-down', 'x')
def defesesound():
	Music.play_sound("defense.wav")

@listen('long-press','p')
def bluedefense():
	blue.vel*=0.9
	blue.mass=defense
	blue.color='black' 
	schedule(1,nodefenseblue)
	
@listen('long-press','x')
def reddefense():
	red.vel*=0.9
	red.mass=defense
	red.color='black'
	schedule(1,nodefensered)

def nodefenseblue():
	blue.mass=normalmass*2
	blue.color='blue'

def nodefensered():
	red.mass=normalmass
	red.color='red'



@listen('frame-enter')
def check_blue_lose():
	if blue.x < 0 or blue.x > 800 or blue.y < 0 or blue.y > 600:
		exit()
		
@listen('frame-enter')
def check_red_lose():
	if red.x < 0 or red.x > 800 or red.y < 0 or red.y > 600:
		exit()