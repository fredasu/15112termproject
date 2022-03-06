###################
#Name: Freda Su
#Andrew ID: fysu
#tp3 woohoo
###########

import copy, math, random, time, pygame
import sys, csv
from cmu_112_graphics import *
from tp3_pz import *    #to access the plants and zombies

def appStarted(app):
    app.mode = 'splashScreenMode'
    app.margin = 15
    app.cols = 9
    app.rows = app.sun = 5
    app.yBottom = app.height - app.margin*2
    app.xBottomLeft = 0 + app.margin
    app.xBottomRight = app.width - app.margin
    app.yTop = app.height * 1/4 #let's say the board takes up about 3/4 of the canvas
    app.colWidth = (app.xBottomRight - app.xBottomLeft)/app.cols
    app.boxWidth = (app.width - 2*app.margin)/app.cols
    app.boxHeight = (app.height - 2*app.margin)/app.rows
    app.totalTime = app.time0 = time.time() #increase difficulty of zombies as time continues
    app.zombieTypes = [RegularZombie(), ConeheadZombie(), BucketheadZombie(),
    PoleVaulter(), NewspaperZombie(), Wizard()]
    app.plantTypes = [Sunflower(), PeaShooter(), CherryBomb(), WallNut(),
    Watermelon(), Cannon(), "Shovel"]
    app.plantLoading = [0] * (len(app.plantTypes) - 1)  #account for shovel
    app.zombiesOnscreen = []    #will add zombies as time continues, can have multiple zombise in same place
    app.plantsOnscreen = dict() #where each key is the coord they're at, only 1 plant per coord
    app.sunSpots = []   #locations where sun appears from either sunflower or randomly appearing
    app.gameOver = False
    app.plantChosen = None
    app.plantChosenCoord = (-1, -1)
    app.pea = []   #to draw peas shooting out
    app.watermelon = [] #to draw parabola trajectory based on starting rc, will change
    app.coconut = []    #cannon only fires when pressed
    app.timerDelay = 20    #20ms
    app.RoboConeOrig = app.loadImage('RoboConeLag.png')
    app.RoboConeScaled = app.scaleImage(app.RoboConeOrig, 1/2)
    app.RegZombOrig = app.loadImage('RegCovidZombie.png')
    app.RegZombScaled = app.scaleImage(app.RegZombOrig, 1/12)
    app.ConeheadOrig = app.loadImage('CoronaConehead.png')
    app.ConeheadScaled = app.scaleImage(app.ConeheadOrig, 1/2.5)
    app.PoleVaulterOrig = app.loadImage('PoleVaulter.png')
    app.PoleVaulterScaled = app.scaleImage(app.PoleVaulterOrig, 1/1.25)
    app.NewspaperOrig = app.loadImage('NewspaperZ.png')
    app.NewspaperScaled = app.scaleImage(app.NewspaperOrig, 1/1.7)
    app.SunflowerOrig = app.loadImage('sunflower.png')
    app.SunflowerScaled = app.scaleImage(app.SunflowerOrig, 1/4.5)
    app.PeashooterOrig = app.loadImage('peashooter-Handsanitizer.png')
    app.PeashooterScaled = app.scaleImage(app.PeashooterOrig, 1/3)
    app.CherryOrig = app.loadImage('cherry.png')
    app.CherryScaled = app.scaleImage(app.CherryOrig, 1/1.5)
    app.WallnutOrig = app.loadImage('wallnut.png')
    app.WallnutScaled = app.scaleImage(app.WallnutOrig, 1/4)
    app.WatermelonOrig = app.loadImage('watermelon.png')
    app.WatermelonScaled = app.scaleImage(app.WatermelonOrig, 1/5)
    app.CoconutOrig = app.loadImage('Cannon.png')
    app.CoconutScaled = app.scaleImage(app.CoconutOrig, 1/9.5)
    app.TPOrig = app.loadImage('toiletp.png')
    app.TPScaled = app.scaleImage(app.TPOrig, 1/2)
    app.DropletOrig = app.loadImage('droplet.png')
    app.DropletScaled = app.scaleImage(app.DropletOrig, 1/20)
    app.ShovelOrig = app.loadImage('shovel.png')
    app.ShovelScaled = app.scaleImage(app.ShovelOrig, 1/4)
    app.bucketSpriteStrip = app.loadImage("BucketSpriteStrip.png")
    app.bucketSpriteScaled = app.scaleImage(app.bucketSpriteStrip, 3.5)
    app.sprites = []
    spriteCut(app)
    app.spriteCounter = 0
    pygame.mixer.init()
    pygame.mixer.music.load("music.mp3")
    pygame.mixer.music.set_volume(.1)
    app.pauseMusic = True
    app.gameType = None
    app.gameWon = False
    app.timesUp = False
    app.zombiesKilled = 0
    app.name = ''
    app.displayScores = False

def appRestarted(app):
    app.mode = 'splashScreenMode'
    app.sun = 5
    app.yBottom = app.height - app.margin
    app.xBottomLeft = 0 + app.margin
    app.xBottomRight = app.width - app.margin
    app.yTop = app.height * 1/4
    app.colWidth = (app.xBottomRight - app.xBottomLeft)/app.cols
    app.boxWidth = (app.width - 2*app.margin)/app.cols
    app.boxHeight = (app.height - 2*app.margin)/app.rows
    app.totalTime = app.time0 = time.time()
    app.plantLoading = [0] * (len(app.plantTypes) - 1)
    app.zombiesOnscreen = []
    app.plantsOnscreen = dict()
    app.sunSpots = []
    app.gameOver = False
    app.gameWon = False
    app.timesUp = False
    app.plantChosen = None
    app.plantChosenCoord = (-1, -1)
    app.pea = []
    app.watermelon = []
    app.coconut = []
    app.zombiesKilled = 0
    pygame.mixer.music.pause()
    pygame.mixer.music.set_volume(.1)
    app.name = ''
    app.displayScores = False
    app.sprites = []
    spriteCut(app)

