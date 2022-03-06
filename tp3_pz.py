###################
#Name: Freda Su
#Andrew ID: fysu
#tp3 woohoo
###########

import copy, math, random, time
import sys

from cmu_112_graphics import *

class Plant(object):
    def __init__(self):
        self.health = 10    #amt of hits it can take from zombie before dying
        self.cost = 5  #amt it costs to buy it
        self.load = 3    #amt of time it takes to reload next "plant" in the seed packets?
        self.type = "Plant"
        self.damage = 1 #for scaling purposes later

    def __repr__(self):
        return self.type

    def getHealth(self):
        return self.health
    
    def getCost(self):
        return self.cost
    
    def getLoad(self):
        return self.load
    
    def setRow(self, row):
        self.row = row
    
    def setCol(self, col):
        self.col = col
    
    def getRow(self):
        return self.row
    
    def getCol(self):
        return self.col
    
    def isAttacked(self, attack):
        self.health -= attack

    def getDamage(self):
        return self.damage

    def getAttackType(self):
        return "None"
    
    def setTime(self, time):
        self.time = time
    
    def getTime(self):
        return self.time

class PeaShooter(Plant):
    #hand sanitizer, attacks generic zombie (virus) or variant best
    def __init__(self):
        super().__init__()
        self.type = "PeaShooter"
    
    def getDamage(self):
        return self.damage
    
    def getAttackType(self):
        return "Sanitizer"
    
    def getSpeed(self):
        return 50

class Sunflower(Plant):
    #produces the toilet paper currency
    def __init__(self):
        super().__init__()
        self.cost //= 2
        self.type = "Sunflower"
        self.damage = 0
        self.load = 1

class WallNut(Plant):
    #PPE "masks"
    def __init__(self):
        super().__init__()
        self.health *= 100
        self.cost *= 1.5
        self.cost = int(self.cost)
        self.load *= 6
        self.type = "WallNut"
        self.damage = 0

class CherryBomb(Plant):
    def __init__(self):
        super().__init__()
        self.cost *= 1.5
        self.cost = int(self.cost)
        self.load *= 1.5
        self.damage *= 5
        self.type = "Cherry Bomb"
    
    def getDamage(self):  #should be called whenever planted
        #insert some sound effect here?
        #how to do damage on nearby zombies?
        #defeats a 3x3 grid of zombies (and plants)
        return self.damage
    
    def getAttackType(self):
        return "Fire"

class Watermelon(Plant):
    #maybe this lobs toilet paper, who knows
    def __init__(self):
        super().__init__()
        self.cost *= 2
        self.damage *= 5
        self.type = "Watermelon"
    
    def getAttackType(self):
        return "TP" #idk

class Cannon(Plant):
    #shoots toilet paper rolls i guess
    #a difference here is that you have to click on it in order to fire
    def __init__(self):
        super().__init__()
        self.cost *= 3
        self.type = "Cannon"
        self.damage *= 8
    
    def getAttackType(self):
        return "TP"
    
    def getSpeed(self):
        return 100   #may change

class Zombie(object):
    #all features that zombies have
    def __init__(self):
        self.health = 10    #regular zombie health
        self.speed = .5  #will change depending
        self.attack = 1 #deals 1 damage each attack
        self.type = "Zombie"
        self.xCoord = 1000   # x coord starts at the far left of screen

    def __repr__(self):
        return self.type

    def isAttacked(self, damageLevel, attackType):  #will pass in attack damage from plant
        self.health -= damageLevel
    
    def getHealth(self):
        return self.health
    
    def getSpeed(self):
        return self.speed
    
    def move(self, step):
        #take step fxn, loop thru list of zombies
        self.xCoord -= step  #start on the right, move to the left
    
    def setRow(self, row):  #give actual row for zombie, instead of -1 default
        self.row = row
    
    def getRow(self):
        return self.row
    
    def getX(self):
        return self.xCoord
    
    def getAttack(self):
        return self.attack
    
    def setXCoord(self, x):
        self.xCoord = x

class RegularZombie(Zombie):
    #your generic virus strain
    def __init__(self):
        super().__init__()

class ConeheadZombie(Zombie):
    #a mutated, slightly stronger strain that moves faster as well
    def __init__(self):
        super().__init__()
        self.health *= 1.5
        self.speed *= 1.25
        self.type = "Conehead"

class BucketheadZombie(Zombie):
    #even stronger virus mutant! faster, more durable, more attack power!
    def __init__(self):
        super().__init__()
        self.health *= 4
        self.speed *= 1.5
        self.attack *= 2
        self.type = "Buckethead"

class PoleVaulter(Zombie):
    #the Karen, represented by pole vaulting over your defensive wallnut mask :(
    def __init__(self):
        super().__init__()
        self.health *= 1.2
        self.speed *= 2 #before pole vaulting, then slows down
        self.type = "Pole Vaulter"
        self.vaulted = False
    
    def vault(self, boxWidth):    #once vaulted over plant, slows down
        self.speed /= 3
        self.xCoord -= boxWidth
        self.vaulted = True
    
    def getVaultStatus(self):
        return self.vaulted

class NewspaperZombie(Zombie):
    #the fake news zombie that hates it when you destroy his newspaper
    def __init__(self):
        super().__init__()
        self.origHealth = self.health   #for halfway health purposes later
        self.health *= 2
        self.speed /= 4
        self.type = "Newspaper"
        self.hasNewspaper = True

    def isAttacked(self, damageLevel, attackType):
        self.health -= damageLevel
        if self.health <= self.origHealth and self.hasNewspaper:  #newspaper now gone, he's angry
            self.speed *= 4*3.5   #3.5x the default speed
            self.attack *= 2    #more lethal when angry
            self.hasNewspaper = False   #only want to increase the speed once

class Wizard(Zombie):
    #your internet lag is never late. nor is it ever early. it lags precisely when it means to.
    #or maybe the only way to kill it is with mouse clicks
    def __init__(self):
        super().__init__()
        self.health *= 3
        self.type = "Wizard"
    
    def isAttacked(self, damageLevel, attackType):
        if attackType == "Click":    #you must kill wifi lag with repeated, frustrated clicking!
            self.health -= damageLevel
        else: #but for sake of gameplay, we'll allow other types of attacks
            self.health -= damageLevel*.2   #but it doesn't do as much damage
