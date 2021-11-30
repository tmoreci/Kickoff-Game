#creates the leaderboard of scores


def readFile(path): #from course notes
    with open(path, "rt") as f:
        return f.read()

def writeFile(path, contents): #from course notes
    with open(path, "wt") as f:
        f.write(contents)


def updateLeaderBoard(app): #adds score onto text of all scores
    scoreToWrite = f"{app.score},{app.endZone}\n"
    scores = readFile("scores.txt")
    scores+= scoreToWrite
    f = open("scores.txt","w")
    f.write(scores)
    f.close()

    
    pass

def findBest(): #parses through text and finds best score
    scores = readFile("scores.txt")
    scores = scores.splitlines()
    bestScore = 0
    bestTeam = None
    for score in scores:
        score= score.split(",")
        if int(score[0]) > bestScore:
            bestScore = int(score[0])
            bestTeam = score[1]
    return bestScore, bestTeam

def secondBest(): #parses through text and finds second best score
    bestScore, bestTeam = findBest()
    secondScore = 0
    secondTeam = None
    scores = readFile("scores.txt")
    scores = scores.splitlines()
    for score in scores:
        score = score.split(",")
        if int(score[0]) == bestScore and score[1] == bestTeam:
            continue
        elif int(score[0]) > secondScore:
            secondScore = int(score[0])
            secondTeam = score[1]
    return secondScore, secondTeam

def thirdBest(): #parses through text and finds third highest score
    bestScore, bestTeam = findBest()
    secondScore, secondTeam = secondBest()
    thirdScore = 0
    thirdTeam = None
    scores = readFile("scores.txt")
    scores = scores.splitlines()
    for score in scores:
        score = score.split(",")
        if int(score[0]) == bestScore and score[1] == bestTeam:
            continue
        if int(score[0]) == secondScore and score[1] == secondTeam:
            continue
        elif int(score[0]) > thirdScore:
            thirdScore = int(score[0])
            thirdTeam = score[1]
    return thirdScore, thirdTeam



