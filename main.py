import pygame, random


pygame.init()
pygame.mixer.init()
fpsClock = pygame.time.Clock()
winx, winy = 750, 750
win = pygame.display.set_mode((winx, winy))


background = pygame.image.load("shapes/background.png")
foodImage = pygame.image.load("shapes/food.png")
GameIcon = pygame.image.load("shapes/icon.png")


pygame.display.set_icon(GameIcon)
pygame.display.set_caption('snake game')


#bib list contains some sounds. this sounds use when player change direction of snake
bibList = [pygame.mixer.Sound("sounds/bib1.wav"),
pygame.mixer.Sound("sounds/bib2.wav"), pygame.mixer.Sound("sounds/bib3.wav"),
pygame.mixer.Sound("sounds/bib4.wav")]
eatingSound = pygame.mixer.Sound("sounds/eating_sound.wav")
crashSound = pygame.mixer.Sound("sounds/crash.wav")


#defualt head position
snakeHead = [375, 375]
#snakeBodyParts dictionary items are list. lists items are position of each part of snake body in x and y axis.
snakeBodyParts = {}
#fList items are list and lists are possible situations for food coordinates
fList = []


"""
conChecker function is for checking contact of snake head with food
and adding one part to snake body parts
"""
def conChecker(lFPos, snakeHead, contact, nos, key, snakeBodyParts):
    #check for making contact with food
    if snakeHead == lFPos:
        contact = True
        eatingSound.play()
        #adding new item to list of snake body parts
        if nos == 1:
            if key == "up":
                snakeBodyParts[1] = [snakeHead[0], snakeHead[1] + 25]
            if key == "down":
                snakeBodyParts[1] = [snakeHead[0], snakeHead[1] - 25]
            if key == "left":
                snakeBodyParts[1] = [snakeHead[0] + 25, snakeHead[1]]
            if key == "right":
                snakeBodyParts[1] = [snakeHead[0] - 25, snakeHead[1]]
        #adding new item to list of snake body parts
        elif nos > 1:
            if key == "up":
                newValue = list(snakeBodyParts.values())[-1]
                newValue = (newValue[0], newValue[1] + 25)
                snakeBodyParts[nos] = newValue
            if key == "down":
                newValue = list(snakeBodyParts.values())[-1]
                newValue = (newValue[0], newValue[1] - 25)
                snakeBodyParts[nos] = newValue
            if key == "left":
                newValue = list(snakeBodyParts.values())[-1]
                newValue = (newValue[0] + 25, newValue[1])
                snakeBodyParts[nos] = newValue
            if key == "right":
                newValue = list(snakeBodyParts.values())[-1]
                newValue = (newValue[0] - 25, newValue[1])
                snakeBodyParts[nos] = newValue
        nos += 1
    return contact, nos


def editorSnakeBodyParts(snakeBodyParts, snakeHead):
    oldHeadPos = list((snakeHead[0], snakeHead[1]))
    numOfIndexOfSnakeBodyParts = len(snakeBodyParts.keys())
    while numOfIndexOfSnakeBodyParts > 0:
        #puts the snake's head for the first index of the snake's body parts
        if numOfIndexOfSnakeBodyParts == 1:
            snakeBodyParts[1] = oldHeadPos
        else:
            #editing list of snake body parts for drawing
            newValues = numOfIndexOfSnakeBodyParts - 1
            newValues = list(snakeBodyParts.values())[newValues - 1]
            snakeBodyParts[numOfIndexOfSnakeBodyParts] = newValues
        numOfIndexOfSnakeBodyParts -= 1


def crashWork(condition):
    running = False
    crashSound.play()


def crash(snakeHead, running, snakeBodyParts, winx, winy):
    if snakeHead[0] >= winx:
        running = crashWork(running)
    elif snakeHead[0] <= winx - winx:
        running = crashWork(running)
    elif snakeHead[1] >= winy:
        running = crashWork(running)
    elif snakeHead[1] <= 0:
        running = crashWork(running)
    for partOfBody in snakeBodyParts.values():
        if snakeHead == partOfBody:
            running = crashWork(running)
    return running


