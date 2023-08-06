import pygame
from FGAme import *
from pygame.locals import *
from sys import exit
import os
import time

class MainMenu(object):
	def __init__(self):
		self.option = 0
		self.text_list = []
		self.screen = pygame.display.set_mode((800,700),0, 32)
		self.caption = pygame.display.set_caption("Main Menu")
		self.clock = pygame.time.Clock()
	
	def select_arrow(self, value):
		select_arrow = open_image("arrowSilver_right.png")
		if value == 0:
			self.screen.blit(select_arrow,(250,560),select_arrow.get_rect())
		elif value == 1:
			self.screen.blit(select_arrow,(250,620),select_arrow.get_rect())

	def initial_buttons(self):
		start_button = open_image("start.png")
		exit_button = open_image("exit.png")

		self.screen.blit(start_button,(290,530),start_button.get_rect())
		self.screen.blit(exit_button,(280,600),exit_button.get_rect())
	def proccess_input(self):
		bg = open_image("menu_background_2.jpg")
		while True:
			self.screen.blit(bg, (0, 0), bg.get_rect())
			self.initial_buttons();
			self.select_arrow(self.option)
			
			for event in pygame.event.get():
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_UP:
						self.option -= 1
						#time.sleep(1/7)
						if self.option < 0:
							self.option = 1
						else:
							# Do nothing
							pass
					if event.key == pygame.K_DOWN:
						self.option += 1
						if self.option > 1:
							self.option = 0
						else:
							# Do nothing
							pass

					if event.key == pygame.K_RETURN:
						if self.option == 0:
							return self.option
						elif self.option == 1:
							pygame.quit()
							exit()
					else:
						# Do nothing
						pass

				if event.type == QUIT:
				    exit()
			
			pygame.display.update()

			time_passed = self.clock.tick(60)

def open_image(name):
	image = pygame.image.load(os.path.abspath('src/hope_of_ropes/images/' + name)).convert_alpha()
	return image