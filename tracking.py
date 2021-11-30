#code finding best optimal move for defender and blocker

import player 
import levels
import math



def distance(x0, y0, x1, y1): #from course notes 6/16
    return ((y1-y0)**2 + (x1-x0)**2)**0.5


def bestMove(app,defender,player): #finds best move
    currDistance = distance(defender.cx,defender.cy,player.cx,player.cy)
    bestDistance = currDistance
    direction = (0,0)
    for i in [-1,0,1]:
        for j in [-1,0,1]:
            #loop through all possible directions
            if i == j == 0:
                continue
            newX = defender.cx + (i * defender.speed)
            newY = defender.cy + (j * defender.speed)
            if isValid(app,newX,newY,defender):
                if distance(newX,newY,player.cx,player.cy)< bestDistance:
                    #checks if move is valid and if its shortest distance
                    bestDistance = distance(newX,newY,player.cx,player.cy)
                    direction = (i,j)
    return direction

def isValid(app,x,y,defender):
    #checks if move is valid
    if x - defender.r < app.margin or x + defender.r > app.width - app.margin:
        return False
    if y - defender.r < app.margin or y + defender.r > app.height - app.margin:
        return False
    for elem in app.defense:
        if elem != defender:
            if isColliding(x,y,defender,elem):
                return False
    return True

def isColliding(x,y,defender,other):
    #checks if defender is colliding with another defender 
    return (math.sqrt((other.cx - x)**2 +
                                (other.cy - y)**2)
                                        < 2*defender.r + other.r)

def findDefender(app, blocker): #finds closest defender that isn't blocked
    bestDistance = app.width
    closestDefender = None
    for defender in app.defense:
        dit = distance(blocker.cx,blocker.cy,defender.cx,defender.cy)
        if dit < bestDistance and not defender.blocked:
            bestDistance = dit
            closestDefender = defender
    return closestDefender

def bestBlockMove(app,blocker,defender):
    currDistance = distance(blocker.cx,blocker.cy,defender.cx,defender.cy)
    bestDistance = currDistance
    direction = (0,0)
    for i in [-1,0,1]:
        for j in [-1,0,1]:
            #loop through all possible directions
            if i == j == 0:
                continue
            newX = blocker.cx + (i * blocker.speed)
            newY = blocker.cy + (j * blocker.speed)
            if isValid2(app,newX,newY,blocker):
                if distance(newX,newY,defender.cx,defender.cy)< bestDistance:
                    #checks if move is valid and if its shortest distance
                    bestDistance = distance(newX,newY,defender.cx,defender.cy)
                    direction = (i,j)
    return direction

def isValid2(app,x,y,blocker):
        #checks if move is valid
    if x - blocker.r < app.margin or x + blocker.r > app.width - app.margin:
        return False
    if y - blocker.r < app.margin or y + blocker.r > app.height - app.margin:
        return False
    for elem in app.blockers:
        if elem != blocker: #checks blockers aren't colliding
            if isColliding(x,y,blocker,elem):
                return False
    return True

def bestSmartMove(app,defender):
    currDistance = distance(defender.cx,defender.cy,app.player.cx,app.player.cy)
    bestDistance = currDistance
    direction = (0,0)
    for i in [-1,0,1]:
        for j in [-1,0,1]:
            #loop through all possible directions
            if i == j == 0:
                continue
            newX = defender.cx + (i * defender.speed)
            newY = defender.cy + (j * defender.speed)
            if isValid3(app,newX,newY,defender,i,j):
                if (distance(newX,newY,app.player.cx,app.player.cy)< 
                    bestDistance):
                    #checks if move is valid and if its shortest distance
                    bestDistance = distance(newX,newY,app.player.cx,
                        app.player.cy)
                    direction = (i,j)
    return direction

