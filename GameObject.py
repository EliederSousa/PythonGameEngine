from Engine import Engine
from Vector import Vector
from Constants import CONST_FONTSTANDARD, CONST_FONTSIZE, CONST_MAXVELOCITY, CONST_ROTATIONDECAY, CONST_MINROTATION
import pygame
from types import SimpleNamespace

class Shape:
    def __init__(self, CONFIG: dict) -> None:
        self.width = CONFIG["width"] if 'width' in CONFIG else 0
        self.height = CONFIG["height"] if 'height' in CONFIG else 0
        # Propriedades de desenho.
        # Não definir valor default para estas linhas é importante para
        # Screen.drawItem saber se vai desenhar algum contorno ou não.
        # Ele não desenha contorno se lineColor for undefined.
        self.lineColor = CONFIG["linecolor"] if 'linecolor' in CONFIG else "white"
        self.lineWidth = CONFIG["linewidth"] if 'linewidth' in CONFIG else 0
        self.color     = CONFIG['color'] if 'color' in CONFIG else "blue"
        self.isFilled  = True if 'color' in CONFIG and CONFIG["type"] != "text" else False
        # Mudar para 'center' desenha a partir do centro.
        self.mode = CONFIG["mode"] if "mode" in CONFIG else "upleft"
        self.type = CONFIG["type"] if "type" in CONFIG else ""
        self.image = CONFIG["image"] if "image" in CONFIG else ""
        self.size  = CONFIG["size"] if "size" in CONFIG else ""


class Square(Shape):
    def __init__(self, CONFIG: dict) -> None:
        self.size = CONFIG["size"] if 'size' in CONFIG else 1
        CONFIG["width"]     = self.size
        CONFIG["height"]    = self.size
        CONFIG["type"]      = "square"
        super().__init__(CONFIG)


class Rectangle(Shape):
    def __init__(self, CONFIG: dict) -> None:
        CONFIG["width"]     = CONFIG["width"] if 'width' in CONFIG else 1
        CONFIG["height"]    = CONFIG["height"] if 'height' in CONFIG else 1
        CONFIG["size"]      = CONFIG["width"] * CONFIG["height"]
        CONFIG["type"]      = "rect"
        super().__init__(CONFIG)


class Circle(Shape):
    def __init__(self, CONFIG: dict) -> None:
        self.radius = CONFIG["radius"] if 'radius' in CONFIG else 1
        CONFIG["width"]     = self.radius
        CONFIG["height"]    = self.radius
        CONFIG["size"]      = self.radius
        CONFIG["type"]      = "circle"
        super().__init__(CONFIG)


class Text(Shape):
    def __init__(self, CONFIG: dict) -> None:
        CONFIG["type"] = "text"
        super().__init__(CONFIG)
        self.text = CONFIG['text']
        font = CONFIG['font'] if 'font' in CONFIG else CONST_FONTSTANDARD
        size = CONFIG['fontsize'] if 'fontsize' in CONFIG else CONST_FONTSIZE
        bold = CONFIG['bold'] if 'bold' in CONFIG else False
        italic = CONFIG['italic'] if 'italic' in CONFIG else False
        self.font = pygame.font.SysFont(font, size, bold, italic)

    def setFont(self, FONTFAMILY: str, FONTSIZE: int, ISBOLD : bool = False, ISITALIC : bool = False) -> None:
        self.font = pygame.font.SysFont(FONTFAMILY, FONTSIZE, ISBOLD, ISITALIC)
    
    def updateText(self, TEXT):
        self.text = str(TEXT)


