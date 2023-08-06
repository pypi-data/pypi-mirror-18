"""TODO:
		Make this.
"""
from FGAme import *
from .number import *

MAX_POS_SCREEN_X, OFFSCREEN_POS_Y  = conf.get_resolution()

class Player:
	def __init__(self):
		self.obj = world.add.circle(10, pos=(pos.middle.x, OFFSCREEN_POS_Y-200))
		self.obj.gravity = 500
		self.obj.damping = 1
		self.score = 0
		self.copied = []
		self.paused = False

	def toggle_pause(self):
		self.paused = not self.paused

	def update(self):
		if not self.paused:
			self.score += 0.5
		# remove_num(self.copied)
		# for index, num in enumerate(str(int(self.score))):
			# self.copied.extend(print_num(int(num),(index*25, 0)))		