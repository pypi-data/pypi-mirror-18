from pgzero.keyboard import keyboard

import Services as service
from pgzero.actor import Actor
from random import randint

#World class
class World:

    colision = False
    # Constructor of world
    def __init__(self,drone,boxes=[],background = 0):
        self.TIME_TO_CREATE_ITEM = 3
        self.drone = drone
        self.boxes = list(boxes)
        self.losangle = None
        self.background = background
        self.gravityChange = None
        self.timeToCreateItem = 0
        self.services = service.Services()
        self.starItem = None


    # Update the frames in screen
    def update(self,dt):
        global colision
        colisionLimits = self.drone.update(dt)
        for box in self.boxes:
            box.update(dt)
        colisionBox = self.defineTouchOnBox()
        if self.losangle == None or self.gravityChange == None or self.starItem == None:
            self.defineWhenCreateItem(dt)

        self.defineTouchOnItems(dt)

        self.decideWhenActivateGravity()
        self.decideWhenActivateSlowMotion()
        self.decideWhenActivateStar()


        if colisionBox == True or colisionLimits == True:
            return False
        else:
            return True

    # listening time to activate gravity item
    def decideWhenActivateGravity(self):
        if keyboard.x and self.drone.containsItemGravity:
            self.gravityChange = None
            self.drone.containsGravityInverted = True
            self.drone.gravity = -self.drone.gravity
            self.drone.containsItemGravity = False


    # listening time to activate slow motion item
    def decideWhenActivateSlowMotion(self):
        if keyboard.z and self.drone.containsItemSlowMotion:
            self.losangle = None
            self.boxes[0].slowMotion = True
            self.boxes[1].slowMotion = True
            self.boxes[2].slowMotion = True
            self.drone.containsItemSlowMotion = False


    # listening time to activate start item
    def decideWhenActivateStar(self):
        if keyboard.c and self.drone.containsItemStar:
            self.starItem = None
            self.drone.containsStartActivated = True
            self.drone.containsItemStar = False


    # monitoring when drone touch on any item
    def defineTouchOnItems(self , dt):
        if self.losangle != None:
            self.losangle.update(dt)
            self.defineTouchOnLosangle()

        if self.gravityChange != None:
            self.defineTouchOnGravityChange()

        if self.starItem != None:
            self.defineTouchOnStar()


    # Draw frames in screen
    def draw(self):
        self.background.draw()
        self.drone.draw()

        for box in self.boxes:
            box.draw()

        if self.losangle != None :
            self.losangle.draw()

        if self.gravityChange != None:
            self.gravityChange.draw()

        if self.starItem != None:
            self.starItem.draw()


    # Define contact between drone and box
    def defineTouchOnBox(self):
        for box in self.boxes:

            if self.drone.sprite.right -10 >= box.sprite.left and self.drone.sprite.left + 1 <= box.sprite.right:
                if self.drone.sprite.bottom -8 >= box.sprite.top and self.drone.sprite.top + 8 <= box.sprite.bottom:
                    if self.drone.containsStartActivated:
                        return False
                    else:
                        return True

    # Define contact between drone and losangle
    def defineTouchOnLosangle(self):
        if  self.drone.sprite.right - 5 >= self.losangle.  sprite.left:
            if self.drone.sprite.bottom -10  >= self.losangle.sprite.top and self.drone.sprite.top <= self.losangle.sprite.bottom:
                self.losangle.sprite = Actor("losango" , pos = (320,23))
                self.drone.containsItemSlowMotion = True

    # Define contact between drone and gravityItem
    def defineTouchOnGravityChange(self):
        if self.drone.sprite.right - 5 >= self.gravityChange.sprite.left:
            if self.drone.sprite.bottom - 10 >= self.gravityChange.sprite.top and \
                            self.drone.sprite.top <= self.gravityChange.sprite.bottom:
                self.drone.containsItemGravity = True
                self.gravityChange.sprite = Actor("gravitychange" , pos = (570,23))

    # Define contact between drone and star
    def defineTouchOnStar(self):
        if self.drone.sprite.right - 7 >= self.starItem.sprite.left:
            if self.drone.sprite.bottom - 12 >= self.starItem.sprite.top and \
                            self.drone.sprite.top <= self.starItem.sprite.bottom:
                self.drone.containsItemStar = True
                self.starItem.sprite = Actor("star" , pos = (750,23))

    # Define what item to create
    def defineWhenCreateItem(self ,dt):
        self.timeToCreateItem += dt
        if self.timeToCreateItem >= self.TIME_TO_CREATE_ITEM:
            self.timeToCreateItem = 0

            # all combinations to define how random show the items on screen
            if self.losangle == None and self.gravityChange == None and self.starItem == None:
                random = randint(0,2)

            elif self.losangle == None and self.gravityChange == None:
                random = randint(0,1)

            elif self.gravityChange == None and self.starItem == None:
                random = randint(1,2)

            elif self.starItem == None and self.losangle == None:
                random = randint(0,1)
                if random == 1:
                    random = 2

            elif self.gravityChange == None:
                random = 1

            elif self.starItem == None:
                random = 2
            else:
                random = 0

            self.chooseItemToCreate(random)


    # create selected item
    def chooseItemToCreate(self , random):
        if random == 0:
            self.losangle = self.services.createItemLosangle()

        if random == 1:
            self.gravityChange = self.services.createItemGravityChange()

        if random == 2:
            self.starItem = self.services.createItemStart()