from pgzero.actor import Actor
from random import randint

import Main as MP

# StarItem class
class StarItem:

    # Constructor of StarItem
    def __init__(self , name ):
        self.pos = (randint(MP.WIDTH - 40, MP.WIDTH- 20) , randint(75 , MP.HEIGHT - 25))
        self.sprite = Actor(name.lower() , self.pos)
        self.tempo = 0

    # Draw frames in screen
    def draw(self):
        self.sprite.draw()