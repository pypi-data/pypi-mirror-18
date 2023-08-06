import pygame	

class Music:

	pygame.mixer.pre_init(44100, 16, 2, 4096)
	pygame.init()
	
	def play_music(music):
		main_sound = pygame.mixer.music.load(music)
		main_sound = pygame.mixer.music.play()
		pygame.mixer.music.set_volume(0.2);
		
	def play_sound(sound):
		dash_sound = pygame.mixer.Sound(sound)
		dash_sound.set_volume(0.2)
		dash_sound.play()