from random import randint
from pgzero.actor import Actor

import sys
sys.path.append("/home/leonardo/Área de Trabalho/Fly in the jungle/jogo")

import Main as main

# Box class
class Box:


    # Constructor of Box
    def __init__(self,name,speed0 = 0):
        self.TIME_SLOWMOTION = 7
        self.initialPos = (randint(main.WIDTH - 40,main.WIDTH- 20),randint(75,main.HEIGHT - 25))
        self.sprite = Actor(name.lower(),pos = (self.initialPos[0],self.initialPos[1]))
        self.speed = speed0
        self.initialSpeed = speed0
        self.pos = self.initialPos
        self.tempo = 0
        self.slowMotion = False
        self.tempoSlowMotion = 0
        self.storeSpeed = None

    # Update the states of frames
    def update(self, dt):
        self.tempo += dt
        self.evaluateSpeed(dt)
        self.evaluatePos(dt)
        self.defineSprite()

    # Draw frames in scrren
    def draw(self):
        self.sprite.draw()

    # Setting the speed
    def evaluateSpeed(self , dt):
        if self.slowMotion == False:
            if self.storeSpeed != None:
                self.speed = self.storeSpeed
                self.storeSpeed = None
            if self.pos[0] < 0:
                self.tempo = 0
                self.speed -= 0.5
        else:
            if self.storeSpeed == None:
                self.storeSpeed = self.speed
            self.speed = -0.15
            self.tempoSlowMotion += dt


            if self.tempoSlowMotion >= self.TIME_SLOWMOTION:
                self.tempoSlowMotion = 0
                self.slowMotion = False

    # Setting the position
    def evaluatePos(self , dt):
        if self.pos[0] < 0:
            self.pos = (main.WIDTH + 25 , randint(75 , main.HEIGHT - 25))
        else:
            self.pos = (self.pos[0]  + self.speed * self.tempo , self.pos[1] )

    # Setting the sprite
    def defineSprite(self):
        self.sprite.x = self.pos[0]
        self.sprite.y = self.pos[1]
