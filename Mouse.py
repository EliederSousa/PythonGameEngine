# -*- coding: utf-8 -*-
"""
Created on Mon Mar 22 10:33:13 2021

@author: MariEli
"""
from Vector import *

class Mouse:
    def __init__(self):
        self.position = Vector(0, 0)
        self.lastPosition = Vector(0, 0)
        self.isClicked = False
        self.button = 1
        self.pressedTicks = 0

        self.dragThreshold = 25 # Número de ticks antes do clique virar um 'arrastar'
        self.drag = False

    def setPosition( self, x, y ):
        self.lastPosition = Vector(self.position.x, self.position.y)
        self.position = Vector(x, y)

    def setButton(self, clicked: bool):
        self.isClicked = clicked