class GameObject:
    __id = Engine.generateID()    
    def __init__(self, CONFIG: dict) -> None:
        self.id = Engine.generateID()
        self.cloneData = CONFIG
        # Propriedade de posição, direção e física.
		# Position só pode ser instância de Point() ou Vector().
        self.position = CONFIG["position"] if 'position' in CONFIG else Vector(0, 0)
        self.velocity = CONFIG["velocity"] if 'velocity' in CONFIG else Vector(0, 0)
        self.acceleration = CONFIG["acceleration"] if 'acceleration' in CONFIG else Vector(0, 0)
        self.maxVelocity = CONFIG["maxVelocity"] if 'maxVelocity' in CONFIG else CONST_MAXVELOCITY
		
        self.locks = SimpleNamespace(
            rotation=(True if "lockRotation" in CONFIG else False),
            position=(True if "lockPosition" in CONFIG else False))
        self.rotation = CONFIG["rotation"] if 'rotation' in CONFIG else 0
        self.velRotation = CONFIG["velRotation"] if 'velRotation' in CONFIG else 0
        self.rotationDecay = CONFIG["rotationDecay"] if 'rotationDecay' in CONFIG else CONST_ROTATIONDECAY
        self.mass = CONFIG["mass"] if 'mass' in CONFIG else 1
        self.inverseMass = 1./self.mass
        
        self.shape = CONFIG["shape"] if 'shape' in CONFIG else Shape()
        if self.shape.type == "rect":
            self.handler = pygame.Rect(self.position.x, self.position.y, self.shape.width, self.shape.height)
        elif self.shape.type == "square":
            self.handler = pygame.Rect(self.position.x, self.position.y, self.shape.width, self.shape.width)
        self.velocityLineColor  = "red"
        self.accelerationLineColor = "blue"
		
        self.velocityShape  = {
            'style': 'line',
            'position': self.position,
            'to': self.position,
            'lineColor': self.velocityLineColor,
            'lineWidth': 1
        }
        self.accelerationShape  = {
            'style': 'line',
            'position': self.position,
            'to': self.position,
            'lineColor': self.accelerationLineColor,
            'lineWidth': 1
        }

    def __str__(self) -> str:
        return "GameObject[ID: %s]: (POS: %s, VEL: %s, ACCEL: %s)" % (self.id, self.position, self.velocity, self.acceleration)


    def applyForce(self, forceVector: Vector) -> None:
        force = forceVector.clone()
        force.scale( self.inverseMass )
        self.acceleration.add( force ) # 2ª lei de Newton


    def applyGravity(self, gravityVector: Vector) -> None:
        gravity = gravityVector.clone()
        self.acceleration.add( gravity )

    
    def seek(self, obj: Vector) -> None:
        maxForce = 5
        desiredVel = Vector(obj.x, obj.y)        
        desiredVel.sub(self.position);         
        desiredVel.normalize()
        desiredVel.scale(self.maxVelocity)
        desiredVel.sub(self.velocity)
        desiredVel.limit(maxForce)
        self.applyForce( desiredVel )


    def evade(self, obj: Vector) -> None:
        maxForce = .1
        desiredVel = Vector(obj.x, obj.y)        
        desiredVel.sub(self.position);                
        desiredVel.scale( -1 )            
        desiredVel.normalize()
        desiredVel.scale(self.maxVelocity)
        desiredVel.sub(self.velocity)
        desiredVel.limit(maxForce)        
        self.applyForce( desiredVel )

    def map_range(self, value: float, in_min: int, in_max: int, out_min: int, out_max: int) -> float:
        return (value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

    def arrive(self, obj: 'GameObject') -> None:
        maxForce = .005
        desiredVel = Vector(obj.x, obj.y)        
        desiredVel.sub(self.position)
        d = desiredVel.size()
        desiredVel.normalize()
        if d < 10000:
            m = self.map_range(d, 0, 10000, 0, self.maxVelocity)
            desiredVel.scale(m)
        else:
            desiredVel.scale(self.maxVelocity)
        desiredVel.sub(self.velocity)
        desiredVel.limit(maxForce)        
        self.applyForce( desiredVel )


    def updateEvent(self) -> None:
        pass


    def update(self) -> None:
        if not self.locks.position:
            self.velocity.add( self.acceleration )
            self.velocity.limit( self.maxVelocity )
            self.position.add( self.velocity )

            if Engine.debug:
                velocityVec = self.velocity.clone()
                velocityVec.scale(20)
                velocityVec.add( self.position )
                self.velocityShape["position"] = self.position
                self.velocityShape["to"] = velocityVec

                accelerationVec = self.acceleration.clone()
                accelerationVec.scale(400)
                accelerationVec.add( self.position )
                self.accelerationShape["position"] = self.position
                self.accelerationShape["to"] = accelerationVec
            
            self.acceleration.scale(0)

        if not self.locks.rotation:
            # Checar se a tela é circular, e atualizar a posição conforme o necessário
            if abs( self.velRotation ) > CONST_MINROTATION:
                self.rotation += self.velRotation
                self.velRotation *= self.rotationDecay
        
        