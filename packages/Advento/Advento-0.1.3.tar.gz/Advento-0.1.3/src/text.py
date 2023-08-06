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
	gameDisplay.fill(white)
	largeText = pygame.font.Font('freesansbold.ttf', 35)
	TextSurf, TextRect = text_objects(text, largeText, black)
	TextRect.center = ((x),(y))
	gameDisplay.blit(TextSurf, TextRect)
	pygame.display.update()
	time.sleep(5)