def spriteCut(app):
    imageWidth, imageHeight = app.bucketSpriteScaled.size
    spriteWidth = imageWidth/7
    for i in range(2):
        sprite = app.bucketSpriteScaled.crop((6+spriteWidth*i, 0, 3+spriteWidth*(i+1), imageHeight))
        app.sprites.append(sprite)
    for i in range(2, 6):
        sprite = app.bucketSpriteScaled.crop((-8+spriteWidth*i, 0, -8+spriteWidth*(i+1), imageHeight))
        app.sprites.append(sprite)
    for i in range(6, 7):
        sprite = app.bucketSpriteScaled.crop((spriteWidth*i, 0, spriteWidth*(i+1), imageHeight))
        app.sprites.append(sprite)
    #the spacing of each sprite is weird so i had to adjust the cuts of each sprite :(

def gameMode_appStopped(app):    #make sure to shut off the music when close app
    pygame.mixer.music.stop()

def gameMode_timerFired(app):
    #so it checks to resize everything
    app.yBottom = app.height - app.margin*2
    app.xBottomLeft = 0 + app.margin
    app.xBottomRight = app.width - app.margin
    app.yTop = app.height * 1/4
    app.colWidth = (app.xBottomRight - app.xBottomLeft)/app.cols
    app.boxWidth = (app.width - 2*app.margin)/app.cols
    app.boxHeight = (app.height - 2*app.margin)/app.rows
    app.spriteCounter = (1 + app.spriteCounter) % len(app.sprites)  #could walk slower, but it's still funny
    if app.gameOver or app.gameWon or app.timesUp:
        pygame.mixer.music.stop()
        return
    i = 0
    while i in range(len(app.pea)):   #step all the peas forward
        x0, y, speed = app.pea[i]
        if x0 > app.width:
            app.pea.pop(i)  #don't bother drawing things offscreen
        else:
            x1 = x0 + speed
            app.pea[i] = (x1, y, speed)
            i += 1
    k = 0
    while k in range(len(app.coconut)): #step all coconuts forward
        x0, y, speed = app.coconut[k]
        if x0 > app.width:
            app.coconut.pop(k)
        else:
            x1 = x0 + speed
            app.coconut[k] = (x1, y, speed)
            k += 1
    #see if coco hit anything, can't do this in cannonAction bc that's only checked when clicked
    i = 0
    while i in range(len(app.coconut)):
        plant = Cannon()
        damage = plant.getDamage()
        attackType = plant.getAttackType()
        xCoco, y, speed = app.coconut[i]
        row, col = getCell(app, xCoco, y)
        bestZombieIndex = findBestZombie(app, row)
        if bestZombieIndex != -1:
            zombie = app.zombiesOnscreen[bestZombieIndex]
            if row == zombie.getRow() and xCoco >= zombie.getX():
                zombie.isAttacked(damage, attackType)
                if zombie.getHealth() <= 0:
                    app.zombiesOnscreen.pop(bestZombieIndex)
                    app.zombiesKilled += 1
                app.coconut.pop(i)  #get rid of coconut bc already hit zombie
                continue
        i += 1

    zombieActions(app)
    sunActions(app)
    plantActions(app)

    if time.time() - app.time0 >= 10:
        #add a random sun
        yRand = random.randint(int(app.yTop), app.height - 3*app.margin)
        xRand = random.randint(0 + 3*app.margin, app.width - 3*app.margin)
        t = time.time()
        app.sunSpots.append((xRand, yRand, t))  #sun disappears when enough time passed
        if app.gameType == 'short':
            if time.time() - app.totalTime <= 60*3:
                moreZombie(app)
            else:
                if len(app.zombiesOnscreen) == 0:
                    app.gameWon = True
                app.time0 = time.time()
        elif app.gameType == 'long':
            if time.time() - app.totalTime <= 60*5:
                moreZombie(app)
            else:   #time's up, terminate game anyways: even if there are still zombies onscreen
                app.timesUp = True

def moreZombie(app):
    if time.time() - app.totalTime >= 70:   #randomly choose how many zombies appear as well
            randNumZ = random.randint(1, 5)
            for x in range(randNumZ):
                randIndex = random.randrange(len(app.zombieTypes))
                addZombie(app, randIndex)
    elif time.time() - app.totalTime >= 60:
        randIndex = random.randrange(len(app.zombieTypes))
        addZombie(app, randIndex)
    elif time.time() - app.totalTime >= 50:
        randIndex = random.randrange(5)
        addZombie(app, randIndex)
    elif time.time() - app.totalTime >= 40:
        randIndex = random.randrange(4)
        addZombie(app, randIndex)
    elif time.time() - app.totalTime >= 30:
        randIndex = random.randrange(3)
        addZombie(app, randIndex)
    elif time.time() - app.totalTime >= 20:
        randIndex = random.randrange(2)
        addZombie(app, randIndex)
    elif time.time() - app.totalTime >= 10:
        randIndex = random.randrange(1) #generic zombie must appear first
        addZombie(app, randIndex)
    app.time0 = time.time()

def findBestZombie(app, r): #given a row, return index of where bestZombie is
    bestZombieX = app.width
    bestZombieIndex = -1
    #see if there's a zombie in the same row
    for z in range(len(app.zombiesOnscreen)):
        zombie = app.zombiesOnscreen[z]
        if zombie.getRow() == r:
            if zombie.getX() <= bestZombieX:
                bestZombieX = zombie.getX()
                bestZombieIndex = z
    return bestZombieIndex