def isValid3(app,x,y,defender,i,j):
    #checks if move is valid
    if x - defender.r < app.margin or x + defender.r > app.width - app.margin:
        return False
    if y - defender.r < app.margin or y + defender.r > app.height - app.margin:
        return False
    for elem in app.defense:
        if elem != defender:
            if isColliding(x,y,defender,elem):
                return False
    if not pathIsClear(app,x,y,defender,i,j): 
        #checks if there are blockers in the path
        return False
    return True

def pathIsClear(app,x,y,defender,i,j): 
    #checks if a blocker is in the path of the defender
    count = 0
    new = player.Defender(x,y,defender.r,defender.speed)
    for blocker in app.blockers:
        if isColliding(x,y,new,blocker):
            return False
    while inBounds(app,new.cx,new.cy,new):
        new.cx += new.speed * i
        new.cy += new.speed * j
        for blocker in app.blockers:
            if isColliding(new.cx,new.cy,new,blocker):
                return False
    
    return True

def inBounds(app,x,y,defender): #checks if defender is inBounds
    if x - defender.r < app.margin or x + defender.r > app.width - app.margin:
        return False
    if y - defender.r < app.margin or y + defender.r > app.height - app.margin:
        return False
    return True 

def playerBestMove(player,app):
    #finds best move for player
    endZone = (app.margin + app.fieldWidth//app.lines)
    currDistance = player.cy - endZone
    bestDistance = app.fieldHeight
    bestDirection = (0,0)
    for i in [-1,0,1]:
        for j in [-1,0,1]:
            if i == 0 and j ==0:
                continue
            newX = player.cx + (i *player.speed)
            newY = player.cy + (j*player.speed)
            if validMove(app,newX,newY,player):
                if newY - endZone< bestDistance:
                    bestDistance = newY - endZone
                    bestDirection = (i,j)
                if newY - endZone == bestDistance:
                    if defenderInPath(app,newX,newY,i,j):
                        continue
                    newDirection = findDirection((i,j),bestDirection,player,app)
                    bestDirection = newDirection
    return bestDirection

def validMove(app,x,y,player):
    #checks if move is valid for player
    if not inBounds(app,x,y,player):
        return False
    for defender in app.defense:
        if isColliding(x,y,player,defender):
            return False
    for blocker in app.blockers:
        if isColliding(x,y,player,blocker):
            return False
    return True

def findDirection(direct1, direct2,player,app): 
    #finds best direction for player to take
    if direct1 == (0,1):
        return direct1
    if direct2 == (0,1):
        return direct2
    x1 = player.cx + (direct1[0]*player.speed)
    x2 = player.cx + (direct2[0]*player.speed)
    if borderDist(app,x1)> borderDist(app,x2):
        return direct1
    else: 
        return direct2

def borderDist(app,x): #finds closest distance from point to a border
    dist1 = x - app.margin
    dist2 = (app.margin + app.fieldWidth)-x
    if dist1<dist2:
        return dist1
    else:
        return dist2

def defenderInPath(app,x,y,i,j):
        #checks if a blocker is in the path of the defender
    new = player.Player(x,y)
    for defender in app.defense:
        if isColliding(x,y,new,defender):
            return True
    while inBounds(app,new.cx,new.cy,new):
        new.cx += new.speed * i
        new.cy += new.speed * j
        for defender in app.defense:
            if isColliding(new.cx,new.cy,new,defender):
                return True
    
    return False


def funnelMove(app,defender,target):
    currDistance = distance(defender.cx,defender.cy,target[0],target[1])
    bestDistance = currDistance
    direction = (0,0)
    for i in [-1,0,1]:
        for j in [-1,0,1]:
            #loop through all possible directions
            newX = defender.cx + (i * defender.speed)
            newY = defender.cy + (j * defender.speed)
            if isValid(app,newX,newY,defender):
                if distance(newX,newY,target[0],target[1])< bestDistance:
                    #checks if move is valid and if its shortest distance
                    bestDistance = distance(newX,newY,target[0],target[1])
                    direction = (i,j)
    return direction












