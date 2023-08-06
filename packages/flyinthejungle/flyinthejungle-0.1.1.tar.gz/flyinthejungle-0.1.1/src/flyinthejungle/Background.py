from pgzero.actor import Actor

# Brackground class
class Background:

    # Constructor of Background
    def __init__(self,name,x,y):
        self.pos = (x,y)
        self.sprite = Actor(name.lower(),self.pos)

        # Draw frame in screen
    def draw(self):
        self.sprite.draw()