#food function choose random food position from possible states
def food(lIndPP, fList):
    #randomly select index from list of possible food positions
    findex = random.randint(0, lIndPP)
    #choose specified index from list of possible food position
    lFPos = fList[findex]
    return lFPos


#making possible positions of food function generate possible position of food
def makingPPF(winx, snakeBodyParts, snakeHead, winy, fList):
    #editing fList and adding all possible positions
    for xpos in range(winx + 1):
      if xpos % 25 == 0 and xpos % 50 == 25:
          for ypos in range(winy + 1):
              if ypos % 25 == 0 and ypos % 50 == 25:
                  fList.append([xpos, ypos])
    #removing all parts of snake from possible positions
    for value in snakeBodyParts.values():
        if value in fList:
            fList.remove(value)
    fList.remove(snakeHead)

    return fList


#snake function draw snake head
def snakeDrawer(snakeHead, snakeBodyParts, win, running):
    pygame.draw.circle(win, (255, 255, 0), (snakeHead[0], snakeHead[1]), 25)
    #drawing snake body
    for values in snakeBodyParts.values():
         pygame.draw.circle(win, (0, 255, 255), (values[0], values[1]), 25)


def changeKey(key, route1, route2):
    if key != route1 and key != route2:
        return route2, True


#the direction of the snake
key = ""
#number of snake body parts
nos = 1
#the number of times the snake has changed direction
number = 0
nFoodGen = 0
#snake's head contact with food
contact = False
running = True
while running:


    fpsClock.tick(10)
    win.blit(background, (0, 0))


    if nFoodGen == 0:
        fList = makingPPF(winx, snakeBodyParts, snakeHead, winy, fList)
        #making possible positions of food
        old_snake_head = snakeHead
        #last index of possible positions
        lIndPP = fList[-1]
        lIndPP = fList.index(lIndPP)
        lFPos = food(lIndPP, fList)
        nFoodGen += 1
    if contact == True:
        fList = makingPPF(winx, snakeBodyParts, snakeHead, winy, fList)
        lIndPP = fList[-1]
        lIndPP = fList.index(lIndPP)
        lFPos = food(lIndPP, fList)
        contact = False
        nFoodGen += 1


    if nos > 1:
        editorSnakeBodyParts(snakeBodyParts, snakeHead)


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        keyChange = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                try:
                    key, keyChange = changeKey(key, "down", "up")
                except TypeError:
                    pass
            elif event.key == pygame.K_DOWN:
                try:
                    key, keyChange = changeKey(key, "up", "down")
                except TypeError:
                    pass
            elif event.key == pygame.K_RIGHT:
                try:
                    key, keyChange = changeKey(key, "left", "right")
                except TypeError:
                    pass
            elif event.key == pygame.K_LEFT:
                try:
                    key, keyChange = changeKey(key, "right", "left")
                except TypeError:
                    pass
            if keyChange == True:
                bibList[number % 4].play()
                number += 1
            keyChange = False
            break


    #change position of snake head
    if key == "up":
        snakeHead[1] -= 50
    if key == "down":
        snakeHead[1] += 50
    if key == "right":
        snakeHead[0] += 50
    if key == "left":
        snakeHead[0] -= 50


    contact , nos = conChecker(lFPos, snakeHead, contact, nos, key, snakeBodyParts)
    running = crash(snakeHead, running, snakeBodyParts, winx, winy)
    win.blit(foodImage, (lFPos[0] - 25, lFPos[1] - 25))
    snakeDrawer(snakeHead, snakeBodyParts, win, running)


    pygame.display.update()


while pygame.mixer.get_busy():
    pass
pygame.mixer.quit()
pygame.quit()