def zombieActions(app):
    a = (1/3) * (app.yBottom - app.yTop) - app.margin
    b = .75
    for zombie in app.zombiesOnscreen:
        x = zombie.getX()
        row = zombie.getRow()
        y1 = app.yBottom - (a * (app.rows - (row+1))**b) #should be the bottom edge
        if row == 0:
            y0 = app.yTop
        else:
            y0 = app.yBottom - (a * (app.rows - (row))**b) #should be the top edge
        y = (y0 + y1)/2
        row, col = getGridCell(app, x, y)  #get the column that the zombie is in
        if (row, col) in app.plantsOnscreen:    #keys are the coordinates
            #eat plant before continuing
            if isinstance(zombie, PoleVaulter): #vault over first object
                if zombie.getVaultStatus() == False:
                    zombie.vault(app.boxWidth)
            plant = app.plantsOnscreen[(row, col)]
            attack = zombie.getAttack()
            plant.isAttacked(attack)
            if plant.getHealth() <= 0:
                del app.plantsOnscreen[(row, col)]   #remove plant bc it's been eaten
        else:   #otherwise, free to keep moving
            step = zombie.getSpeed()
            zombie.move(step)
        if zombie.getX() <= 0:  #reached left edge of screen = you lose
            app.gameOver = True

def plantActions(app):
    #check if peashooters in same row as zombies => attack
    #put list of (r,c) of cherryBombs to delete after we're done looping
    cherryBombs = []
    for key in app.plantsOnscreen:
        r, c = key
        plant = app.plantsOnscreen[(r,c)]
        damage = plant.getDamage()
        attackType = plant.getAttackType()
        if isinstance(plant, PeaShooter):
            peaShooterActions(app, plant, damage, attackType, r, c)
        elif isinstance(plant, CherryBomb):
            cherryBombs.append((r, c))
            cherryBombActions(app, r, c, damage, attackType)
        elif isinstance(plant, Watermelon):
            watermelonActions(app, plant, damage, attackType, r, c)
    for (x,y) in cherryBombs:   #need to remove cherry bomb, not sure if this will break anything
        if time.time() - app.plantsOnscreen[(x,y)].getTime() >= 1:  #so we can see cherry bomb for longer
            del app.plantsOnscreen[(x,y)]

def peaShooterActions(app, plant, damage, attackType, r, c):
    #peashooter looks for target and shoots
    bestZombieIndex = findBestZombie(app, r)
    #found the frontMost zombie to attack
    if bestZombieIndex != -1 and time.time() - plant.getTime() >= 2:
        xTopLeft, xTopRight, xBottomLeft, xBottomRight, y0, y1 = gridCellBounds(app, r, c)
        xPeaStart = (xBottomLeft + xBottomRight)/2
        yPea = .75*y0 + .25*y1  #to appear out of the "mouth" of peashooter
        vPea = plant.getSpeed()
        app.pea.append((xPeaStart, yPea, vPea))
        plant.setTime(time.time())
    #calculate if pea has hit zombie => remove pea and attack zombie
    i = 0
    while i in range(len(app.pea)):
        bestZombieIndex = findBestZombie(app, r)
        xPea, y, speed = app.pea[i]
        row, col = getGridCell(app, xPea, y)
        if bestZombieIndex != -1:
            zombie = app.zombiesOnscreen[bestZombieIndex]
            if row == zombie.getRow() and xPea >= zombie.getX():
                zombie.isAttacked(damage, attackType)
                if zombie.getHealth() <= 0:
                    app.zombiesOnscreen.pop(bestZombieIndex)
                    app.zombiesKilled += 1
                app.pea.pop(i)  #get rid of pea bc already hit zombie
                continue
        i += 1

def cherryBombActions(app, r, c, damage, attackType):
    #check 3x3 square around it
    a = (1/3) * (app.yBottom - app.yTop) - app.margin
    b = .75
    j = 0
    while j in range(len(app.zombiesOnscreen)):
        zombie = app.zombiesOnscreen[j]
        row = zombie.getRow()
        y1 = app.yBottom - (a * (app.rows - (row+1))**b) #should be the bottom edge
        if row == 0:
            y0 = app.yTop
        else:
            y0 = app.yBottom - (a * (app.rows - (row))**b) #should be the top edge
        x = zombie.getX()
        y = (y0 + y1)/2
        rowCheck, col = getGridCell(app, x, y)  #get the column that the zombie is in
        row = zombie.getRow()   #already know row
        if (row >= r - 1 and row <= r + 1 and col >= c - 1 and col <= c + 1):
            #attack zombies in range
            zombie.isAttacked(damage, attackType)
            if zombie.getHealth() <= 0:
                app.zombiesOnscreen.pop(j)
                app.zombiesKilled += 1
                continue
        j += 1

def watermelonActions(app, plant, damage, attackType, r, c):
    #find zombies to attack, add coordinates to watermelon list
    bestZombieIndex = findBestZombie(app, r)
    if bestZombieIndex != -1 and time.time() - plant.getTime() >= 1.5:    #lob once per sec
        zombie = app.zombiesOnscreen[bestZombieIndex]
        newZombieX = zombie.getX() - zombie.getSpeed() * (1000/app.timerDelay)  #calculate new zombie position
        app.watermelon.append((r, c, time.time(), newZombieX))
        plant.setTime(time.time())
    #remove the melons that have already hit target or fall on the ground
    i = 0
    while i in range(len(app.watermelon)):
        r, c, startingTime, newX = app.watermelon[i]
        xTopLeft, xTopRight, xBottomLeft, xBottomRight, y0, y1 = gridCellBounds(app, r, c)
        middleX = (xBottomLeft + xBottomRight)/2
        timeDiff = time.time() - startingTime
        x = ((newX - middleX))*timeDiff + middleX   #x parameterize w t (b-a)t + a
        if x >= newX:
            app.watermelon.pop(i)
            bestZombieIndex = findBestZombie(app, r)
            if bestZombieIndex != -1:
                app.zombiesOnscreen[bestZombieIndex].isAttacked(damage, attackType)
                if app.zombiesOnscreen[bestZombieIndex].getHealth() <= 0:
                    app.zombiesOnscreen.pop(bestZombieIndex)
                    app.zombiesKilled += 1
        else:
            i += 1

