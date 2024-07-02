# -*- coding: utf-8 -*-
"""
Created on Mon Mar 22 10:32:04 2021

@author: MariEli
"""
import pygame
from pygame.locals import *
from Constants import *
from Vector import *
from pygame import gfxdraw
from typing import Type, Any
from GameObject import *

class Screen:
	def __init__(self) -> None:
		self.width = CONST_SCREENWIDTH
		self.height = CONST_SCREENHEIGHT
		self.zoom = 1
		self.center = Vector(0, 0)
		self.color = pygame.Color(255, 255, 255, 255)
		self.handler = pygame.display.set_mode((CONST_SCREENWIDTH, CONST_SCREENHEIGHT))
		self.display = pygame.Surface((CONST_SCREENWIDTH/CONST_SCREENFACTOR, CONST_SCREENHEIGHT/CONST_SCREENFACTOR))
		self.alpha	= 127
	
	def setAlpha(self, alpha: int) -> None:
		self.alpha = 255 if alpha > 255 else alpha

	def clear(self) -> None:
		self.display.set_alpha(self.alpha)
		self.display.fill(self.color)

	def setFillColor(self, color: str) -> None:
		self.color = color
		
	def drawItem(self, ITEM: 'GameObject') -> None:
		if ITEM.shape.type == "square":
			self.drawSquare(ITEM)
		elif ITEM.shape.type == "rect":
			self.drawRect(ITEM)
		elif ITEM.shape.type == "circle":
			self.drawCircle(ITEM)
		elif ITEM.shape.type == "text":
			self.drawText(ITEM)
		elif ITEM.shape.image:
			if 0 <= ITEM.alpha <= 255:
				ITEM.shape.image.fill((255, 255, 255, ITEM.alpha), None, pygame.BLEND_RGBA_MULT)
			self.display.blit(ITEM.shape.image, (ITEM.position.x, ITEM.position.y), None, BLEND_RGBA_ADD )

	def drawCircle(self, ITEM: 'GameObject') -> None:
		if ITEM.shape.image:
			ITEM.shape.image.fill((255, 255, 255, ITEM.shape.alpha), None, pygame.BLEND_RGBA_MULT)
			self.display.blit(ITEM.shape.image, (ITEM.position.x, ITEM.position.y), None, BLEND_RGBA_ADD )
		else:
			if ITEM.shape.isFilled:
				gfxdraw.filled_circle(self.display, int(ITEM.position.x), int(ITEM.position.y), ITEM.shape.radius, pygame.Color(ITEM.shape.color) )
				gfxdraw.aacircle(self.display, int(ITEM.position.x), int(ITEM.position.y), ITEM.shape.radius, pygame.Color(ITEM.shape.color) )
			else:
				gfxdraw.aacircle(self.display, int(ITEM.position.x), int(ITEM.position.y), ITEM.shape.radius, pygame.Color(ITEM.shape.color) )

	def rotate_rect(self, rect, angle):
		# Calcule o centro do retângulo
		center = rect.center
		# Calcule os vértices do retângulo
		vertices = [(rect.topleft[0], rect.topleft[1]), 
					(rect.topright[0], rect.topright[1]), 
					(rect.bottomright[0], rect.bottomright[1]), 
					(rect.bottomleft[0], rect.bottomleft[1])]
		# Rotacione cada vértice em torno do centro
		rotated_vertices = []
		for vertex in vertices:
			# Transle o vértice para o centro
			translated_vertex = (vertex[0] - center[0], vertex[1] - center[1])
			# Rotaciona o vértice
			rotated_x = translated_vertex[0] * math.cos(math.radians(angle)) - translated_vertex[1] * math.sin(math.radians(angle))
			rotated_y = translated_vertex[0] * math.sin(math.radians(angle)) + translated_vertex[1] * math.cos(math.radians(angle))
			# Transle o vértice de volta
			rotated_vertex = (rotated_x + center[0], rotated_y + center[1])
			# Arredonde as coordenadas para números inteiros
			rotated_vertex = (round(rotated_vertex[0]), round(rotated_vertex[1]))
			rotated_vertices.append(rotated_vertex)
		return rotated_vertices

	def drawRect(self, OBJ: 'GameObject') -> None:
		rect = pygame.Rect(OBJ.position.x, OBJ.position.y, OBJ.shape.width, OBJ.shape.height)

		if OBJ.locks.rotation:
			if OBJ.shape.isFilled:
				gfxdraw.box(self.display, rect, pygame.Color(OBJ.shape.color))
				gfxdraw.rectangle(self.display, rect, pygame.Color(OBJ.shape.lineColor))
			else:
				gfxdraw.rectangle(self.display, rect, pygame.Color(OBJ.shape.lineColor))
		else:
			rotated_vertices = self.rotate_rect(rect, OBJ.rotation)
			rect = self.rotate_rect(rect, OBJ.rotation)
			if OBJ.shape.isFilled:
				pygame.gfxdraw.filled_polygon(self.display, rotated_vertices, pygame.Color(OBJ.shape.color))		
			pygame.gfxdraw.line(self.display, rotated_vertices[0][0], rotated_vertices[0][1], rotated_vertices[1][0], rotated_vertices[1][1], pygame.Color(OBJ.shape.lineColor))
			pygame.gfxdraw.line(self.display, rotated_vertices[1][0], rotated_vertices[1][1], rotated_vertices[2][0], rotated_vertices[2][1], pygame.Color(OBJ.shape.lineColor))
			pygame.gfxdraw.line(self.display, rotated_vertices[2][0], rotated_vertices[2][1], rotated_vertices[3][0], rotated_vertices[3][1], pygame.Color(OBJ.shape.lineColor))
			pygame.gfxdraw.line(self.display, rotated_vertices[3][0], rotated_vertices[3][1], rotated_vertices[0][0], rotated_vertices[0][1], pygame.Color(OBJ.shape.lineColor))		


	def drawSquare(self, OBJ: 'GameObject') -> None:
		square = pygame.Rect(OBJ.position.x, OBJ.position.y, OBJ.shape.size, OBJ.shape.size)
		if(OBJ.shape.isFilled):
			gfxdraw.box(self.display, square, pygame.Color(OBJ.shape.color))
			gfxdraw.rectangle(self.display, square, pygame.Color(OBJ.shape.lineColor))
		else:
			gfxdraw.rectangle(self.display, square, pygame.Color(OBJ.shape.lineColor))
	
	def drawText(self, ITEM: 'GameObject') -> None:
		msgSurface = ITEM.shape.font.render(ITEM.shape.text, True, pygame.Color(ITEM.shape.color))
		msgRect = msgSurface.get_rect()
		msgRect.topleft = (ITEM.position.x, ITEM.position.y)
		self.display.blit(msgSurface, msgRect)

	def draw(self, item: 'GameObject') -> None:
		gfxdraw.aacircle(self.display, item.position.x, item.position.y, item.radius, pygame.Color(item.color))
		
	def update(self) -> None:
		scaledDisplay = pygame.transform.scale(self.display, (CONST_SCREENWIDTH, CONST_SCREENHEIGHT))
		self.handler.blit( scaledDisplay, (0, 0), None )
		pygame.display.update()

pygame.init()