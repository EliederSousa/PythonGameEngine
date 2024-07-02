import pygame
from pygame.locals import *
from sys import exit
from Mouse import *
from Keyboard import *

class Events:
    def __init__(self):
        self.mouse = Mouse()
        self.keyboard = Keyboard()
        self.validKeys = [K_UP, K_DOWN, K_LEFT, K_RIGHT]
    
    def checkEvents(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            elif event.type == MOUSEMOTION:
                self.mouse.setPosition(*event.pos)
            elif event.type == MOUSEBUTTONDOWN:
                self.mouse.setButton(True)
            elif event.type == MOUSEBUTTONUP:
                self.mouse.setButton(False)
            elif event.type == KEYDOWN:
                self.keyboard.setKey(event.key, True)
            elif event.type == KEYUP:
                self.keyboard.setKey(event.key, False)
                
            