def cannonActions(app, plant, r, c):
    #only here bc cannon was clicked => fire if have TP ammo left
    if app.sun > 0:
        xTopLeft, xTopRight, xBottomLeft, xBottomRight, y0, y1 = gridCellBounds(app, r, c)
        xStart = .25*xBottomLeft + .75*xBottomRight
        yStart = (y0 + y1)/2
        vCoco = plant.getSpeed()
        app.coconut.append((xStart, yStart, vCoco))
        app.sun -= 1    #the TP ammo has to come from somewhere

def sunActions(app):
    #adding/removing sun from sky and sunflowers
    i = 0
    while i in range(len(app.sunSpots)):
        x, y, t = app.sunSpots[i]
        if time.time() - t >= 10:  #sun disappears after a while if not collected
            app.sunSpots.pop(i)
        else:
            i += 1

    for plant in app.plantsOnscreen.values():
        if isinstance(plant, Sunflower):
            time0 = plant.getTime()
            if time.time() - time0 >= 5:    #can change later
                row = plant.getRow()
                col = plant.getCol()
                xTopLeft, xTopRight, xBottomLeft, xBottomRight, y0, y1 = gridCellBounds(app, row, col)
                x = (xBottomLeft + xBottomRight)/2
                y = .25*y0 + .75*y1
                app.sunSpots.append((x, y, time.time()))
                #reset sun time
                plant.setTime(time.time())

def addZombie(app, randIndex):
    randRow = random.randint(0, 4)
    newZombie = app.zombieTypes[randIndex]
    newZombie.setRow(randRow)
    newZombie.setXCoord(app.width)
    app.zombiesOnscreen.append(copy.copy(newZombie))    #avoid aliasing

def gameMode_mousePressed(app, event):
    if app.gameOver or app.gameWon:
        appRestarted(app)
        return
    elif app.timesUp:
        return
    #click on the falling "sun", the plant "seed packets", and to launch the coconut cannon
    x = event.x
    y = event.y
    #check if clicked on a plant seed row, then check if clicked on plant/zombie
    if y <= app.margin + app.boxHeight:
        row, col = getCell(app, x, y)
        if 1 <= col <= len(app.plantTypes):  #clicked on a plant packet, <= len bc of sun box offset
            potentialPlant = app.plantTypes[col - 1]    #account for sun box offset
            if col == len(app.plantTypes):
                app.plantChosen = "Shovel"
            elif app.sun >= potentialPlant.getCost() and potentialPlant.getLoad() <= (time.time() - app.plantLoading[col - 1]):
                app.plantChosen = potentialPlant
            else:   #not done loading/not enough $ = didn't select on anything
                app.plantChosen = None
                app.plantChosenCoord = (-1, -1)
    else:
        #clicked on the grid
        row, col = getGridCell(app, x, y)
        if (row, col) in app.plantsOnscreen:  #check if clicked on cannon = fire => check if hit zombie
            for (r, c) in app.plantsOnscreen:
                plant = app.plantsOnscreen[(r,c)]
                if isinstance(plant, Cannon):
                    if row == r and col == c:
                        cannonActions(app, plant, r, c)
                        break   #can't really click on multiple cannons at once
        a = (1/3) * (app.yBottom - app.yTop) - app.margin
        b = .75
        z = 0
        while z in range(len(app.zombiesOnscreen)):
            zombie = app.zombiesOnscreen[z]
            if isinstance(zombie, Wizard):
                #figure out where zombie is, then see if clicked on it
                newImage = app.scaleImage(app.RoboConeScaled, .75**(app.rows - zombie.getRow()))
                imageWidth, imageHeight = newImage.size
                y1 = app.yBottom - (a * (app.rows - (zombie.getRow()+1))**b) #should be the bottom edge
                if zombie.getRow() == 0:
                    y0 = app.yTop
                else:
                    y0 = app.yBottom - (a * (app.rows - (zombie.getRow()))**b) #should be the top edge
                cx = zombie.getX()
                cy = (y0 + y1)/2
                xLeft = cx - imageWidth/2
                xRight = cx + imageWidth/2
                yTop = cy - imageHeight/2
                yBot = cy + imageHeight/2
                if xLeft <= x <= xRight and yTop <= y <= yBot:
                    zombie.isAttacked(3, "Click")   #may change damageLevel later
                    if zombie.getHealth() <= 0:
                        app.zombiesOnscreen.pop(z)
                        app.zombiesKilled += 1
                    break   #can only click on 1 zombie at a time
            z += 1
    #check if clicked on a sun
    i = 0
    while i in range(len(app.sunSpots)):
        cx, cy, t = app.sunSpots[i]
        imageWidth, imageHeight = app.TPScaled.size
        xLeft = cx - imageWidth/2
        xRight = cx + imageWidth/2
        yTop = cy - imageHeight/2
        yBot = cy + imageHeight/2
        if xLeft <= x <= xRight and yTop <= y <= yBot:
            app.sunSpots.pop(i)
            app.sun += 1
        else:
            i += 1

def gameMode_mouseDragged(app, event):
    #drag plant to new location? only activate if already clicked on seed packet
    if app.gameOver or app.gameWon or app.timesUp:
        return
    x = event.x
    y = event.y
    if app.plantChosen != None:
        app.plantChosenCoord = (x,y)

