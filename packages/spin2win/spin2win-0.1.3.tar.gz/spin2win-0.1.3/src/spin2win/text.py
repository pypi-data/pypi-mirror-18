import pygame
import time
black = (0,0,0)
white = (255,255,255)

def text_objects(text, font, color):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()
	
def message_display(x, y, text):
		clock = pygame.time.Clock()
		gameDisplay = pygame.display.set_mode((800,650))
		gameDisplay.fill(black)
		largeText = pygame.font.Font('freesansbold.ttf', 35)
		TextSurf, TextRect = text_objects(text, largeText, white)
		TextRect.center = ((x),(y))
		gameDisplay.blit(TextSurf, TextRect)
		rect = pygame.Rect(0, 600, 800, 50)
		pygame.display.update(rect)
	
		