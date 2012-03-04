#!/usr/bin/env python
from ants import *
import random
import cProfile
import copy
import a_star, util

#class log:
    #def __init__(self):
      #self.log_on = True
      #self.f = open('/home/david/ants/log.txt', 'w')
    #def log(self, tag, message):
      #if self.log_on:
	#string = tag + str(message) + '\n'
	#self.f.write(string)
	#self.f.flush()
#l = log()

# define a class with a do_turn method
# the Ants.run method will parse and update bot input
# it will also run the do_turn method for us
class MyBot:
    def __init__(self):
        # define class level variables, will be remembered between turns
	self.turn = 0
	self.ant_lookup = {}
	self.level_string = ''
	self.level_array = []
	self.level_size = ()
	self.food = []
	self.outskirts = []
	self.enemy_hills = []
	self.total_ants = -1
	self.dead_ants = 0
	self.current_ants = -1
	self.map_ants = -1
	self.hive_ants = -1

    # do_setup is run once at the start of the game
    # after the bot has received the game settings
    # the ants class is created and setup by the Ants.run method
    def do_setup(self, ants):
      self.level_string = util.strip_string(ants.render_text_map())
      self.level_array = util.string_to_array(self.level_string)
      self.level_size = (ants.cols, ants.rows)
      for y in range(0, self.level_size[1]):
	row = []
	for x in range(0, self.level_size[0]):
	  row.append(False)
	self.outskirts.append(row)
        # initialize data structures after learning the game settings

    def update_level(self, ants):
      "Updates class variables for string and array levels"
      new_s = util.strip_string(ants.render_text_map())
      s = ''
      pos = 0
      for char in self.level_string:
	if char != '%':
	  s = s + new_s[pos]
	else: s = s + '%'
	pos += 1
      self.level_string = s
      self.level_array = util.string_to_array(self.level_string)

    def update(self, ants):
      "Updates class variables"
      ###Initializes class variables
      if self.total_ants == -1:
	self.total_ants = len(ants.my_ants())
      ###Updates Food
      new_food = ants.food()
      for f in self.food:
	if f not in new_food and ants.visible(f) and 'a' in a_star.surroundings(f, self.level_array):
	  self.total_ants += 1
      self.food = ants.food()
      ###Calibrates ant lookup and resets value to None
      a = ants.my_ants()
      dead = []
      for ant in self.ant_lookup:
	if ant not in a:
	  dead.append(ant)
      for ant in dead:
	self.dead_ants += 1
	del self.ant_lookup[ant]
      for ant in a:
	self.ant_lookup[ant] = None
      self.current_ants = self.total_ants - self.dead_ants
      self.map_ants = len(self.ant_lookup)
      self.hive_ants = self.current_ants - self.map_ants
	
    def smart_move(self, ants, loc, level):
      "Returns direction based on a* generated guide, checks four directions for occupation"
      directions = a_star.move_direction(loc, level)
      if directions != None:
	for d in directions:
	  dest = ants.destination(loc, d)
	  if ants.unoccupied(dest):
	    return d
      return None	

    def rank_ants_proximity(self, guide):
      "Returns sorted list of ants with smallest surrounding numbers first"
      rankings = {}
      array = copy.deepcopy(guide)
      for ant in self.ant_lookup:
	if self.ant_lookup[ant] == None:
	  rankings[ant] = a_star.ant_distance(ant, array)
      return sorted(rankings, key=rankings.__getitem__)

    def num_ants_without_assignment(self):
      "Determines number ants that do not have guide"
      count = 0
      for a in self.ant_lookup:
	if self.ant_lookup[a] == None:
	  count += 1
      return count

    def set_outskirts(self, ants):
      "Manipulates outskirts list"
      o = []
      for y in range(0, self.level_size[1]):
	for x in range(0, self.level_size[0]):
	  point = (y, x)
	  if ants.visible(point):
	    self.outskirts[y][x] = True
	  if not self.outskirts[y][x]:
	    o.append((y, x))
      return o
	      
    def set_hills(self, ants):
      "Determines hills to be attacked"
      hills = ants.enemy_hills_locs()
      for h in hills:
	if h not in self.enemy_hills:
	  self.enemy_hills.append(h)
      razed = []
      for h in self.enemy_hills:
	if ants.visible(h) and h not in hills:
	  razed.append(h)
      for h in razed:
	self.enemy_hills.remove(h)

    def get_defense_region(self, ants):
      array = copy.deepcopy(self.level_array)
      points = []
      for hill in ants.my_hills():
	for p in a_star.defensive_destinations(hill, array):
	  points.append(p)
      return points

    def assign_food(self, ants):
      array = copy.deepcopy(self.level_array)
      food_guide = a_star.place_all_numbers(self.food, array)
      rankings = self.rank_ants_proximity(food_guide)
      closest = rankings[0 : len(self.food)]
      a = []
      for ant in closest:
	if self.ant_lookup[ant] == None:
	  self.ant_lookup[ant] = [food_guide]
	  a.append(ant)
      #l.log("Food Ants: ", a)
      #l.log("Food Guide: ", util.array_to_string(food_guide))
      
    def assign_defense(self, ants):
      array = copy.deepcopy(self.level_array)
      regions = self.get_defense_region(ants)	
      for hill in ants.my_hills():
	y, x = hill
	array[y][x] = -1
      defense_guide = a_star.place_all_numbers(regions, array)
      rankings = self.rank_ants_proximity(defense_guide)
      closest = rankings[0 : len(regions)]
      a = []
      for ant in closest:
	if self.ant_lookup[ant] == None:
	  self.ant_lookup[ant] = [defense_guide]
	  a.append(ant)
      
    def assign_hills(self, ants):
      self.set_hills(ants)
      if len(self.enemy_hills) > 0: 
	array = copy.deepcopy(self.level_array)
	attack_guide = a_star.place_all_numbers(self.enemy_hills, array)
	rankings = self.rank_ants_proximity(attack_guide)
	closest = rankings[0 : self.num_ants_without_assignment() / 2]
	a = []
	for ant in closest:
	  if self.ant_lookup[ant] == None:
	    self.ant_lookup[ant] = [attack_guide]
	    a.append(ant)
	#l.log("Hill Ants: ", a)
	#l.log("Hill Guide: ", util.array_to_string(attack_guide))
	

    def assign_attack(self, ants):
      array = copy.deepcopy(self.level_array)
      enemies = ants.enemy_ants_locs()
      attack_guide = a_star.place_all_numbers(enemies, array)
      rankings = self.rank_ants_proximity(attack_guide)
      closest = rankings[0 : 2]
      a = []
      for ant in closest:
	if self.ant_lookup[ant] == None:
	  self.ant_lookup[ant] = [attack_guide]
	  a.append(ant)

    def assign_outskirts(self, ants):
      array = copy.deepcopy(self.level_array)	
      outskirts = self.set_outskirts(ants)
      #l.log("Outskirts: ", outskirts)
      outskirt_guide = a_star.place_all_numbers(outskirts, array)
      a = []
      for ant in self.ant_lookup:
	if self.ant_lookup[ant] == None:
	  self.ant_lookup[ant] = [outskirt_guide]
	  a.append(ant)
      #l.log("Outskirt Ants: ", a)
      #l.log("Outskirt Guide: ", util.array_to_string(outskirt_guide))
  
    def assign_orders(self, ants):
      self.assign_food(ants)
      #self.assign_defense(ants)
      self.assign_hills(ants)
      #self.assign_attack(ants)
      self.assign_outskirts(ants)
        
    def do_turn(self, ants):
      self.turn += 1
      #l.log("Turn: ", self.turn)
      #l.log("Turn Time: ", ants.turntime)
      self.update_level(ants)
      self.update(ants)
      self.assign_orders(ants)
      destinations = []
      for ant in ants.my_ants():
	if self.ant_lookup[ant] != None:
	  direction = self.smart_move(ants, ant, self.ant_lookup[ant][0])
	else: direction = None
	if direction != None:
	  dest = ants.destination(ant, direction)
	  if dest not in destinations:
	    ants.issue_order((ant, direction))
	    del self.ant_lookup[ant]
	    self.ant_lookup[dest] = None
	  destinations.append(dest)
	if ants.time_remaining() < 10:
	  break

def run_my_bot(source):
  Ants.run(source, MyBot())
    
if __name__ == '__main__':
    # psyco will speed up python a little, but is not needed
    try:
        import psyco
        psyco.full()
    except ImportError:
        pass
    
    try:
        # if run is passed a class with a do_turn method, it will do the work
        # this is not needed, in which case you will need to write your own
        # parsing function and your own game state class
        run_my_bot(sys.stdin)
    except KeyboardInterrupt:
        print('ctrl-c, leaving ...')