def gameMode_mouseReleased(app, event):
    if app.gameOver or app.gameWon or app.timesUp:
        return
    #drop plant on garden grid
    x = event.x
    y = event.y
    if y >= app.yTop:   #released onto board probably
        row, col = getGridCell(app, x, y)
    else:
        app.plantChosen = None
        app.plantChosenCoord = (-1, -1)
        return
    rDel, cDel = -1, -1
    if 0 <= row < app.rows:
        if 0 <= col < app.cols: #in garden
            #make sure can't add another plant if box is taken
            for plant in app.plantsOnscreen.values():
                r = plant.getRow()
                c = plant.getCol()
                if r == row and c == col:    #there's already a plant there = don't add to list (shovel)
                    if app.plantChosen == "Shovel":
                        rDel, cDel = r, c
                    app.plantChosen = None  #reset
                    app.plantChosenCoord = (-1, -1)
                    break
            if (rDel, cDel) != (-1, -1):
                del app.plantsOnscreen[(rDel, cDel)]
                return
            elif app.plantChosen == "Shovel":   #trying to shovel nothing
                app.plantChosen = None
                app.plantChosenCoord = (-1, -1)
                return
            elif app.plantChosen != None:
                newPlant = app.plantChosen
                newPlant.setRow(row)
                newPlant.setCol(col)
                newPlant.setTime(time.time())
                app.plantsOnscreen[(row, col)] = copy.copy(newPlant)  #avoid aliasing
                app.sun -= newPlant.getCost()
                plantIndex = app.plantTypes.index(newPlant)
                app.plantLoading[plantIndex] = time.time()
    app.plantChosen = None  #reset
    app.plantChosenCoord = (-1, -1)

def gameMode_keyPressed(app, event):
    if event.key == "Space":
        if app.pauseMusic:
            pygame.mixer.music.unpause()
        else:
            pygame.mixer.music.pause()
        app.pauseMusic = not app.pauseMusic
    if app.timesUp:
        if event.key == "Enter":
            leaderboard = readLeaderboard()
            updateLeaderboard(leaderboard, app.name, app.zombiesKilled)
            app.mode = 'splashScreenMode'
            app.gameWon = False
            app.timesUp = False
            app.gameType = None
        elif event.key == "Backspace":
            app.name = app.name[:len(app.name) - 1]
        elif event.key == "Space":
            app.name = app.name + ' '
        else:
            app.name += event.key

#from https://www.cs.cmu.edu/~112/notes/notes-animations-part2.html
def cellBounds(app, row, col):  #for the toolbox line only
    x0 = app.margin + app.boxWidth*col
    x1 = x0 + app.boxWidth
    y0 = app.margin + app.boxHeight*row 
    y1 = y0 + app.boxHeight
    return x0, y0, x1, y1

#from https://www.cs.cmu.edu/~112/notes/notes-animations-part2.html
def getCell(app, x, y):
    #for the toolbox line only
    #based on the coordinates, return the cell (make sure it doesn't break if not clicked in a cell)
    x -= app.margin
    y -= app.margin
    row = y//app.boxHeight
    col = x//app.boxWidth
    return int(row), int(col)

def getGridCell(app, x, y):
    #based on the coordinates, return the cell (make sure it doesn't break if not clicked in a cell)
    #it should be somewhere on the garden
    mCols = colSlopes(app)
    a = (1/3) * (app.yBottom - app.yTop) - app.margin
    b = .75
    r = 0   #trying different rows
    while r in range(app.rows):
        yBottomRowLine = app.yBottom - (a * (app.rows - (r+1))**b)
        if y < yBottomRowLine:
            break
        else:
            r += 1
    y0 = app.yBottom - (a * (app.rows - (r))**b)
    y1 = app.yBottom - (a * (app.rows - (r+1))**b)
    c = 0   #trying different col
    while c in range(app.cols):
        mColLeft = mCols[c]
        mColRight = mCols[c + 1]
        xColLeft = app.xBottomLeft + app.colWidth*c
        xColRight = app.xBottomLeft + app.colWidth*(c + 1)
        #we also know the y-coord of the col lines are app.yBottom
        #check where the y val given hits the col lines
        xLeftBound = (y - app.yBottom)/mColLeft + xColLeft
        xRightBound = (y - app.yBottom)/mColRight + xColRight
        if xLeftBound <= x <= xRightBound:  #check if x-val between the col lines
            break
        else:
            c += 1
    return r, c

def gridCellBounds(app, row, col):
    #estimate that the dist bw row lines is y = a*x^b where a = bottom row, b = scaling factor, x = row
    #a and b were found experimentally
    #equation was found using best-fit functions of calculator
    a = (1/3) * (app.yBottom - app.yTop) - app.margin
    b = .75
    y1 = app.yBottom - (a * (app.rows - (row+1))**b) #should be the bottom edge
    if row == 0:
        y0 = app.yTop
    else:
        y0 = app.yBottom - (a * (app.rows - (row))**b) #should be the top edge
    #to find x, figure out where the col line intersects with y lines (constant)
    mCols = colSlopes(app)
    mColLeft = mCols[col]
    mColRight = mCols[col + 1]
    xColLeft = app.xBottomLeft + app.colWidth*col
    xColRight = app.xBottomLeft + app.colWidth*(col + 1)
    #we also know the y-coord of the col lines are app.yBottom
    xBottomLeft = (y1 - app.yBottom)/mColLeft + xColLeft
    xBottomRight = (y1 - app.yBottom)/mColRight + xColRight
    xTopLeft = (y0 - app.yBottom)/mColLeft + xColLeft
    xTopRight = (y0 - app.yBottom)/mColRight + xColRight
    return xTopLeft, xTopRight, xBottomLeft, xBottomRight, y0, y1

