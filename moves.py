import random

PrintComments = True
stat_enable = False

#total times moves used
energybeam = 0
slam = 0
recover = 0
irondefence = 0
flykick = 0

def clear_stats():
    global energybeam, slam, recover, irondefence, flykick
    energybeam = 0
    slam = 0
    recover = 0
    irondefence = 0
    flykick = 0

def enable_stats():
    global stat_enable
    stat_enable = True

def disable_stats():
    global stat_enable
    stat_enable = False

def get_moves_stats():
    return [energybeam,slam,recover,irondefence,flykick]

def comment(s):
    global PrintComments
    
    if(PrintComments):
        print(s)

def EnergyBeam(state,player1,player2):

    if stat_enable:
        global energybeam
        energybeam = energybeam + 1

    comment(player1.name +" used energy beam")
    
    player1.attack -= 0.1 * player2.attack
    player1.defence -= 0.1 * player1.defence
    player2.accuracy -= 0.1 * player2.accuracy

    accur = random.randint(0,100)

    if player1.accuracy > accur:
        player2.hp -= (player1.attack * 0.4)

        if player1.hp < 0.2 * player1.maxhp:
            player2.hp -= (player1.attack * 0.2)

        comment(player1.name + "'s energy beam hit " + player2.name)
    else:
        comment("energy beam missed")
    
    return (state,player1,player2)

def Slam(state,player1,player2):

    if stat_enable:
        global slam
        slam = slam + 1

    comment(player1.name +" used slam")

    player1.hp -= ((player1.attack*0.5) / player1.defence) * 10
    player2.hp -= ((player1.attack*2.2) / player2.defence) * 10
    player1.agility -= 25

    return(state,player1,player2)

def Recover(state,player1,player2):

    if stat_enable:
        global recover
        recover = recover + 1

    comment(player1.name +" used Recover")
    player1.hp += 30
    player1.defence -= 10

    if(player1.hp > player1.maxhp):
        player1.hp = player1.maxhp

    return (state,player1,player2)

def IronDefence(state,player1,player2):

    if stat_enable:
        global irondefence
        irondefence = irondefence + 1

    comment(player1.name +" used Iron Defence")
    
    player1.defence += 25
    player2.accuracy -= 10
    player1.attack -= 5 if player1.attack > 25 else 0

    return (state,player1,player2)

def FlyKick(state,player1,player2):

    if stat_enable:
        global flykick
        flykick = flykick + 1

    comment(player1.name +" is preparing to kick ")

    accur = random.randint(0,100)

    if player1.accuracy > accur:
        player1.agility += 15
        player2.hp -= ((player1.attack*4) / player2.defence) * 10
        comment(player1.name + " used fly kick")
    else:
        player1.hp -= 25 * (player1.agility/player1.defence)
        player1.defence -= 20
        comment(player1.name + " missed "+ player2.name)

    return (state,player1,player2)