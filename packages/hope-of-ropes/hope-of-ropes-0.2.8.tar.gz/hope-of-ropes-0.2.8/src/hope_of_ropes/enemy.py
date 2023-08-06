from FGAme import *

class Enemy:
	def __init__(self):
		self.items = []

	def add(self, pos):
		obj = world.add.rectangle(shape=(20, 10), \
								  pos=pos, \
								  vel=(-50,0), \
								  color=(0,255,0,255))
		obj.inertia = 'inf'
		obj.is_enemy = True
		self.items.append(obj)


	def remove(self, remove_item):
		self.items.remove(remove_item)