def colSlopes(app):    #return list of col slopes
    xVanish = app.width/2
    yVanish = -1*(app.height)
    colSlopes = []
    for i in range(app.cols + 1):   #the for loop may be redundant but this is so it accounts for resizing
        m = (yVanish - app.yBottom)/(xVanish - (app.xBottomLeft + i*app.colWidth))
        colSlopes.append(m)
    return colSlopes

def gameMode_redrawAll(app, canvas):
    canvas.create_rectangle(0, 0, app.width, app.height, fill = "tan")
    canvas.create_rectangle(0, 0, app.width, app.yTop - app.margin, fill = "light blue")
    drawGrid(app, canvas)
    drawPea(app, canvas)    #not a projectile bc it moves fast
    drawWatermelon(app, canvas) #projectile
    drawCoconut(app, canvas)    #not a projectile bc it moves fast
    drawSunCount(app, canvas)
    drawPlantPackets(app, canvas)   #plant seed packets at the top
    drawPlants(app, canvas)
    drawZombies(app, canvas)
    drawSun(app, canvas)
    drawProgressBar(app, canvas)
    drawPlantChosen(app, canvas)

    if app.gameWon:
        drawGameWon(app, canvas)
    elif app.gameOver:
        drawGameOver(app, canvas)
    elif app.timesUp:
        drawTimesUp(app, canvas)

def drawGrid(app, canvas):
    #draw garden background, draw zombies on top
    for r in range(app.rows):
        for c in range(app.cols):
            xTopLeft, xTopRight, xBottomLeft, xBottomRight, y0, y1 = gridCellBounds(app, r, c)
            canvas.create_polygon(xTopLeft, y0, xTopRight, y0, xBottomRight, y1, xBottomLeft, y1,
            fill = "light green", outline = "black")

def drawZombies(app, canvas):
    a = (1/3) * (app.yBottom - app.yTop) - app.margin
    b = .75
    for zombie in app.zombiesOnscreen:
        row = zombie.getRow()
        y1 = app.yBottom - (a * (app.rows - (row+1))**b) #should be the bottom edge
        if row == 0:
            y0 = app.yTop
        else:
            y0 = app.yBottom - (a * (app.rows - (row))**b) #should be the top edge
        x = zombie.getX()
        y = (y0 + y1)/2
        if isinstance(zombie, Wizard):
            newImage = app.scaleImage(app.RoboConeScaled, .75**(app.rows - row))
        elif isinstance(zombie, RegularZombie):
            newImage = app.scaleImage(app.RegZombScaled, .75**(app.rows - row))
        elif isinstance(zombie, ConeheadZombie):
            newImage = app.scaleImage(app.ConeheadScaled, .75**(app.rows - row))
        elif isinstance(zombie, BucketheadZombie):
            sprite = app.sprites[app.spriteCounter]
            newImage = app.scaleImage(sprite, .75**(app.rows - row))
        elif isinstance(zombie, PoleVaulter):
            newImage = app.scaleImage(app.PoleVaulterScaled, .75**(app.rows - row))
        elif isinstance(zombie, NewspaperZombie):
            newImage = app.scaleImage(app.NewspaperScaled, .75**(app.rows - row))
        canvas.create_image(x, y, image=ImageTk.PhotoImage(newImage))

def drawPea(app, canvas):
    #not projectile motion bc of how "fast" it's moving
    for (x, y, vPea) in app.pea:
        row, col = getGridCell(app, x, y)
        newImage = app.scaleImage(app.DropletScaled, .75**(app.rows - row))
        canvas.create_image(x, y, image = ImageTk.PhotoImage(newImage))

def drawCoconut(app, canvas):
    for (x, y, vCoco) in app.coconut:
        row, col = getGridCell(app, x, y)
        newImage = app.scaleImage(app.TPScaled, .75**(app.rows - row))
        canvas.create_image(x, y, image = ImageTk.PhotoImage(newImage))

def drawGameOver(app, canvas):
    canvas.create_rectangle(0, 0, app.width, app.height, fill = "black")
    canvas.create_text(app.width/2, app.height/2, text = "YOU LOSE", fill = "white",
    font = "Arial 25 bold")
    canvas.create_text(app.width/2, app.height/2 + 20, text = "Click anywhere to restart",
    fill = "white", font = "Arial 12 bold")

def drawPlantPackets(app, canvas):
    #draw those seed packets in a row at the top
    #should also have an offset for the sun count
    #also says "loading" if plant packet not done refreshing
    for c in range(len(app.plantTypes)):    #draw boxes around seed packets
        x0, y0, x1, y1 = cellBounds(app, 0, c)
        x0 += app.boxWidth
        x1 += app.boxWidth
        middleX = (x0 + x1)/2
        rightX = .25*x0 + .75*x1
        botY = .1*y0 + .9*y1
        middleY = (y0 + y1)/2
        lowerY = .25*y0 + .75*y1
        upperY = .75*y0 + .25*y1
        avgY = (upperY + middleY)/2
        plant = app.plantTypes[c]
        canvas.create_rectangle(x0, y0, x1, y1)
        if c == 0:
            newImage = app.scaleImage(app.SunflowerScaled, 1/2.3)
        elif c == 1:
            newImage = app.scaleImage(app.PeashooterScaled, 1/2.3)
        elif c == 2:
            newImage = app.scaleImage(app.CherryScaled, 1/2.3)
        elif c == 3:
            newImage = app.scaleImage(app.WallnutScaled, 1/2.3)
        elif c == 4:
            newImage = app.scaleImage(app.WatermelonScaled, 1/2.3)
        elif c == 5:
            newImage = app.scaleImage(app.CoconutScaled, 1/2.3)
        elif c == 6:
            newImage = app.scaleImage(app.ShovelScaled, 1/4)
            avgY = middleY
        canvas.create_image(middleX, avgY, image = ImageTk.PhotoImage(newImage))
        if c < len(app.plantTypes) - 1: #shovel has no cost
            canvas.create_text(middleX, lowerY, text = app.plantTypes[c].getCost(), font = "Arial 12 bold")
            if plant.getLoad() > (time.time() - app.plantLoading[c]):
                canvas.create_text(rightX, botY, text = "Loading...")

