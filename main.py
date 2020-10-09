from game import *
from moves import *
from network import *
import pygame
import torch
import sys

done = False
moves = [EnergyBeam,Slam,Recover,IronDefence,FlyKick]

game = game()

p1 = character("blue.png","red",moves,100,200,200,400)
p2 = character("red.png","blue",moves,50,100,400,200)

game.init_players(p1,p2)
agent1 = torch.load("bots3/bot"+str(sys.argv[1]))[0]
agent2 = torch.load("bots3/bot"+str(sys.argv[2]))[0]
clock = pygame.time.Clock()

while not done:

    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

    winner = game.take_action(agent1.forward(game.get_state_p1()),agent2.forward(game.get_state_p2()))

    print("red:",game.p1.hp," blue:",game.p2.hp)

    comment("----------------------------")

    if winner != 0:

        game.reset()
        print("***************************")
        print("player ",winner," won")
        print("***************************")

    game.render()
    clock.tick(1)

