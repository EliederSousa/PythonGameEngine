from ObjectContainer import *
from Vector import *
from GameObject import *
from Screen import *
from Constants import *
from typing import Type, Any
import time

class Engine:    
    __nextid = 0
    __maximumid = 2 ** 32
    debug = False
    maxVelocity = CONST_MAXVELOCITY


    def __init__(self) -> None:
        self.groundFriction = CONST_FRICTION
        self.groundNormal = CONST_FRICTIONNORMAL
        self.hasGravity = False
        self.container = ObjectContainer()
        self.frictionMag = self.groundFriction * self.groundNormal
        self.gravity = Vector( 0, CONST_GRAVITY )
        self.screen = Screen()


    def setGravity(self, isActive: bool, force: Vector) -> None:
        self.hasGravity = isActive
        self.gravity = force


    @staticmethod
    def generateID() -> int:
        Engine.__nextid += 1
        if Engine.__nextid > Engine.__maximumid:
            Engine.__nextid = 1
        return Engine.__nextid
    

    def addForce( self, OBJ: 'GameObject', FORCE: Vector) -> None:
        OBJ.applyForce( FORCE )


    def addGravity( self, OBJ: 'GameObject', FORCE: Vector) -> None:
        OBJ.applyGravity( FORCE )


    def applyForces(self, obj: 'GameObject', index: int) -> None:

        if not obj.locks.position:
            # Aplicando Fricção
            friction = obj.velocity.clone()
            friction.normalize()
            friction.scale( -1 * self.frictionMag )
            self.addForce( obj, friction )
            
            # Aplicando Gravidade
            if self.hasGravity:
                self.addGravity(obj, self.gravity)

            # Resolvendo colisões
            self.solveCollisions( obj, index )  
            
        obj.update()
        obj.updateEvent()

    
    def solveCollisions(self, obj: 'GameObject', index: int) -> None:
        if obj.position.y + obj.shape.height > self.screen.height:
            obj.velocity.y = 0
            obj.position.y = self.screen.height - obj.shape.height
        
        for index2, obj2 in enumerate(self.container.objects):
            if obj2 != None:
                if index != index2:
                    if( self.checkCollision(obj, obj2) ):
                        obj.velocity.scale(-1)
                        obj2.velocity.scale(-1)

    
    def checkCollision(self, obj1: 'GameObject', obj2: 'GameObject'):
        # HitTest (AABB)
        halfsize1X = 0
        halfsize1Y = 0
        halfsize2X = 0
        halfsize2Y = 0
        if obj1.shape.type == "square":
            halfsize1X = obj1.shape.size/2
            halfsize1Y = obj1.shape.size/2
        elif obj1.shape.type == "rectangle":
            halfsize1X = obj1.shape.width/2
            halfsize1Y = obj1.shape.height/2
        elif obj1.shape.type == "circle":
            halfsize1X = obj1.shape.size/2
            halfsize1Y = obj1.shape.size/2

        if obj2.shape.type == "square":
            halfsize2X = obj2.shape.size/2
            halfsize2Y = obj2.shape.size/2
        elif obj2.shape.type == "rectangle":
            halfsize2X = obj2.shape.width/2
            halfsize2Y = obj2.shape.height/2
        elif obj2.shape.type == "circle":
            halfsize2X = obj2.shape.size/2
            halfsize2Y = obj2.shape.size/2

        maxDistance = Vector( halfsize1X + halfsize2X, halfsize1Y + halfsize2Y )
        
        distX = abs( obj2.position.x - obj1.position.x )
        distY = abs( obj2.position.y - obj1.position.y )
        if distX < maxDistance.x and distY < maxDistance.y:
            return True
        else:
            return False
    

    def updateObjects(self) -> None:
        for index, obj in enumerate(self.container.objects):
            if obj != None:
                if hasattr(obj, "maxTime"):
                    if time.time() * 1000 - obj.startTime >= obj.maxTime:
                        self.removeGameObject(index)
                    else:
                        self.applyForces( obj, index )
                else:
                    self.applyForces( obj, index )


    def updateScreen(self) -> None:
        self.screen.clear()

        for w in self.container.objects:
            if w != None:
                self.screen.drawItem(w)

        self.screen.update()
    

    def addGameObject(self, OBJ: 'GameObject') -> 'GameObject':
        self.container.add( OBJ )
        return OBJ


    def removeGameObject(self, ID: int) -> None:
        self.container.remove( ID )


    def countGameObjects(self) -> int:
        return self.container.getCount()