def drawSunCount(app, canvas):
    #sun count in top left corner, before plant packets
    x0, y0, x1, y1 = cellBounds(app, 0, 0)
    middleX = (x0 + x1)/2
    middleY = .75*y0 + .25*y1
    lowerY = .25*y0 + .75*y1
    canvas.create_rectangle(x0, y0, x1, y1)
    canvas.create_text(middleX, lowerY, text = app.sun, font = "Arial 12 bold")
    canvas.create_image(middleX, middleY, image = ImageTk.PhotoImage(app.TPScaled))

def drawPlants(app, canvas):
    #draw plants on the garden
    for plant in app.plantsOnscreen.values():
        row = plant.getRow()
        col = plant.getCol()
        xTopLeft, xTopRight, xBottomLeft, xBottomRight, y0, y1 = gridCellBounds(app, row, col)
        x = (xBottomLeft + xBottomRight)/2
        y = (y0 + y1)/2
        if isinstance(plant, Sunflower):
            newImage = app.scaleImage(app.SunflowerScaled, .75**(app.rows - row))
        elif isinstance(plant, PeaShooter):
            newImage = app.scaleImage(app.PeashooterScaled, .75**(app.rows - row))
        elif isinstance(plant, CherryBomb):
            newImage = app.scaleImage(app.CherryScaled, .75**(app.rows - row))
        elif isinstance(plant, WallNut):
            newImage = app.scaleImage(app.WallnutScaled, .75**(app.rows - row))
        elif isinstance(plant, Watermelon):
            newImage = app.scaleImage(app.WatermelonScaled, .75**(app.rows - row))
        elif isinstance(plant, Cannon):
            newImage = app.scaleImage(app.CoconutScaled, .75**(app.rows - row))       
        canvas.create_image(x, y, image=ImageTk.PhotoImage(newImage))

def drawSun(app, canvas):
    for (x, y, t) in app.sunSpots:
        row, col = getGridCell(app, x, y)
        newImage = app.scaleImage(app.TPScaled, .75**(app.rows - row))
        canvas.create_image(x, y, image = ImageTk.PhotoImage(newImage))

#would like to thank my math teachers for teaching how to parameterize x and y in terms of t
#i now have an answer for "when are we going to use this in real life"
def drawWatermelon(app, canvas):
    #figure out endpoint based on where zombie will move, for now we're going to choose it
    #same y coord, different x
    for i in range(len(app.watermelon)):
        r, c, startingTime, newX = app.watermelon[i]    #will change later
        xTopLeft, xTopRight, xBottomLeft, xBottomRight, y0, y1 = gridCellBounds(app, r, c)
        middleX = (xBottomLeft + xBottomRight)/2
        middleY = (y0 + y1)/2   #may change depending on animation?
        timeDiff = time.time() - startingTime
        x = ((newX - middleX))*timeDiff + middleX   #x parameterize w t (b-a)t + a
        y = 2.5*app.boxHeight*(timeDiff)*(timeDiff - 1) + middleY   #y parameterize w t? (t-a)(t-b) + c, scaled so peak is more noticeable
        newImage = app.scaleImage(app.TPScaled, .75**(app.rows - r))
        canvas.create_image(x, y, image = ImageTk.PhotoImage(newImage))

def drawPlantChosen(app, canvas):
    #draw the plant as it's being dragged around
    x, y = app.plantChosenCoord
    if x != -1 and y != -1 and app.plantChosen != None:
        if isinstance(app.plantChosen, Sunflower):
            newImage = app.scaleImage(app.SunflowerScaled, 1/2.3)
            canvas.create_image(x, y, image = ImageTk.PhotoImage(newImage))
        elif isinstance(app.plantChosen, PeaShooter):
            newImage = app.scaleImage(app.PeashooterScaled, 1/2.3)
            canvas.create_image(x, y, image = ImageTk.PhotoImage(newImage))
        elif isinstance(app.plantChosen, CherryBomb):
            newImage = app.scaleImage(app.CherryScaled, 1/2.3)
            canvas.create_image(x, y, image = ImageTk.PhotoImage(newImage))
        elif isinstance(app.plantChosen, WallNut):
            newImage = app.scaleImage(app.WallnutScaled, 1/2.3)
            canvas.create_image(x, y, image = ImageTk.PhotoImage(newImage))
        elif isinstance(app.plantChosen, Watermelon):
            newImage = app.scaleImage(app.WatermelonScaled, 1/2.3)
            canvas.create_image(x, y, image = ImageTk.PhotoImage(newImage))
        elif isinstance(app.plantChosen, Cannon):
            newImage = app.scaleImage(app.CoconutScaled, 1/2.3)
            canvas.create_image(x, y, image = ImageTk.PhotoImage(newImage))
        elif app.plantChosen == "Shovel":
            newImage = app.scaleImage(app.ShovelScaled, 1/4)
            canvas.create_image(x, y, image = ImageTk.PhotoImage(newImage))

