from pgzero.actor import Actor
from random import randint

import Main as MP

# Losangle class
class Losangle:

    # Constructor of Losangle
    def __init__(self,name = None):
        self.time = 0
        self.pos = (randint(MP.WIDTH - 40, MP.WIDTH- 20),randint(75,MP.HEIGHT - 25))
        self.sprite = Actor(name.lower() ,self.pos)

    # Draw frames in screen
    def draw(self ):
        self.sprite.draw()

    # Update frames in screen
    def update(self, dt):
        self.time = self.time + dt




