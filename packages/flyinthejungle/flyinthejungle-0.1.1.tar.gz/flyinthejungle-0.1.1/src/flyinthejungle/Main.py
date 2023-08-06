import sys

sys.path.append("/home/leonardo/Área de Trabalho/Fly in the jungle/src/jogo")

import Services

WIDTH = 905
HEIGHT = 450

play = False
services = Services.Services()
points = 0
actualAndHighPoints= [0 , 0]
savedPoints = False
world = None

# Draw frimes in screen
def draw():
    global play, points , world , actualAndHighPoints , savedPoints

    screen.clear()

    if world == None:
        world = services.decideIfcreateWorld()
        if savedPoints == False:
            actualAndHighPoints = services.savePoints(actualAndHighPoints , points)
            savedPoints = True
        services.drawBestPoints(screen , actualAndHighPoints)
        points = 0
    else:
        world.draw()
        services.drawKeyboards()
        points = services.drawPoints(screen , world.drone.containsGravityInverted , points)
        play = True
        savedPoints = False



# Update frames in screen
def update(dt):
    global world , play

    if world != None and play == True:
        play = world.update(dt)
        if (play == False):
            screen.clear()
            world = None








