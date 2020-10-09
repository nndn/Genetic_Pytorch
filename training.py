from game import *
from moves import *
from network import *
import pygame
import pandas 
import matplotlib.pyplot as plt

def fight(game ,agent1, agent2):
    done = False

    while not done:
        winner = game.take_action(agent1.forward(game.get_state_p1()),agent2.forward(game.get_state_p2()))

        if winner != 0:
            done = True
            game.reset()

            if winner == 1:
                return agent1
            
            if winner == 2:
                return agent2

            return agent1

def fightHalf(agents):

    global game

    n = len(agents)
    m = int(n/2)

    if n == 1:
        return agents[0]

    for i in range(m):
        agents[i] = fight(game,agents[i],agents[m+i])

    return agents[:m]


moves = [EnergyBeam,Slam,Recover,IronDefence,FlyKick]

energybeam_ = []
slam_ = []
recover_ = []
irondefence_ = []
flykick_ = []

game = game()
game.init_pygame()

p1 = character("red.png","red",moves)
p2 = character("red.png","blue",moves)

game.init_players(p1,p2)
num_episodes = 100

#for episode in range(num_episodes):

agents = []
top16 = []
top128 = []


for i in range(1024):
    agents.append(network())

done = False
for episode in range(num_episodes):

    if done == True:
        break

    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

    agents = fightHalf(agents)
    agents = fightHalf(agents)
    agents = fightHalf(agents)

    top128 = agents.copy()

    agents = fightHalf(agents)
    agents = fightHalf(agents)
    agents = fightHalf(agents)

    top16 = agents.copy()

    enable_stats()
    agents = fightHalf(agents)
    agents = fightHalf(agents)
    agents = fightHalf(agents)
    winner = fightHalf(agents)   
    disable_stats()

    agents = []

    for i in range(256):
        agents.append(network()) #256

    agents = agents + top128 #128

    for agent in top16: #16*8 = 128
        agents.append(mutate(agent,0.01))
        agents.append(mutate(agent,0.02))
        agents.append(mutate(agent,0.03))
        agents.append(mutate(agent,0.03))
        agents.append(mutate(agent,0.04))
        agents.append(mutate(agent,0.05))
        agents.append(mutate(agent,0.06))
        agents.append(mutate(agent,0.10))

    for a in top16: #256
        for b in top16:
            agents.append(breed(a,b))

    for i in range(256):
        agents.append(network())


    print("episode:",episode)

    T.save(winner,"bots7/bot"+str(episode))

    [e_,s_,r_,i_,f_] = get_moves_stats()
    energybeam_.append(e_)
    slam_.append(s_)
    recover_.append(r_)
    irondefence_.append(i_)
    flykick_.append(f_)
    clear_stats()

dict_ = {'energy beam':energybeam_, 'slam':slam_, 'recover':recover_, 'iron defence':irondefence_, 'flykick':flykick_}

df = pandas.DataFrame(dict_)

df.to_csv("graphs/moves6.csv")
df.plot()
plt.show()
