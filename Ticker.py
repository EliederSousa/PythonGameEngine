import pygame
import random

class Ticker:
	def __init__(self, minTime, maxTime):
		self.counter = 0
		self.lastTime = pygame.time.get_ticks()
		self.compareValue = 0
		self.minTime = minTime
		self.maxTime = maxTime

	def update(self):
		self.lastTime = self.now()
		self.counter = 0
		self.compareValue = random.randrange(self.minTime, self.maxTime)

	def now(self):
		return pygame.time.get_ticks()

	def compare(self):
		self.counter += 1
		return (self.now() - self.lastTime) >= self.compareValue