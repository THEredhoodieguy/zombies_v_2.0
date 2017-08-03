#class definitions for our agents

import random, math
import multiprocessing as mp

def get_velocity(speed, direction):
    """Takes a speed and direction and returns change in x and y coords"""
    x = math.cos(direction) * speed
    y = math.sin(direction) * speed
    return (x, y)




class Human(object):
    """
    Humans are the basic unit of the simulation.
    They run from the nearest zombie 
    """

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 1.0
        self.direction = 0
        self.closest_zombie = None

    def get_dist(self, zombie):
        return math.sqrt((zombie.x - self.x)**2 + (zombie.y - self.y)**2)

    def move(self, xbound, ybound):
        """"""
        (xvel, yvel) = get_velocity(self.speed, self.direction)
        new_x = self.x + xvel
        new_y = self.y + yvel

        if(self.x + xvel > xbound or self.x + xvel < 0):
            new_x = self.x - xvel
        if(self.y + yvel > ybound or self.y + yvel < 0):
            new_y = self.y - yvel

        self.x = new_x
        self.y = new_y

    def set_direction(self):
        if (self.closest_zombie != None):
            self.direction = -1*math.atan2(self.closest_zombie.y - self.y, self.closest_zombie.x - self.x)
            # print("Has closest zombie")
            # print("Direction: " + str(self.direction))
        else:
            self.direction = random.random() * math.pi * 2





class Zombie(object):
    """
    Zombies are the predator in the simulation.
    They chase and eat humans, and make new zombies when they eat
    """

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 1.2
        self.direction = 0
        self.closest_human = None
        self.eat_dist = 3

    def get_dist(self, human):
        return math.sqrt((human.x - self.x)**2 + (human.y - self.y)**2)

    def move(self, xbound, ybound):
        (xvel, yvel) = get_velocity(self.speed, self.direction)
        new_x = self.x + xvel
        new_y = self.y + yvel
        if(self.x + xvel > xbound or self.x + xvel < 0):
            new_x = self.x - xvel
        if(self.y + yvel > ybound or self.y + yvel < 0):
            new_y = self.y - yvel
        self.x = new_x
        self.y = new_y

    def set_direction(self):
        if(self.closest_human != None):
            self.direction = math.atan2(self.closest_human.y - self.y, self.closest_human.x - self.x)
        else:
            self.direction = random.random() * math.pi * 2

    def eat(self):
        return Zombie(self.x, self.y)





class Simulator(object):
    """
    The Simulator holds references to all humans and zombies
    """

    def __init__(self, num_humans, num_zombies, xbound, ybound, num_blocks):
        self.humans = [Human(random.randint(0,xbound), random.randint(0,ybound)) for h in range(num_humans)]
        self.zombies = [Zombie(random.randint(0,xbound), random.randint(0,ybound)) for z in range(num_zombies)]
        self.num_blocks = num_blocks
        self.block_unit_x = xbound / num_blocks
        self.block_unit_y = ybound / num_blocks
        self.xbound = xbound
        self.ybound = ybound
        #the following lists are used to put humans and zombies into the simulator at the end of turns
        self.new_humans = list()
        self.new_zombies = list()
        self.pool = mp.Pool(processes=4)

    def closest_zombie(self, human):
        #Check to make sure there are zombies at all
        if(len(self.zombies) > 0):
            min_dist = math.inf
            min_zombie = None
            #if there are zombies in the same block as the human
            if len(self.zombie_blocks[int(human.x//self.block_unit_x) - 1][int(human.y//self.block_unit_y) - 1]) != 0:
                for zombie in self.zombie_blocks[int(human.x//self.block_unit_x) - 1][int(human.y//self.block_unit_y) - 1]:
                    if human.get_dist(zombie) < min_dist:
                        min_dist = human.get_dist(zombie)
                        min_zombie = zombie
                human.closest_zombie = min_zombie
            #else check the whole array of zombies
            elif(len(self.zombies) > 0):
                for zombie in self.zombies:
                    if human.get_dist(zombie) < min_dist:
                        min_dist = human.get_dist(zombie)
                        min_zombie = zombie
        #else assign the human no zombie
        else:
            human.closest_zombie = None

    def closest_human(self, zombie):
        if(len(self.humans) > 0):
            min_dist = math.inf
            min_human = None
            if len(self.human_blocks[int(zombie.x//self.block_unit_x) - 1][int(zombie.y//self.block_unit_y) - 1]) != 0:
                for human in self.human_blocks[int(zombie.x//self.block_unit_x) - 1][int(zombie.y//self.block_unit_y) - 1]:
                    if zombie.get_dist(human) < min_dist:
                        min_dist = zombie.get_dist(human)
                        min_human = human
                zombie.closest_human = min_human
            elif(len(self.humans) > 0):
                for human in self.humans:
                    if zombie.get_dist(human) < min_dist:
                        min_dist = zombie.get_dist(human)
                        min_human = human
        else:
            zombie.closest_human = None

    def get_humans(self):
        return self.humans

    def get_zombies(self):
        return self.zombies

    def update(self):
        self.human_blocks = [[list() for j in range(self.num_blocks)] for i in range(self.num_blocks)]
        self.zombie_blocks = [[list() for j in range(self.num_blocks)] for i in range(self.num_blocks)]

        for h in self.humans:
            self.human_blocks[int(h.x//self.block_unit_x) - 1][int(h.y//self.block_unit_y) - 1].append(h)
        for z in self.zombies:
            self.zombie_blocks[int(z.x//self.block_unit_x) - 1][int(z.y//self.block_unit_y) - 1].append(z)

        #initializing a pool of resources to multithread the process of finding the closest human/zombie

        for i in self.human_blocks:
            for j in i:
                for human in j:
                    self.pool.apply_async(self.closest_zombie, args=(human))
                    # self.closest_zombie(human)

        for i in self.zombie_blocks:
            for j in i:
                for zombie in j:
                    self.pool.apply_async(self.closest_human, args=(zombie))
                    # self.closest_human(zombie)

        for h in self.humans:
            h.set_direction()
        for z in self.zombies:
            z.set_direction()

        random.shuffle(self.humans)
        random.shuffle(self.zombies)
        for h in self.humans:
            h.move(self.xbound, self.ybound)
        for z in self.zombies:
            z.move(self.xbound, self.ybound)

        #have zombies eat humans near to them
        for z in self.zombies:

            if (z.closest_human != None) and (z.get_dist(z.closest_human) < z.eat_dist):
                if(z.closest_human in self.humans):
                    self.new_zombies.append(z.eat())
                    self.humans.remove(z.closest_human)

        for z in self.new_zombies:
            self.zombies.append(z)