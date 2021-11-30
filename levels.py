import player
#creates different levels

def getLevel(app): #gets level from app started
    if app.level == 1:
        return [level1D(app), level1B(app)]
    if app.level == 2:
        return [level2D(app), level1B(app)]
    if app.level == 3:
        return [level3D(app),level1B(app)]
    if app.level == 4:
        return[level4D(app),level1B(app)]
    if app.level == 5:
        return [level5D(app),level1B(app)]
    if app.level == 6:
        return [level6D(app),level1B(app)]

def level1D(app):
    yard = app.fieldHeight//app.lines
    cy = app.fieldWidth//5
    defender1 = player.SmartDefender(app.margin + cy, app.margin +yard,10, 2)
    defender2 = player.Defender(app.margin + 4*cy, app.margin + 3*yard,10,2)
    defender3 = player.Defender(app.margin + app.fieldWidth//2, 4*yard,10,2)
    return [defender1, defender2, defender3]


def level2D(app):
    yard = app.fieldHeight//app.lines
    cy = app.fieldWidth//5
    defender1 = player.Defender(app.margin + cy, app.margin +yard,10, 2)
    defender2 = player.Defender(app.margin + 2*cy, app.margin + 2*yard,10,2)
    defender3 = player.Defender(app.margin + 3*cy, app.margin + 2*yard,10,2)
    defender4 = player.Defender(app.margin + 4*cy, app.margin + 3*yard,10,2)
    defender5 = player.Defender(app.margin + app.fieldWidth//2, 4*yard,10,2)
    return [defender1,defender2,defender3,defender4, defender5]

def level3D(app):
    result = level2D(app)
    yard = app.fieldHeight//app.lines
    cy = app.fieldWidth//5
    new = player.Defender(app.margin + app.fieldWidth//2, 3* yard,10,2)
    result.append(new)
    return result

def level4D(app):
    yard = app.fieldHeight//app.lines
    cy = app.fieldWidth//5
    defender1 = player.SmartDefender(app.margin + cy, app.margin +yard,10, 3)
    defender2 = player.SmartDefender(app.margin + 4*cy, app.margin + 3*yard,10,
        3)
    defender3 = player.SmartDefender(app.margin + app.fieldWidth//2, 4*yard,10, 
        3)
    return [defender1, defender2, defender3]

def level5D(app):
    yard = app.fieldHeight//app.lines
    cy = app.fieldWidth//5
    defender1 = player.SmartDefender(app.margin + cy, app.margin +yard,10, 2)
    defender2 = player.SmartDefender(app.margin + 2*cy, app.margin + 2*yard,10,2)
    defender3 = player.SmartDefender(app.margin + 3*cy, app.margin + 2*yard,10,2)
    defender4 = player.SmartDefender(app.margin + 4*cy, app.margin + 3*yard,10,2)
    defender5 = player.SmartDefender(app.margin + app.fieldWidth//2, 4*yard,10,2)
    return [defender1,defender2,defender3,defender4, defender5]

def level6D(app):
    yard = app.fieldHeight//app.lines
    cy = app.fieldWidth//5
    mid = app.margin + app.fieldWidth//2
    mid2 = app.margin + app.fieldHeight//2
    dif = app.fieldWidth//8
    defender1 = player.FunnelDefender(app.margin + cy, app.margin +yard,10, 2,
        (mid,mid2))
    defender2 = player.FunnelDefender(app.margin + 2*cy, app.margin + 2*yard,10,
        2, (mid + dif,mid2))
    defender3 = player.FunnelDefender(app.margin + 3*cy, app.margin + 2*yard,10,
        2, (mid + 2*dif,mid2))
    defender4 = player.FunnelDefender(app.margin + 4*cy, app.margin + 3*yard,10,
        2, (mid + 3*dif,mid2))
    defender5 = player.SmartDefender(app.margin + app.fieldWidth//2, 4*yard,10,
        2)
    defender6 = player.Defender(app.margin + 10, app.margin + yard,10,2)
    return [defender1,defender2,defender3,defender4, defender5,defender6]



def level1B(app): #creates the blockers 
    yard = app.fieldHeight//app.lines
    cy = app.fieldWidth//5
    blocker1 = player.Blocker(app.margin + 2*cy, yard*10)
    blocker2 = player.Blocker(app.margin + 3*cy, yard*10)
    return [blocker1,blocker2]

