import pygame
import random

def getKeyboardInput():

    key = pygame.key.get_pressed()

    keyup =  key[pygame.K_UP]
    keydown = key[pygame.K_DOWN]
    keyright = key[pygame.K_RIGHT]
    keyleft = key[pygame.K_LEFT]

    return [keyup,keydown,keyright,keyleft]

class obj:
    def __init__(self,image,width = 0,height = 0,x = 0,y = 0):
        self.image = pygame.image.load("assets/"+image).convert_alpha()
        self.x = x
        self.y = y
        self.width = self.image.get_size()[0] / 5
        self.height = self.image.get_size()[1] / 5

        if height != 0 and width != 0:
            self.height = int(height)
            self.width = int(width)

        self.image = pygame.transform.scale(self.image, (int(self.width), int(self.height)))

    def set_width(self,width):
        self.width = width
        self.image = pygame.transform.scale(self.image, (int(self.width), int(self.height)))

class character(obj):

    def __init__(self, image, name, moves,width=0, height=0, x=0, y=0):
        super(character,self).__init__(image, width=width, height=height, x=x, y=y)
        self.x = x
        self.y = y
        self.name = name

        #character stats
        self.maxhp = 100
        self.hp = 100
        self.attack = 100
        self.defence = 100
        self.agility = 100
        self.accuracy = 80

        self.moves = moves

    def reset_stats(self):
        self.maxhp = 100
        self.hp = 100
        self.attack = 100
        self.defence = 100
        self.agility = 100
        self.accuracy = 80

    def use(self, num, state, player2):
        return self.moves[num](state,self,player2)

    def get_hp(self):
        return (self.hp / self.maxhp) * 100

