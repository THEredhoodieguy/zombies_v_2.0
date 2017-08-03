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
        self.nearest_zombie = None

    def get_dist(self, zombie):
        return math.sqrt((zombie.x - self.x)**2 + (zombie.y - self.y)**2)

    def move(self, xbound, ybound):
        """movement presently works as though humans and zombies are on a sphere"""
        (xvel, yvel) = get_velocity(self.speed, self.direction)
        new_x = self.x + xvel
        new_y = self.y + yvel
        if(new_x < 0): new_x = xbound + new_x
        if(new_x > xbound): new_x = new_x - xbound
        if(new_y < 0): new_y = ybound + new_y
        if(new_y > ybound): new_y = new_y - ybound
        self.x = new_x
        self.y = new_y

    def set_direction(self):
        if self.closest_zombie == None:
            self.direction = math.random() * math.pi * 2
        else:
            self.direction = -1*math.atan2(self.closest_zombie.y - self.y, self.closest_zombie.x - self.x)





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
        self.nearest_human = None
        self.eat_dist = 3

    def get_dist(self, human):
        return math.sqrt((human.x - self.x)**2 + (human.y - self.y)**2)

    def move(self, xbound, ybound):
        (xvel, yvel) = get_velocity(self.speed, self.direction)
        new_x = self.x + xvel
        new_y = self.y + yvel
        if(new_x < 0): new_x = xbound + new_x
        if(new_x > xbound): new_x = new_x - xbound
        if(new_y < 0): new_y = ybound + new_y
        if(new_y > ybound): new_y = new_y - ybound
        self.x = new_x
        self.y = new_y

    def set_direction(self):
        if self.closest_human == None:
            self.direction = math.random() * math.pi * 2
        else:
            self.direction = math.atan2(self.closest_human.y - self.y, self.closest_human.x - self.x)

    def eat(self):
        return Zombie(self.x, self.y)




class Simulator(object):
    """
    The Simulator holds references to all humans and zombies
    """

    def __init__(self, num_humans, num_zombies, x_bound, y_bound, num_blocks):
        self.humans = [Human(random.randint(0,x_bound), random.randint(0,y_bound)) for h in range(num_humans)]
        self.zombies = [Zombie(random.randint(0,x_bound), random.randint(0,y_bound)) for z in range(num_zombies)]
        self.num_blocks = num_blocks
        self.block_unit_x = x_bound / num_blocks
        self.block_unit_y = y_bound / num_blocks 
        #the following lists are used to put humans and zombies into the simulator at the end of turns
        self.new_humans = list()
        self.new_zombies = list()

    def closest_zombie(self, human):
        #Check to make sure there are zombies at all
        if(len(self.zombies) > 0):
            min_dist = math.inf
            min_zombie = None
            #if there are zombies in the same block as the human
            if len(self.zombie_blocks[human.x//self.block_unit_x][human.y//self.block_unit_y]) != 0:
                for zombie in self.zombie_blocks[human.x//self.block_unit_x][human.y//self.block_unit_y]:
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
            if len(self.human_blocks[zombie.x//self.block_unit_x][zombie.y//self.block_unit_y]) != 0:
                for human in self.human_blocks[zombie.x//self.block_unit_x][zombie.y//self.block_unit_y]:
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


    def update(self):
        self.human_blocks = [[list() for j in range(self.num_blocks)] for i in range(self.num_blocks)]
        self.zombie_blocks = [[list() for j in range(self.num_blocks)] for i in range(self.num_blocks)]

        for h in self.humans:
            human_blocks[h.x//self.block_unit_x][h.y//self.block_unit_y].append(h)
        for z in self.zombies:
            zombie_blocks[z.x//self.block_unit_x][z.y//self.block_unit_y].append(z)

        #initializing a pool of resources to multithread the process of finding the closest human/zombie
        pool = mp.Pool(resources=100)

        for i in self.human_blocks:
            for j in i:
                for human in j:
                    pool.apply(self.closest_zombie, args=(human))

        for i in self.zombie_blocks:
            for j in i:
                for zombie in j:
                    pool.apply(self.closest_human, args=(zombie))

        self.humans.shuffle()
        self.zombies.shuffle()
        for h in self.humans:
            h.move()
        for z in self.zombies:
            z.move()

        #have zombies eat humans near to them
        for z in self.zombies:
            if z.get_dist(z.closest_human) < z.eat_dist:
                if(z.closest_human in self.humans):
                    self.new_zombies.append(z.eat())
                    self.humans.remove(z.closest_human)

        for z in self.new_zombies:
            self.zombies.append(z)