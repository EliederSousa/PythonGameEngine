from GameObject import *
from Weapon import *

class Particle(GameObject):
    def __init__(self, CONFIG: dict) -> None:
        super().__init__(CONFIG)
        self.startTime  = timeNow()
        self.type       = CONFIG["type"] if "type" in CONFIG else ""

        self.mass       = .01 if self.type == "fire" else .3
        self.maxTime    = 2000 if self.type == "projectile" else 2500
        
        self.shape      = Rectangle({
            "width": 3,
            "height": 3,
            "linecolor": "aqua",
            "color": "blue"
        })

    def updateEvent(self):
        if self.type == "fire":
            pass


class Player(GameObject):
    def __init__(self, CONFIG: dict, engineHandler: Engine, eventHandler: Events) -> None:
        super().__init__(CONFIG)
        self.engineHandler  = engineHandler
        self.eventHandler   = eventHandler
        self.weapons        = [Weapon(1, engineHandler)]
        self.actualWeapon   = 0
        self.health         = 100
        self.armor          = 0

    def takeWeapon(self, weaponType: int) -> None:
        self.weapons.append(Weapon(weaponType, self.engineHandler))
        if self.actualWeapon == -1:
            self.actualWeapon = len(self.weapons)-1

    
    def getAmmo(self):
        return self.weapons[self.actualWeapon].ammo
    
    def getRounds(self):
        return self.weapons[self.actualWeapon].rounds
    
    def getWeaponName(self):
        return self.weapons[self.actualWeapon].name

    
    def updateEvent(self) -> None:
        if self.eventHandler.keyboard.isPressed(K_UP):
            self.velocity.y = 0
            self.applyForce(Vector(0, -20))
        if self.eventHandler.keyboard.isPressed(K_RIGHT):
            self.velocity.x = 3
        if self.eventHandler.keyboard.isPressed(K_LEFT):
            self.velocity.x = -3
        if self.eventHandler.keyboard.isPressed(K_e):
            for w in range(20):
                self.engineHandler.addGameObject(Particle({
                    "position": self.position.clone(),
                    "velocity": Vector(random.randint(-1, 1) * 10, random.randint(-1, 1) * 10),
                    "type": "fire",
                }))
                
            self.weapons[self.actualWeapon].recharge()
            self.weapons[self.actualWeapon].reload()
        elif self.eventHandler.mouse.isClicked:
            self.weapons[self.actualWeapon].shoot(self.position, self.eventHandler.mouse)