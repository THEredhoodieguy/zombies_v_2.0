#!usr/bin/env python3

#tests for agents.py

from agents import *

if __name__ == "__main__":
    h = Human(1,1)
    z = Zombie(1,3)

    h.closest_zombie = z

    old_dist = h.get_dist(z)

    h.set_direction()
    h.move(500,500)

    new_dist = h.get_dist(z)

    assert new_dist > old_dist, "Human not running away from Zombie"

    h = Human(1,1)
    z = Zombie(1,3)

    z.closest_human = h

    old_dist = z.get_dist(h)

    z.set_direction()
    z.move(500,500)

    new_dist = z.get_dist(h)
    assert new_dist < old_dist, "Zombie not chasing Human"

