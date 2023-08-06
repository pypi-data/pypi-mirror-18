#! /usr/bin/env python
import pygame
import time
from pygame.locals import *
from sys import exit

class textScreen:

	def __init__(self):

		self.text = "default"
		self.pygamePosition = [100,100]
		self.color = (0,0,0)
		self.font = pygame.font.get_default_font()
		self.d_font = 28
		self.game_font = pygame.font.SysFont(self.font, self.d_font)


def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()
 
def message_display(text):
    largeText = pygame.font.Font('freesansbold.ttf',115)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = ((display_width/2),(display_height/2))
    gameDisplay.blit(TextSurf, TextRect)
 
    pygame.display.update()
 
    time.sleep(2)