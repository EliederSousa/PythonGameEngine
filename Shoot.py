from Vector import *
from GameObject import *
from Events import *
from Utils import *
from Constants import CONST_GRAVITY


class Shoot(GameObject):
    def __init__(self, CONFIG: dict) -> None:
        self.type       = CONFIG["type"] if "type" in CONFIG else "projectile"
        CONFIG["mass"]  = .1 if self.type == "projectile" else 10        
        self.maxTime    = 5000 if self.type == "projectile" else 2500
        self.target     = CONFIG["target"] if "target" in CONFIG else self
        self.startTime  = timeNow()

        super().__init__(CONFIG)

    def updateEvent(self):
        if self.type != "solid":
            self.applyForce(Vector(0, -CONST_GRAVITY)) # Anti-gravity
        if self.type == "missile":
            mouseDistanceVector = self.target.position.clone()
            mouseDistanceVector.sub(self.position)
            force = Vector(mouseDistanceVector.getAngle(), "angle")
            force.scale(2)
            accel_ratio = 300
            print( (timeNow() - self.startTime) / accel_ratio)
            force.limit( (timeNow() - self.startTime) / accel_ratio)
            self.applyForce(force)
        
        # self.seek( ev.mouse.position.clone() )

