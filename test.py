from network import *
from moves import *
from game import *

'''
net = network()
print(net.state_dict())

print("-----------------------------------------------------")
net2 = network()
print(net2.state_dict())

print("-----------------------------------------------------")
net3 = breed(net,net2)
print(net3.state_dict())
'''

game = game()
game.init_pygame()

c1 = character("red.png","sad",[])
c2 = character("red.png","sadi",[])
state = None



