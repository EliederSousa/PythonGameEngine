from Utils import *
from Vector import *
from Shoot import *
from GameObject import *
from typing import Type, Any, Union
import random

weaponTypes = [
    {
        "name": "Stone",
        "rof": 2000,
        "power": 15,
        "damage": 10,
        "ammo": 1,
        "round": 0,
        "type": "solid",
        "precision": 4
    },
    {
        "name": "Pistol",
        "rof": 800,
        "power": 30,
        "damage": 20,
        "ammo": 10,
        "round": 2,
        "type": "projectile",
        "precision": 4
    },
    {
        "name": "Sniper",
        "rof": 2000,
        "power": 100,
        "damage": 100,
        "ammo": 3,
        "round": 1,
        "type": "projectile",
        "precision": 0
    },
    {
        "name": "Rocket Launcher",
        "rof": 1000,
        "power": 5,
        "damage": 150,
        "ammo": 5,
        "round": 5,
        "type": "missile",
        "precision": 0
    }
]

class Weapon():
    """
        Instantiates a new weapon. You need to pass the configuration data and a pointer to an Engine instance.
        You can pass an integer as CONFIG, that will generate a premade configurated weapon.
    """
    def __init__(self, CONFIG: Union[dict, int], engineHandler: Engine) -> None:
        if isinstance(CONFIG, int):
            CONFIG = weaponTypes[CONFIG]

        self.name       = CONFIG["name"] if "name" in CONFIG else "Unknown"
        self.rateOfFire = CONFIG["rof"] if "rof" in CONFIG else 500
        self.power      = CONFIG["power"] if "power" in CONFIG else 10
        self.damage     = CONFIG["damage"] if "damage" in CONFIG else 10
        self.ammo       = CONFIG["ammo"] if "ammo" in CONFIG else 10
        self.rounds     = CONFIG["round"] if "round" in CONFIG else 2
        self.type       = CONFIG["type"] if "type" in CONFIG else "projectile"
        self.precision  = CONFIG["precision"] if "precision" in CONFIG else 1
        self.maxAmmo    = self.ammo
        self.maxRounds  = self.rounds
        self.lastShoot  = 0
        self.engineHandler = engineHandler


    def shoot(self, shooterPosition: Vector, targetObject: Any) -> None:
        if timeNow() - self.lastShoot > self.rateOfFire:
            if self.ammo > 0:
                self.lastShoot = timeNow()
                mouseDistanceVector = targetObject.position.clone()
                mouseDistanceVector.sub(shooterPosition)
                precision = random.randint( -self.precision/2, self.precision/2 )
                force = Vector(mouseDistanceVector.getAngle() + precision, "angle")
                force.scale(self.power)
                self.engineHandler.addGameObject(Shoot({
                    "position": shooterPosition.clone(),
                    "velocity": force,
                    "lockRotation": True,
                    "type": self.type,
                    "target": targetObject,
                    #"rotation": force.getAngle(),
                    "shape": Rectangle({
                        "width": 3,
                        "height": 3,
                        "linecolor": "white",
                        "color": "red"
                    })
                }))
                self.ammo -= 1
            elif self.rounds > 0:
                self.reload()
            else:
                self.noAmmoAnimation()


    def recharge(self):
        self.rounds = self.maxRounds


    def reload(self) -> None:
        if self.rounds > 0:
            self.rounds -= 1
            self.ammo   = self.maxAmmo
            self.lastShoot = timeNow()

    def noAmmoAnimation(self) -> None:
        # play sound
        pass
