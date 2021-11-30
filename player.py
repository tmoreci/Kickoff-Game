#Trevor Moreci
#tmoreci
#file making the class for the player and defenders

from cmu_112_graphics import *
import random, math
import tracking



class Player(object): #
    def __init__(self,cx,cy):
        self.r = 10
        self.speed = 3
        self.cx = cx
        self.cy = cy
        self.color = "black"
        self.acceleration = 0.002

    def draw(self,app,canvas): #draws player
        canvas.create_oval(self.cx - self.r, self.cy - self.r, self.cx +self.r,
            self.cy + self.r,fill = self.color)
        
    def outBounds(self,app): #checks if player is in bounds
        if self.cx - self.r < app.margin:
            return True
        if self.cx +self.r > app.width - app.margin:
            return True
        if self.cy -self.r < app.margin:
            return True
        if self.cy + self.r > app.height - app.margin:
            return True
        for blocker in app.blockers:
            if blocker.blocked(self): #so player can't collide with blockers
                return True
        return False
    
    def touchdown(self,app): #checks if player scored
        if self.cy < app.margin + (app.fieldHeight//app.lines):
            return True
    
    def onTimerFired(self):
        if self.speed >6:
            self.acceleration = 0
        self.speed += self.speed *self.acceleration

    def makeBestMove(self,app):
        direct = tracking.playerBestMove(self,app)
        self.cx += (self.speed * direct[0])
        self.cy += (self.speed * direct[1])

class Defender(Player): #defines defenders
    def __init__(self,cx,cy,r,speed):
        self.cx = cx
        self.cy = cy
        self.speed = speed
        self.color = "brown"
        self.r = r
        self.blocked = False

    def onTimerFired(self,app,other):
        if self.blocked: #can't move if blocked
            return
        #finds best move and makes it
        bestMove = tracking.bestMove(app,self,app.player)
        self.cx += self.speed * bestMove[0]
        self.cy += self.speed * bestMove[1]
    
    
    def tackled(self,other): #checks if defender makes tackle
        #code from hw14 starter file
        return (math.sqrt((other.cx - self.cx)**2 +
                                (other.cy - self.cy)**2)
                                        < self.r + other.r)
    


class Blocker(Player):
    def __init__(self,cx,cy):
        self.r = 10
        self.speed = 2
        self.cx = cx
        self.cy = cy
        self.color = "brown"
        self.blocking = False
        self.blockTime = 1

    def onTimerFired(self,app):
        if self.blocking: #can't move if blocking
            self.blockTime +=1
            return
        #finds closest defender and best move towards that defender and makes it
        defender = tracking.findDefender(app,self)
        bestMove = tracking.bestBlockMove(app,self,defender)
        self.cx += self.speed * bestMove[0]
        self.cy += self.speed * bestMove[1]

    def blocked(self,other): #checks if collided with defender for block
        return (math.sqrt((other.cx - self.cx)**2 +
                                (other.cy - self.cy)**2)
                                        < self.r + other.r)
    

class SmartDefender(Defender):
    def onTimerFired(self,app,other):
        if self.blocked: #can't move if blocked
            return
        #finds best move and makes it
        bestMove = tracking.bestSmartMove(app,self)
        self.cx += self.speed * bestMove[0]
        self.cy += self.speed * bestMove[1]

class FunnelDefender(Defender):
    def __init__(self,cx,cy,r,speed,target):
        super().__init__(cx,cy,r,speed)
        self.target = target
        self.blocked = False
    
    def onTimerFired(self,app,other):
        if self.blocked:
            return
        if app.player.cy > self.target[1]:
            bestMove = tracking.funnelMove(app,self,self.target)
        else:
            bestMove = tracking.bestMove(app,self,app.player)
        self.cx += self.speed * bestMove[0]
        self.cy += self.speed * bestMove[1]
        

class Boost(Blocker): #defines the boost ball for player
    def __init__(self,cx,cy,color):
        self.cx = cx
        self.cy = cy
        self.r = 5
        self.color = color

    def draw(self,canvas,numPoints):
        lst = []
        angle = math.pi *3/2 #start angle
        change = 2*math.pi / numPoints #change in angle each point
        smallR = self.r*(3/8)
        for i in range(numPoints):
            #finds the outer and inner point at each iteration and adds to list
            x1 = self.cx +self.r*math.cos(angle+change*i)
            y1 = self.cy+math.sin(angle +change*i)*self.r
            x2 = self.cx + math.cos(angle +change*i+change/2)*smallR
            y2 = self.cy+math.sin(angle + change*i+ change/2)*smallR
            lst.extend([x1,y1,x2,y2])
        canvas.create_polygon(lst,fill=self.color)

class SpeedBump(Boost): #class for speed bumps
    def draw(self,canvas):
        canvas.create_oval(self.cx - self.r,self.cy - self.r,self.cx + self.r,
            self.cy + self.r, fill = self.color)
        canvas.create_line(self.cx - self.r,self.cy - self.r,self.cx + self.r,
            self.cy + self.r, width = 3)









