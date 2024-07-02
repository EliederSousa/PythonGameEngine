import math
from Constants import CONST_PI180, CONST_IPI180
from typing import Type, Union

class Vector:
	def __init__(self, x: float, y: Union[float, str]) -> None:
		if y == "angle":
			self.x = math.cos(CONST_PI180 * x)
			self.y = math.sin(CONST_PI180 * x)
		else:
			self.x = x
			self.y = y

	def __str__(self) -> str:
		return "Vector(x: %.3f, y: %.3f)" % (self.x, self.y)
	
	def clone(self) -> 'Vector':
		return Vector(self.x, self.y)
	
	def add( self, Vector ) -> None:
		self.x += Vector.x
		self.y += Vector.y

	def sub( self, Vector ) -> None:
		self.x -= Vector.x
		self.y -= Vector.y
		
	def mul( self, Vector ) -> None:
		self.x *= Vector.x
		self.y *= Vector.y
	
	def div( self, Vector ) -> None:
		self.x /= Vector.x
		self.y /= Vector.y 
	
	def normalize(self) -> 'Vector':
		size = self.size()
		if size != 0:
			return Vector(self.x / self.size(), self.y / self.size() )
		else:
			return Vector(self.x, self.y)
	
	def size(self) -> float:
		return math.sqrt( (self.x * self.x) + (self.y * self.y) ) 

	def fastSize(self) -> float:
		return (self.x * self.x) + (self.y * self.y)
	
	def scale( self, factor ) -> None:
		self.x *= factor
		self.y *= factor
	
	def limit( self, maximum ) -> None:
		if self.size() > maximum:
			normalized = self.normalize()
			normalized.scale( maximum )
			self.x = normalized.x
			self.y = normalized.y
	
	def getAngle(self) -> float:
		return ( CONST_IPI180 * math.atan2(self.y, self.x))