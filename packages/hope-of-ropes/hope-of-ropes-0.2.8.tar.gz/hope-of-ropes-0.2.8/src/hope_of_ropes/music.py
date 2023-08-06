import pygame
import os


class Music():
	def __init__(self):
		pygame.init()
		pygame.mixer.pre_init(44100, 16, 2, 4096)
		self.abs_path = os.path.abspath('src/hope_of_ropes/assets/')
		self.rope = pygame.mixer.Sound(self.abs_path+'/sfx/hang.wav')
		pygame.mixer.music.load(self.abs_path+'/music/Miami Nights 1984 - Accelerated.mp3')
		pygame.mixer.music.play(-1)

	def play_rope(self, number_times=0): # name_file should include extension like (.mp3, .wav)
		self.rope.play(number_times)
		
	def stop_music(self):
		pygame.mixer.stop()
