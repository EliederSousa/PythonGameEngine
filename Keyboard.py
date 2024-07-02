# -*- coding: utf-8 -*-
"""
Created on Wed Sep  7 20:50:50 2022

@author: MariEli
"""

class Keyboard:
	def __init__(self):
		self.keys = {"UP": False, "DOWN": False, "LEFT": False, "RIGHT": False, "SPACE": False }
		
	def isPressed( self, key ):
		try:
			return self.keys[key]
		except KeyError:
			return False
	
	def setKey(self, key: int, boolValue: bool ):
		self.keys[key] = boolValue
