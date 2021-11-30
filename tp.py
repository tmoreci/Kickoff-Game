#Trevor Moreci ; tmoreci
#term project

import player
import levels
import highScores


from cmu_112_graphics import *
import random, math
from tkinter import *


# code here

def appStarted(app): #defines variables necessary for app
    app.margin = 50
    app.fieldWidth = app.width - 2*app.margin
    app.fieldHeight = app.height - 2*app.margin
    app.lines = 12
    app.player = player.Player(app.margin + app.fieldWidth//2, 
            app.margin + (app.fieldHeight//app.lines) * (app.lines-1) )
    app.gameOver = False
    app.touchdown = False
    app.level = 1
    app.defense = levels.getLevel(app)[0]
    app.blockers = levels.getLevel(app)[1]
    app.score = 0
    app.gameStarted = False
    app.teamScreen = False
    app.digits = "0123456789"
    app.endZone = "None"
    app.playerColor = "black"
    app.blockerColor = "yellow"
    app.finished = False
    app.numLevels = 5
    app.speedBumps= []
    app.boost = randomBoost(app)
    app.boosted = False
    app.hitBump = False
    app.leaderboard = False

    pass

def randomBumps(app): #creates random speedbumps depending on level
    result = []
    i =1
    for i in range(app.level):
        top = app.margin + (app.fieldHeight//app.lines)+5
        bottom = app.height-app.margin - (app.fieldHeight//app.lines)*2-5
        x = random.randint(app.margin +5, app.margin + app.fieldWidth -5)
        y = random.randint(top,bottom)
        speedBump= player.SpeedBump(x,y,"red")
        result.append(speedBump)
    return result



def randomBoost(app): #creates a player of class boost at a random position
    x = random.randint(app.margin +5, app.margin + app.fieldWidth -5)
    top = app.margin + (app.fieldHeight//app.lines)+5
    bottom = app.height-app.margin - (app.fieldHeight//app.lines)-5
    y = random.randint(top,bottom)
    boost = player.Boost(x,y,"yellow")
    if boost.blocked(app.player): #makes sure boost doesn't spawn on player
        return randomBoost(app)
    app.speedBumps+= randomBumps(app)
    return boost

def mousePressed(app,event):
    #starts game if click in the start box 
    #goes to team screen if click in team screen box
    if not app.gameStarted:
        if event.x >= app.width//5 and event.x <= app.width//5 *4:
            if event.y >= app.height//2 and event.y <= app.height//10*6:
                app.gameStarted = True
            if event.y >= app.height//10*7 and event.y <= app.height//10*8:
                app.teamScreen = True
            if event.y >= (app.height//10 *9 -20) and event.y<= (app.height -20):
                app.leaderboard = True
        
def resetLevel(app): #resets everything for new level
    app.defense = levels.getLevel(app)[0]
    app.blockers = levels.getLevel(app)[1]
    app.player = player.Player(app.margin + app.fieldWidth//2, 
        app.margin + (app.fieldHeight//app.lines) * (app.lines-1) )
    app.player.color = app.playerColor
    for blocker in app.blockers:
        blocker.color = app.blockerColor
    app.touchdown = False
    app.boosted = False
    app.speedBumps = []
    app.boost = randomBoost(app)

    

def chooseTeam(app,x): 
    #gets player, blocker, and end zone colors based on team choice
    ind = x-1
    colors = ["black","purple","silver","blue","red"]
    colors2 = ["gold","black","blue","red","yellow"]
    teams = ["Steelers","Ravens","Lions","Giants","Chiefs"]
    app.playerColor = colors[ind]
    app.blockerColor = colors2[ind]
    app.player.color = app.playerColor
    app.endZone = teams[ind]
    for blocker in app.blockers:
        blocker.color = app.blockerColor


def keyPressed(app,event):
    if app.leaderboard:
        if event.key == "r":
            appStarted(app)
    if app.teamScreen:
        if event.key in app.digits:
            chooseTeam(app,int(event.key))
            app.teamScreen = False
    if app.gameOver or app.finished: #restarts game if r is clicked
        if event.key == "r":
            highScores.updateLeaderBoard(app)
            appStarted(app)
    if app.touchdown:
        if event.key == "Space":
            #resets defense, blockers, player if next level 
            resetLevel(app)
    if app.gameOver or app.touchdown or not app.gameStarted or app.finished: 
        #can't move if level is finished or game isn't started
        return
    #keys move player if move is valid
    if event.key == "Up":
        app.player.cy -= app.player.speed
        if app.player.outBounds(app):
            app.player.cy += app.player.speed
    if event.key == "Down":
        app.player.cy += app.player.speed
        if app.player.outBounds(app):
            app.player.cy -= app.player.speed
    if event.key == "Left":
        app.player.cx -= app.player.speed
        if app.player.outBounds(app):
            app.player.cx += app.player.speed
    if event.key == "Right":
        app.player.cx += app.player.speed
        if app.player.outBounds(app):
            app.player.cx -= app.player.speed
    if event.key == "Space":
        app.player.makeBestMove(app)
    pass

def runAI(app):
    for defender in app.defense: #moves defender and checks if it makes a tackle
        defender.onTimerFired(app,app.player)
        if defender.tackled(app.player):
            app.gameOver = True
    for blocker in app.blockers: #calls action for each blocker
        blocker.onTimerFired(app)
    for defender in app.defense:
        for blocker in app.blockers:
            #checks if blocker can block defender
            if blocker.blocked(defender):
                blocker.blocking = True
                defender.blocked = True
                if blocker.blockTime % 30 == 0:
                    #blockers block for 3 seconds then disappear
                    app.blockers.remove(blocker)
                    defender.blocked = False
    if len(app.blockers)== 0:
        for defender in app.defense:
            defender.blocked = False
                

def timerFired(app):
    if app.gameOver or app.touchdown or not app.gameStarted or app.finished:
        return
    if app.player.touchdown(app): #checks if player scored
        app.score += 7
        app.level +=1
        if app.level > app.numLevels:
            app.finished = True
        else:
            app.touchdown = True
    if app.boost.blocked(app.player) and not app.boosted: 
        #checks if player got boost
        app.score +=3
        app.boosted = True
    for bump in app.speedBumps:
        if bump.blocked(app.player):
            app.gameOver = True
            app.hitBump = True
    app.player.onTimerFired()
    runAI(app) #runs defenders and players action
    pass

def drawField(app,canvas): #draws the football field
    canvas.create_rectangle(app.margin,app.margin, app.margin +app.fieldWidth,
        app.margin + app.fieldHeight,width = 15)
    for i in range(app.lines):
        left = app.margin 
        top = app.margin + (app.fieldHeight//app.lines)*i
        right = left + app.fieldWidth
        bottom = top + (app.fieldHeight//app.lines)
        if i == 0:
            color = "blue"
        elif i == app.lines -1:
            color = app.blockerColor
        else:
            color = "green"
        canvas.create_rectangle(left,top,right, bottom,fill = color)
    if not app.gameOver and not app.touchdown and not app.finished:
        canvas.create_text(app.margin + app.fieldWidth//2, 
                app.margin + app.fieldHeight//2, text = "112", font = "Arial 35",
                fill = "white")
    canvas.create_text(app.margin + app.fieldWidth//2, 
            app.margin + (app.fieldHeight//app.lines)//2, text = "End Zone",
                font = "Arial 43", fill = "yellow" )
    canvas.create_text(app.margin + app.fieldWidth//2,app.margin*14.5 - 10,
        text = app.endZone, font = "Arial 43",fill = app.playerColor)
    

def drawHome(app,canvas): #draws home screen
    canvas.create_rectangle(0,0,app.width,app.height,fill = "blue")
    canvas.create_text(app.width//2, app.height//3, text = "112 Kickoff",
        font = "Arial 50", fill = "yellow")
    canvas.create_rectangle(app.width//5, app.height//2, app.width//5 *4, 
        app.height//10 *6, fill = "yellow")
    midWidth = (app.width//5*4 - app.width//5)//2 + app.width//5
    midHeight = (app.height//10*6 - app.height//2)//2 + app.height//2
    canvas.create_text(midWidth,midHeight, text = "Start", font = "Arial 40")
    canvas.create_rectangle(app.width//5, app.height//10 *7, app.width//5*4,
        app.height//10 *8, fill = "yellow")
    midHeight2 = (app.height//10*8 - app.height//10*7)//2 + app.height//10*7
    canvas.create_text(midWidth,midHeight2,text = "Choose Team",
        font = "Arial 25")
    midHeight3 = (app.height - app.height//10*9)//2 + app.height//10*9
    canvas.create_rectangle(app.width//5, app.height//10 *9 -20, app.width//5*4,
        app.height-20, fill = "yellow")
    canvas.create_text(midWidth,midHeight3-20,text = "LeaderBoard",
        font = "Arial 30")
    
def drawTeamBoard(app,canvas): #draws the board with all the team options
    width = app.width//2
    dist = app.height//20
    boxWidth = app.width//3
    text = "Arial 17"
    canvas.create_rectangle(0,0,app.width,app.height,fill = "blue")
    canvas.create_text(app.width//2, app.height//10, 
        text = "Click Number for Team", font = "Arial 25", fill = "yellow")
    canvas.create_rectangle(boxWidth,dist*3+5,boxWidth*2,dist*5-5,
        fill = "yellow")
    canvas.create_text(width,dist*4, text = "1. Steelers", font = text)
    canvas.create_rectangle(boxWidth,dist*5+5,boxWidth*2,dist*7-5,
        fill = "purple")
    canvas.create_text(width,dist*6, text = "2. Ravens", font = text)
    canvas.create_rectangle(boxWidth,dist*7+5,boxWidth*2,dist*9-5,
        fill = "silver")
    canvas.create_text(width,dist*8, text = "3. Lions", font = text, 
        fill = "blue")
    canvas.create_rectangle(boxWidth,dist*9+5,boxWidth*2,dist*11-5,
        fill = "red")
    canvas.create_text(width,dist*10, text = "4. Giants", font = text,
        fill="blue")
    canvas.create_rectangle(boxWidth,dist*11+5,boxWidth*2,dist*13-5,
        fill = "yellow")
    canvas.create_text(width,dist*12, text = "5. Chiefs", font = text, 
        fill = 'red')
    

def drawPlayers(app,canvas): #draws all the players on the screen
    app.player.draw(app,canvas)
    if not app.boosted:
        app.boost.draw(canvas,5)
    for defender in app.defense:
        defender.draw(app,canvas)
    for blocker in app.blockers:
        blocker.draw(app,canvas)
    for bump in app.speedBumps:
        bump.draw(canvas)
    
def drawLeaderboard(app,canvas): #draws leaderboard scren
    canvas.create_rectangle(0,0,app.width,app.height,fill = "blue")
    topScore, topTeam = highScores.findBest()
    secondScore, secondTeam = highScores.secondBest()
    thirdScore, thirdTeam = highScores.thirdBest()
    width = app.width//2
    dist = app.height//20
    canvas.create_text(app.width//2, app.height//10, 
        text = "Leaderboard", font = "Arial 30", fill = "yellow")
    canvas.create_text(width,dist*4, text = f"1. {topTeam}: {topScore}", 
        font= "Arial 25")
    canvas.create_text(width,dist*6, text = f"2. {secondTeam}: {secondScore}",
        font = "Arial 25")
    canvas.create_text(width,dist*8, text = f"3. {thirdTeam}: {thirdScore}",
        font = "Arial 25")
    canvas.create_text(width,dist*12,text = "Press r to return Home",
        font = "Arial 20")

def redrawAll(app,canvas):
    if not app.gameStarted and not app.teamScreen and not app.leaderboard:
        #draws home screen if game isn't started
        drawHome(app,canvas)
        return
    if not app.gameStarted and app.teamScreen and not app.leaderboard:
        drawTeamBoard(app,canvas)
        return
    if not app.gameStarted and not app.teamScreen and app.leaderboard:
        drawLeaderboard(app,canvas)
        return
    drawField(app,canvas)
    drawPlayers(app,canvas)
    canvas.create_text(35,10,text= "Score:"+str(app.score))
    if app.gameOver: #game over text
        if app.hitBump:
            word = "Speed Bump!"
        else:
            word = "TACKLED!"
        canvas.create_text(app.width//2,app.height//2, text = word, 
            font = "Arial 35", fill = "white")
        canvas.create_text(app.width//2, app.height//3*2, 
            text = "press r to restart", font = "Arial 20", fill = "white")
    if app.touchdown: #text for next level
        canvas.create_text(app.width//2,app.height//2, text = "TOUCHDOWN!!", 
            font = "Arial 35", fill = "white")
        canvas.create_text(app.width//2, app.height//3*2, 
            text = "press space for next level", font = "Arial 20", 
                fill = "white")
    if app.finished: #text that game has been completed
        canvas.create_text(app.width//2,app.height//2, text = "Game Completed!", 
            font = "Arial 35", fill = "white")
        canvas.create_text(app.width//2, app.height//3*2, 
            text = "press r to restart", font = "Arial 20", fill = "white")

    pass




runApp(width=400, height=800)