class game:
    def __init__(self):
        self.screen = None
        self.winx = None
        self.winy = None
        self.done = False
        self.winner = 0
        self.game_length = 50
        self.init_pygame()
        self.arena = obj("arena.png",700,400,300,375)
        self.beam = obj("beam.png",270,270,300,300)
        self.nothing = obj("arena.png",1,1,0,0)
        self.anim = self.nothing
        self.clock = pygame.time.Clock()
        self.p1_m = 0
        self.p2_m = 0
        self.fps = 3
        self.background = obj("background.png",600,600,300,300)

        self.healthbar1 = obj("health_bar.png",300,30,20,550)
        self.healthbar2 = obj("health_bar.png",300,30,280,50)
        self.healthbarBackground1 = obj("health_bar_background.png",300,30,20,550) 
        self.healthbarBackground2 = obj("health_bar_background.png",300,30,280,50)
        self.max_health_width = 300 

        #animations
        self.beam_animation1 = [self.beam,obj("beam_1.png",270,270,305,300),obj("beam_1.png",270,270,300,300),obj("beam_1.png",270,270,295,300)]
        self.beam_animation2 = [self.beam,obj("beam_2.png",270,270,305,300),obj("beam_2.png",270,270,300,300),obj("beam_2.png",270,270,295,300)]
        self.recover_animation1 = [obj("recover_1.png",200,200,200,400),obj("recover_2.png",200,200,200,400),obj("recover_3.png",200,200,200,400),obj("recover_4.png",200,200,200,400)]
        self.recover_animation2 = [obj("recover_1.png",100,100,400,200),obj("recover_2.png",100,100,400,200),obj("recover_3.png",100,100,400,200),obj("recover_4.png",100,100,400,200)]
        self.iron_defence_animation1 = [obj("defence_1.png",200,200,200,400),obj("defence_2.png",200,200,200,400),obj("defence_3.png",200,200,200,400),obj("defence_4.png",200,200,200,400),obj("defence_5.png",200,200,200,400)]
        self.iron_defence_animation2 = [obj("defence_1.png",100,100,400,200),obj("defence_2.png",100,100,400,200),obj("defence_3.png",100,100,400,200),obj("defence_4.png",100,100,400,200),obj("defence_5.png",100,100,400,200)]
        self.kick_animation1 = [obj("kick_1.png",100,100,400,200),obj("kick_2.png",100,100,400,200),obj("kick_3.png",100,100,400,200),obj("kick_4.png",100,100,400,200)]
        self.kick_animation2 = [obj("kick_1.png",200,200,200,400),obj("kick_2.png",200,200,200,400),obj("kick_3.png",200,200,200,400),obj("kick_4.png",200,200,200,400)]
        self.slam_animation1 = [obj("slam_1.png",100,100,400,200),obj("slam_2.png",100,100,400,200),obj("slam_3.png",100,100,400,200),obj("slam_4.png",100,100,400,200)]
        self.slam_animation2 = [obj("slam_1.png",200,200,200,400),obj("slam_2.png",200,200,200,400),obj("slam_3.png",200,200,200,400),obj("slam_4.png",200,200,200,400)]

        self.animations1 = [self.beam_animation1,self.slam_animation1,self.recover_animation1,self.iron_defence_animation1,self.kick_animation1]
        self.animations2 = [self.beam_animation2,self.slam_animation2,self.recover_animation2,self.iron_defence_animation2,self.kick_animation2]
        #game states
        self.state = None
        self.time = 0
        self.p1 = None
        self.p2 = None

    def reset(self):
        self.done = False
        self.winner = 0
        self.time = 0
        self.p1.reset_stats()
        self.p2.reset_stats()

        self.healthbar1 = obj("health_bar.png",300,30,20,550)
        self.healthbar2 = obj("health_bar.png",300,30,280,50)


    def get_state_p1(self):
        return [self.p1.hp/self.p1.maxhp*100,self.p2.hp/self.p2.maxhp*100,self.p1.attack,self.p1.defence,self.p1.agility,self.p1.accuracy]

    def get_state_p2(self):
        return [self.p2.hp/self.p2.maxhp*100,self.p1.hp/self.p1.maxhp*100,self.p2.attack,self.p2.defence,self.p2.agility,self.p2.accuracy]

    def init_pygame(self):
        pygame.init()
        self.screen = pygame.display.set_mode((600,600))
        self.winx,self.winy = self.screen.get_size()

    def init_players(self, player1, player2):
        self.p1 = player1
        self.p2 = player2

    def checkWinner(self):
        
        if self.p1.hp <= 0:
            return (True,2)
        elif self.p2.hp <= 0:
            return (True,1)
        else:
            return (False,0)

    def doubleCheck(self):

        if self.p1.attack <= 10:
            self.p1.attack = 10

        if self.p1.defence <= 10:
            self.p1.defence = 10

        if self.p1.accuracy <= 10:
            self.p1.accuracy = 10

        if self.p1.agility <= 10:
            self.p1.agility = 10

        if self.p2.attack <= 10:
            self.p2.attack = 10

        if self.p2.defence <= 10:
            self.p2.defence = 10

        if self.p2.accuracy <= 10:
            self.p2.accuracy = 10

        if self.p2.agility <= 10:
            self.p2.agility = 10


    def take_action(self,p1_move,p2_move):

        self.time += 1
        self.p1_m = p1_move
        self.p2_m = p2_move

        if self.time >= self.game_length:
            
            if self.p1.hp >= self.p2.hp:
                return 1
            else:
                return 2

        if(self.p1.agility * random.randint(0,1) > self.p2.agility * random.randint(0,1)):
            (self.state,self.p1,self.p2) = self.p1.use(p1_move, self.state, self.p2)
            (self.done, self.winner) = self.checkWinner()
            self.doubleCheck()
            
            if self.done:
                return self.winner

            (self.state,self.p2,self.p1) = self.p2.use(p2_move, self.state, self.p1)
            (self.done, self.winner) = self.checkWinner()
            self.doubleCheck()

            if self.done:
                return self.winner

        else:
            (self.state,self.p2,self.p1) = self.p2.use(p2_move, self.state, self.p1)
            (self.done, self.winner) = self.checkWinner()
            self.doubleCheck()
            
            if self.done:
                return self.winner

            (self.state,self.p1,self.p2) = self.p1.use(p1_move, self.state, self.p2)
            (self.done, self.winner) = self.checkWinner()
            self.doubleCheck()
            
            if self.done:
                return self.winner

        return 0

    def animate(self,animations,repeat = 1):

        for i in range(repeat):
            for frame in animations:

                self.display(frame)
                self.clock.tick(self.fps)

        self.anim = self.nothing

    def render(self):
        self.display(self.nothing)
        self.clock.tick(self.fps)
        self.animate(self.animations1[self.p1_m],repeat=1)
        self.animate(self.animations2[self.p2_m],repeat=1)

    def display(self,frame):
        self.clearScreen()
        #display all elements
        self.disp(self.background)
        self.anim = self.beam
        self.disp(self.arena)
        self.disp(self.p2)
        self.disp(frame)
        self.disp(self.p1)

        self.healthbar1.set_width(self.p1.get_hp() * self.max_health_width / 100)
        self.healthbar2.set_width(self.p2.get_hp() * self.max_health_width / 100)

        self.disp2(self.healthbarBackground1)
        self.disp2(self.healthbar1)
        self.disp2(self.healthbarBackground2)
        self.disp2(self.healthbar2)

        pygame.display.update()

    def clearScreen(self):
        self.screen.fill((0,0,0))

    def disp(self,object):
        self.screen.blit(object.image,(object.x-int(object.image.get_size()[0]/2),
								object.y-int(object.image.get_size()[1]/2)))
    
    def disp2(self,object):
        self.screen.blit(object.image,(object.x,object.y))
