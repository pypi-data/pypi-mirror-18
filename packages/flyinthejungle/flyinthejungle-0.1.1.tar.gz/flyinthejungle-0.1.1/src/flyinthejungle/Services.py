import pygame
import Drone as drone
import World as worldClass
import Box as box
import Losangle as losangle
import Background as background
import GravityItem as gravityItem
import Main as main
import StarItem as starItem
from pgzero.actor import Actor
from pgzero.keyboard import keyboard


class Services():

    # Constructor of Services
    def __init__(self):
        ...

    # Show pontuation of player
    def showPontuation(self,points,gravityActivated=False):

        if gravityActivated == False:
            pointsString = "POINTS : "
        else:
            pointsString = "20X POINTS : "
        stringPoints = str(points)
        myfont = pygame.font.SysFont("Arial",25)

        label = myfont.render(pointsString + stringPoints,1,(0,255,0))
        return label

    # Show the hightest score of player
    def showHighestPointsOnMenu(self,highpoints):
        HIGHPOINTS = "HIGH POINTS: "
        stringPoints = str(highpoints)
        myfont = pygame.font.SysFont("Arial",30)

        label = myfont.render(HIGHPOINTS + stringPoints,1,(255,255,255))
        return label

    # Show the actual points of player
    def showActualPointsOnMenu(self,points):
        HIGHPOINTS = "Your last one: "
        stringPoints = str(points)
        myfont = pygame.font.SysFont("Arial",25)
        label = myfont.render(HIGHPOINTS + stringPoints,1,(255,255,255))
        return label

    # Create world
    def createWorld(self):

        SPEED_BOX1 = -0.81
        SPEED_BOX2 = -1.1
        SPEED_BOX3 = -1.003
        world = worldClass.World(drone.Drone("drone_right",mass = 100,position=(24,200)),
                         [box.Box("box",speed0 = SPEED_BOX1),box.Box("box",speed0 = SPEED_BOX2),
                          box.Box("box",speed0 = SPEED_BOX3)],
                         background.Background("background",main.WIDTH / 2,main.HEIGHT /2 + 25))
        return world

    # Create item losangle
    def createItemLosangle(self):
        return losangle.Losangle("losango")

    # Create item gravity
    def createItemGravityChange(self):
        return gravityItem.Gravity("gravitychange")

    # Create item star
    def createItemStart(self):
        return starItem.StarItem("star")

    # Draw keys in screen
    def drawKey(self):

        x = Actor("z" , pos = (370 , 23))
        y = Actor("x" , pos = (520 , 23))
        c = Actor("c" , pos= (700 , 27))
        key = (x , y , c)

        return key

    #draw keyborads on screen
    def drawKeyboards(self):
        key = self.drawKey()
        key[0].draw()
        key[1].draw()
        key[2].draw()

    #decide when button play is clicked
    def playClicked(self):
        buttonPlay = Actor("botao_play", pos=(main.WIDTH / 2, main.HEIGHT / 2))
        buttonExit = Actor("btnsair" , pos=(main.WIDTH/ 2 , main.HEIGHT/ 1.2) )
        buttonExit.draw()
        buttonPlay.draw()
        if pygame.mouse.get_pressed()[0] == 1:
            if pygame.mouse.get_pos()[0] >= buttonPlay.left and pygame.mouse.get_pos()[0] <= buttonPlay.right:
                if pygame.mouse.get_pos()[1] >= buttonPlay.top and pygame.mouse.get_pos()[1] <= buttonPlay.bottom:
                    return  True
        if pygame.mouse.get_pressed()[0] == 1:
            if pygame.mouse.get_pos()[0] >= buttonExit.left and pygame.mouse.get_pos()[0] <= buttonExit.right:
                if pygame.mouse.get_pos()[1] >= buttonExit.top and pygame.mouse.get_pos()[1] <= buttonExit.bottom:
                    exit(0)
        return False


    def decideIfcreateWorld(self ):

        create = self.playClicked()
        if create == True or keyboard.K_RETURN:
            world = self.createWorld()
            return world
        else:
            return None

    # draw points on screen when player is playing
    def drawPoints(self, screen, convaintsInverted, points):
        if (convaintsInverted == True):
            points = points + 20
        else:
            points += 1
        screen.blit(self.showPontuation(points, convaintsInverted), (1, 1))
        return points

    #draw the best points on screen
    def drawBestPoints(self , screen, actualAngHighPoints):
        screen.blit(self.showHighestPointsOnMenu(actualAngHighPoints[1]), (main.WIDTH / 2.5, main.HEIGHT / 8))
        screen.blit(self.showActualPointsOnMenu(actualAngHighPoints[0]), (main.WIDTH / 2.5, main.HEIGHT / 4))

    #decide when is to save the actual and highpoints
    def savePoints(self, actualAngHighPoints, points):
        actualAngHighPoints[0] = points
        if points >= actualAngHighPoints[1]:
            actualAngHighPoints[1] = points

        return actualAngHighPoints







