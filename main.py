from GameObject import *
from Screen import Screen
from Events import *
from Vector import *
from ObjectContainer import *
from Shoot import *
from Utils import *
from Weapon import *
from Player import *
from Engine import Engine
import random
from typing import Type, Any
import pygame

# Create a clock object
clock = pygame.time.Clock()

# linewidth não está funcionando

ev  = Events()
eng = Engine()
eng.hasGravity = True
eng.screen.setFillColor((0,0,0))
eng.screen.setAlpha(255)
                 
player1 = eng.addGameObject(Player({
    "position": Vector(100, 100),
    "mass": 10,
    "shape": Rectangle({
        "width": 10,
        "height": 20,
        "linecolor": "green",
    }) 
}, eng, ev))

fpsText = eng.addGameObject(GameObject({
    "position": Vector(10, 10),
    "lockPosition": True,
    "lockRotation": True,
    "shape": Text({
        "text": "FPS:",
        "color": "white",
        "bold": True,
    })
}))

mouseText = eng.addGameObject(GameObject({
    "position": Vector(10, 25),
    "lockPosition": True,
    "lockRotation": True,
    "shape": Text({
        "text": "Mouse:",
        "color": "white",
        "bold": True,
    })
}))

numObjectsText = eng.addGameObject(GameObject({
    "position": Vector(10, 40),
    "lockPosition": True,
    "lockRotation": True,
    "shape": Text({
        "text": "Mouse:",
        "color": "white",
        "bold": True,
    })
}))

ammoText = eng.addGameObject(GameObject({
    "position": Vector(10, 55),
    "lockPosition": True,
    "lockRotation": True,
    "shape": Text({
        "text": "Ammo:",
        "color": "white",
        "bold": True,
    })
}))

healthText = eng.addGameObject(GameObject({
    "position": Vector(10, 70),
    "lockPosition": True,
    "lockRotation": True,
    "shape": Text({
        "text": "Health:",
        "color": "white",
        "bold": True,
    })
}))

while True:
    ev.checkEvents()
    fpsText.shape.text = "FPS: {:.1f}".format(clock.get_fps())
    mouseText.shape.text = "Mouse: {},{}".format(ev.mouse.position.x, ev.mouse.position.y)
    numObjectsText.shape.text = "Objects: {}".format(eng.countGameObjects())
    healthText.shape.text = "Health: {}".format(player1.health)
    ammoText.shape.text = "{} ammo: {}/{}".format(player1.getWeaponName(), player1.getAmmo(), player1.getRounds())    
    eng.updateObjects()
    eng.updateScreen()
    clock.tick(60)
