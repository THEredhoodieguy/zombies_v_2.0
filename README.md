# zombies_v_2.0
Second-Generation Zombie Sim


The first time around, I tried to implement a humans vs zombie simulator, it was really cool, but it ran horribly. Significant performance bottlenecks would arise from any simulation with more than 300 or so humans to start. And really, that's when the simulator is most fun to watch.

This time around, I'm going to try to partition the space that the humans and zombies occupy and multithread their detection behavior.