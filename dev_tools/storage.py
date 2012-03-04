#!/usr/bin/env python
from ants import *
import random
import cProfile
import copy
import a_star, util
from util import l

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
      ###Updates hill attack locations
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
      ###Calibrates ant lookup and resets value to None
      a = ants.my_ants()
      dead = []
      for ant in self.ant_lookup:
	if ant not in a:
	  dead.append(ant)
      for ant in dead:
	self.dead_ants += 1
	del self.ant_lookup[ant]
      ###Resets all ant guides to None
      for ant in a:
	self.ant_lookup[ant] = None
      ###Sets class variables
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

    def rank_ants_proximity(self, guide, D_distance=0):
      "Returns sorted list of ants with smallest surrounding numbers first"
      rankings = {}
      array = copy.deepcopy(guide)
      for ant in self.ant_lookup:
	if self.ant_lookup[ant] == None:
	  rankings[ant] = a_star.ant_distance(ant, array, D_distance)
      return sorted(rankings, key=rankings.__getitem__)

    def num_ants_without_assignment(self):
      "Determines number ants that do not have guide"
      count = 0
      for a in self.ant_lookup:
	if self.ant_lookup[a] == None:
	  count += 1
      return count

    def get_outskirts(self, ants):
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

    def assign_food(self, ants):
      "Assign all food locations as destination"
      if len(self.food) > 0:
	array = copy.deepcopy(self.level_array)
	food_guide = a_star.place_all_numbers(self.food, array)
	rankings = self.rank_ants_proximity(food_guide)
	ant_number = len(self.food)
	a = []
	for ant in rankings:
	  if self.ant_lookup[ant] == None:
	    self.ant_lookup[ant] = food_guide
	    a.append(ant)
	  if len(a) >= ant_number:
	    break
	#l.log("Food Ants: ", str(len(a)) + ' ' + str(a))
	#l.log("Food Guide: \n", util.array_to_string(food_guide))
      
    def assign_defense(self, ants):
      "Assign wall around ant hill"
      array = copy.deepcopy(self.level_array)
      defense_guide, destination_count = a_star.defense_guide(3, ants.my_hills(), array)
      rankings = self.rank_ants_proximity(defense_guide, 10)
      ant_number = min(destination_count, len(self.ant_lookup) / 3)
      a = []
      for ant in rankings:
	if self.ant_lookup[ant] == None:
	  self.ant_lookup[ant] = defense_guide
	  a.append(ant)
	if len(a) >= ant_number:
	  break
      #l.log("Defense Ants: ", str(len(a)) + ' ' + str(a))
      #l.log("Desfense Guide: \n", util.array_to_string(defense_guide))
      
    def assign_hills(self, ants):
      "Assign enemy hills to attack Enemy Hills"
      if len(self.enemy_hills) > 0: 
	array = copy.deepcopy(self.level_array)
	attack_guide = a_star.place_all_numbers(self.enemy_hills, array)
	rankings = self.rank_ants_proximity(attack_guide)
	ant_number = self.num_ants_without_assignment() / 2
	a = []
	for ant in rankings:
	  if self.ant_lookup[ant] == None:
	    self.ant_lookup[ant] = attack_guide
	    a.append(ant)
	  if len(a) >= ant_number:
	    break
	#l.log("Hill Ants: ", str(len(a)) + ' ' + str(a))
	#l.log("Hill Guide: \n", util.array_to_string(attack_guide))

    def assign_outskirts(self, ants):
      "Assign all regions that have not been seen as destination"
      array = copy.deepcopy(self.level_array)	
      outskirts = self.get_outskirts(ants)
      outskirt_guide = a_star.place_all_numbers(outskirts, array)
      a = []
      for ant in self.ant_lookup:
	if self.ant_lookup[ant] == None:
	  self.ant_lookup[ant] = outskirt_guide
	  a.append(ant)
      #l.log("Outskirt Ants: ", str(len(a)) + ' ' + str(a))
      #l.log("Outskirt Guide: \n", util.array_to_string(outskirt_guide))
  
    def assign_orders(self, ants):
      "Ranks the assignment functions in order of importance"
      self.assign_food(ants)
      #self.assign_defense(ants)
      self.assign_hills(ants)
      self.assign_outskirts(ants)
        
    def do_turn(self, ants):
      "Use each ants guide map to determine direction to give to server"
      self.turn += 1
      l.log("Turn: ", self.turn)
      l.log("# Ants: ", len(self.ant_lookup))
      l.log("Mao: ", ants.render_text_map())
      self.update_level(ants)
      self.update(ants)
      self.assign_orders(ants)
      destinations = []
      for ant in ants.my_ants():
	if self.ant_lookup[ant] != None:
	  direction = self.smart_move(ants, ant, self.ant_lookup[ant])
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
