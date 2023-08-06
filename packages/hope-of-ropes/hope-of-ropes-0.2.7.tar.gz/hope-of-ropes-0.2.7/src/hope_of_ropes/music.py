import pygame
import os


class Music():
	def __init__(self):
		pygame.init()
		pygame.mixer.pre_init(44100, 16, 2, 4096)
		self.abs_path = os.path.abspath('src/hope_of_ropes/assets/sfx')

	def play_music(self, name_file, number_times=0): # name_file should include extension like (.mp3, .wav)
		name_file = '/'+name_file
		pygame.mixer.music.load(self.abs_path+name_file)
		pygame.mixer.music.play(number_times)

	def stop_music(self):
		pygame.mixer.music.stop()