def drawProgressBar(app, canvas):
    totalLength = .75*app.width
    xLeft = app.width/2 - totalLength/2
    xRight = app.width/2 + totalLength/2
    if app.gameType == "short":
        progressLength = (time.time() - app.totalTime)/(60*3) * totalLength
        if progressLength > totalLength:
            progressLength = totalLength
    elif app.gameType == "long":
        progressLength = (time.time() - app.totalTime)/(60*5) * totalLength
        if progressLength > totalLength:
            progressLength = totalLength
    canvas.create_rectangle(xLeft, app.height - 1.5*app.margin, xRight,
    app.height - .5*app.margin,fill = "gray")
    canvas.create_rectangle(xLeft, app.height - 1.5*app.margin, xLeft + progressLength,
    app.height - .5*app.margin, fill = "purple")
    canvas.create_text(app.width/2, app.height - app.margin, text = "Progress")

def drawGameWon(app, canvas):
    canvas.create_rectangle(0, 0, app.width, app.height, fill = "black")
    canvas.create_text(app.width/2, app.height/2, text = "YOU WIN!!!!", fill = "white",
    font = "Arial 25 bold")
    canvas.create_text(app.width/2, app.height/2 + 20, text = "Click anywhere to restart",
    fill = "white", font = "Arial 12 bold")

def drawTimesUp(app, canvas):
    canvas.create_rectangle(0, 0, app.width, app.height, fill = "black")
    canvas.create_text(app.width/2, app.height/2, text = "Time's up!", fill = "white",
    font = "Arial 25 bold")
    canvas.create_text(app.width/2, app.height/2 + 40, text = "You killed " + str(app.zombiesKilled) + " zombies!",
    fill = "white", font = "Arial 12 bold")
    canvas.create_text(app.width/2, .75*app.height,
    text = "Don't forget to input your name in the terminal to save your score! (Enter when done.)",
    fill = "white", font = "Arial 12 bold")
    canvas.create_text(app.width/2, .85*app.height, text = "Name: " + app.name,
    fill = "white", font = "Arial 12 bold")


def splashScreenMode_redrawAll(app, canvas):
    canvas.create_rectangle(0, 0, app.width, app.height, fill = "yellow")
    if app.displayScores:
        leaderboard = readLeaderboard()
        d = dict()
        for row in leaderboard:
            name = row[0]
            score = int(row[1])
            if score not in d:
                s = set()
                s.add(name)
                d[score] = s
            else:
                d[score].add(name)
        scoresSorted = sorted(d)
        for i in range(len(scoresSorted)):
            canvas.create_text(app.width/2, app.margin*(len(scoresSorted) - i+1),
            text = f"{d[scoresSorted[i]]} has a score of {scoresSorted[i]}")
        canvas.create_text(app.width/2, .75*app.height,
        text = "Press R to go back to starting screen")
    else:
        canvas.create_text(app.width/2, app.height/2, text = "Welcome! Please choose your game mode:",
        font = "Arial 26 bold")
        canvas.create_text(.25*app.width, .75*app.height, text = "Q = Standard mode")
        canvas.create_text(.75*app.width, .75*app.height, text = "P = Scoring mode")
        canvas.create_text(.5*app.width, .75*app.height, text = "R = see all scores")

def splashScreenMode_keyPressed(app, event):
    if event.key == "Q" or event.key == "q":
        appRestarted(app)
        app.mode = "gameMode"
        app.gameType = "short"
        pygame.mixer.music.play(-1, 0.0)    #loop
        pygame.mixer.music.set_volume(.1)
        app.pauseMusic = False
        app.gameWon = False
        app.timesUp = False
        app.totalTime = app.time0 = time.time()
    elif event.key == "P" or event.key == "p":
        appRestarted(app)
        app.mode = "gameMode"
        app.gameType = "long"
        pygame.mixer.music.play(-1, 0.0)    #loop
        pygame.mixer.music.set_volume(.1)
        app.pauseMusic = False
        app.totalTime = app.time0 = time.time()
        app.gameWon = False
        app.timesUp = False
    elif event.key == "R" or event.key == 'r':
        app.displayScores = not app.displayScores
        app.gameWon = False
        app.timesUp = False

#github.com/grvcekim/15112-databases/
def updateLeaderboard(leaderboard, name, score):
    with open('leaderboard.csv', mode='w', newline = '') as f:
        writer = csv.writer(f)
        updated = False
        for row in leaderboard:
            if row[0] == name:
                row[1] = score
                updated = True
                break
        if not updated:
            leaderboard.append([name, score])
        for row in leaderboard:
            writer.writerow(row)

#github.com/grvcekim/15112-databases/
def readLeaderboard():
    with open('leaderboard.csv', mode='r') as f:
        reader = csv.reader(f)
        leaderboard = [row for row in reader]
    return leaderboard


runApp(width = 1000, height = 600)
#garden is 5 rows x 9 columns


"""
sprite strips: https://www.spriters-resource.com/ds_dsi/pvszds/sheet/138662/
https://en.wikipedia.org/wiki/3D_projection

3D graphics minilecture:
https://docs.google.com/presentation/d/1N4t5eFL35XkWzpUTBSRw-gBM3bbsdJWmRSWX94lgB2A/edit#slide=id.p

Drawing a grid w/ 1-pt perspective:
https://juliannakunstler.com/art1_1pt_ch_board.html

scaling images, animation, splashscreen, events: https://www.cs.cmu.edu/~112/notes/notes-animations-part4.html

links for pics with the proposal/storyboard links or picture links doc

used photoshop to paste things together (learned how to use in art class in middle and hs)
learned math equations in middle and high school algebra, and also physics 1

database, storing scores:
https://docs.google.com/presentation/d/1EgbL7dtYAz6Gav663QfvXUhVlYR7swqZJT2hb36VimQ/edit#slide=id.ga6abfcf73c_0_168

side note: i did try caching the photos for efficiency and stuff but apparently
scaled photos aren't recognized as different photos?, so i couldn't use it :(

pygame music documentation: https://www.pygame.org/docs/ref/music.html
"""