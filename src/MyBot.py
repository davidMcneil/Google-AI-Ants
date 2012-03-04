#!/usr/bin/env python
from ants import *
import math
import pathfind, util

# define a class with a do_turn method
# the Ants.run method will parse and update bot input
# it will also run the do_turn method for us
class MyBot:
    def __init__(self):
        # define class level variables, will be remembered between turns
	self.turn = 0
	self.ant_lookup = {}
	self.total_ants = 0
	self.level_string = ''
	self.level_array = []
	self.level_tiles_seen = []
	self.level_size = ()
	self.total_tiles = 0
	self.food = []
	self.my_hills = []
	self.enemy_hills = []
	self.enemy_ants = []
	self.outskirts = []
	self.percentage_unseen = 0
	self.view_radius = None
	self.attack_radius = None
	self.destinations = []

    # do_setup is run once at the start of the game
    # after the bot has received the game settings
    # the ants class is created and setup by the Ants.run method
    def do_setup(self, ants):
      self.level_string = util.strip_string(ants.render_text_map())
      self.level_array = util.string_to_array(self.level_string)
      self.level_size = (ants.cols, ants.rows)
      self.total_tiles = self.level_size[0] * self.level_size[1]
      self.view_radius = math.ceil(ants.viewradius2 ** .5)
      self.attack_radius = math.ceil(ants.attackradius2 ** .5)
      for y in range(0, self.level_size[1]):
	row = []
	for x in range(0, self.level_size[0]):
	  row.append('X')
	self.level_tiles_seen.append(row)

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
      ###Update unseen list and level fog
      self.outskirts = []
      count_unseen = 0
      for y in range(0, self.level_size[1]):
	for x in range(0, self.level_size[0]):
	  point = (y, x)
	  if ants.visible(point):
	    self.level_tiles_seen[y][x] = self.level_array[y][x]
	  if self.level_tiles_seen[y][x] != 'X' and 'X' in pathfind.extended_surroundings(1, point, self.level_tiles_seen):
	    self.outskirts.append((y, x))    
	  if self.level_tiles_seen[y][x] == 'X':
	    count_unseen += 1
      self.percentage_unseen = float(count_unseen) / float(self.total_tiles)
    
    def update(self, ants):
      "Updates class variables"
      ###Updates Food
      self.food = ants.food()
      ###Updates hills
      self.my_hills = ants.my_hills()
      ###Updates enemy ants
      self.enemy_ants = ants.enemy_ants_locs()
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
	del self.ant_lookup[ant]
      ###Resets all ant guides to None
      for ant in a:
	self.ant_lookup[ant] = None
      self.total_ants = len(self.ant_lookup)
      ###Resets destintion points
      self.destinations = []
      
    def num_ants_without_assignment(self):
      "Determines number ants that do not have guide"
      count = 0
      for a in self.ant_lookup:
	if self.ant_lookup[a] == None:
	  count += 1
      return count

    def rank_ants_proximity(self, guide):
      "Returns sorted list of ants with smallest surrounding numbers first"
      rankings = {}
      for ant in self.ant_lookup:
	y, x = ant
	if self.ant_lookup[ant] == None:
	  d = pathfind.ant_distance(ant, guide)
	  if d != None:
	    rankings[ant] = d
      return sorted(rankings, key=rankings.__getitem__)
      
    def away_hill(self, loc, distance):
      'calculate the closest distance between two locations'
      row1, col1 = loc
      for h in self.my_hills:
	row2, col2 = h
	d_col = min(abs(col1 - col2), self.level_size[1] - abs(col1 - col2))
	d_row = min(abs(row1 - row2), self.level_size[0] - abs(row1 - row2))
	if d_row + d_col < distance:
	  return False
      return True

    def rank_distance_from_hill(self, destinations, ants):
      destinations_map = {}
      for d in destinations:
	for h in self.my_hills:
	  distance = ants.distance(d, h)
	  if d not in destinations_map or distance < destinations_map[d]:
	    destinations_map[d] = distance
      return sorted(destinations_map, key=destinations_map.__getitem__)

    def get_all_outposts(self, distance, level, ants):
      destinations = []
      for y in range(0, self.level_size[1]):
	for x in range(0, self.level_size[0]):
	  if y % distance == 0 and x % distance == 0:
	    if level[y][x] != '%' and self.level_tiles_seen[y][x] != 'X' and self.away_hill((y, x), distance) :
	      destinations.append((y, x))
      return self.rank_distance_from_hill(destinations, ants)

      
    def assign_food(self, ants):
      "Assign all food locations as destination"
      #l.log_on = True
      a = []
      if len(self.food) > 0:
	food_guide, run_status = pathfind.create_guide(self.food, self.level_tiles_seen, ants, depth=self.view_radius + 5)
	if run_status == "stop":
	  return ["stop"]
	rankings = self.rank_ants_proximity(food_guide)
	ant_num = len(self.food)
	for ant in rankings:
	  if self.ant_lookup[ant] == None:
	    self.ant_lookup[ant] = food_guide
	    a.append(ant)
	  if len(a) >= ant_num:
	    #l.log("Food Ants: ", str(len(a)) + ' ' + str(a))
	    #l.log("Food Guide: \n", util.array_to_string(food_guide, True))
	    return a
	#l.log("Food Ants: ", str(len(a)) + ' ' + str(a))
	#l.log("Food Guide: \n", util.array_to_string(food_guide, True))
      return a

    def assign_defense(self, ants):
      #"Assign defensive perimeter based on attack radius"
      #l.log_on = True
      a = []
      num_hills = max(len(self.my_hills), 1)
      ant_hill_ratio = self.total_ants / num_hills
      defense_guide, num_dest, run_status = pathfind.create_defensive_guide(self.attack_radius - 1, self.my_hills ,self.level_tiles_seen, ants)
      if run_status == "stop":
	  return ["stop"]
      if ant_hill_ratio >=4 and ant_hill_ratio <= 7:
	ant_num = 1 * num_hills
      elif ant_hill_ratio > 7:
	ant_num = min(self.total_ants / 7, num_dest) * num_hills
      else: ant_num = 0
      if ant_num > 0:
	rankings = self.rank_ants_proximity(defense_guide)
	#l.log("Rankings: ", rankings)
	for ant in rankings:
	  if self.ant_lookup[ant] == None:
	    self.ant_lookup[ant] = defense_guide
	    a.append(ant)
	  if len(a) >= ant_num:
	    #l.log("Defense Ants: ", str(len(a)) + ' ' + str(a))
	    #l.log("Defense Guide: \n", util.array_to_string(defense_guide, True)) 
	    return a
	#l.log("Defense Ants: ", str(len(a)) + ' ' + str(a))
	#l.log("Defense Guide: \n", util.array_to_string(defense_guide, True)) 
      return a 

    def assign_hills(self, ants):
      "Assign all regions that have not been seen as destination"
      #l.log_on = True
      a = []
      if len(self.enemy_hills) > 0:
	hills_guide, run_status = pathfind.create_guide(self.enemy_hills, self.level_tiles_seen, ants)
	if run_status == "stop":
	  return ["stop"]
	rankings = self.rank_ants_proximity(hills_guide)
	ant_num = self.total_ants / 2
	for ant in rankings:
	  if self.ant_lookup[ant] == None:
	    self.ant_lookup[ant] = hills_guide
	    a.append(ant)
	  if len(a) >= ant_num:
	    #l.log("Hill Ants: ", str(len(a)) + ' ' + str(a))
	    #l.log("Hill Guide: \n", util.array_to_string(hills_guide, True))
	    return a
	#l.log("Hill Ants: ", str(len(a)) + ' ' + str(a))
	#l.log("Hill Guide: \n", util.array_to_string(hills_guide, True))
      return a

    def assign_unseen(self, ants):
      "Assign all regions that have not been seen as destination"
      #l.log_on = True
      a = []
      num_ants_no_guide = self.num_ants_without_assignment()
      if num_ants_no_guide > 0 and self.outskirts > 0:
	unseen_guide, run_status = pathfind.create_guide(self.outskirts, self.level_tiles_seen, ants)
	if run_status == "stop":
	  return ["stop"]
	ant_num = int(num_ants_no_guide * min(self.percentage_unseen + .3, 1))
	rankings = self.rank_ants_proximity(unseen_guide)
	for ant in rankings:
	  if self.ant_lookup[ant] == None:
	    self.ant_lookup[ant] = unseen_guide
	    a.append(ant)
	  if len(a) >= ant_num:
	    #l.log("Unseen Ants: ", str(len(a)) + ' ' + str(a))
	    #l.log("Unseen Guide: \n", util.array_to_string(unseen_guide, True))
	    return a
	#l.log("Unseen Ants: ", str(len(a)) + ' ' + str(a))
	#l.log("Unseen Guide: \n", util.array_to_string(unseen_guide, True))
      return a

    def assign_enemy(self, ants):
      "Assign enemy ants as location"
      #l.log_on = True
      a = []
      if len(self.enemy_ants) > 0 and self.num_ants_without_assignment() > 0:
	guide, run_status = pathfind.create_guide(self.enemy_ants, self.level_array, ants, depth=self.view_radius)
	#l.log("Enemy: ", run_status)
	if run_status == "stop":
	  return ["stop"]
	rankings = self.rank_ants_proximity(guide)
	for ant in rankings:
	  if self.ant_lookup[ant] == None:
	    self.ant_lookup[ant] = guide
	    a.append(ant)
	#l.log("Attack Ants: ", str(len(a)) + ' ' + str(a))
	#l.log("Attack Guide: \n", util.array_to_string(guide, True))
      return a

    def assign_outposts(self, ants):
      "Places grid on map and sets points as destinations"
      #l.log_on = True
      a = []
      ant_num = self.num_ants_without_assignment()
      if ant_num > 0:
	destinations = self.get_all_outposts(int(self.view_radius - 1), self.level_tiles_seen, ants)[0:ant_num]
	outpost_guide, run_status = pathfind.create_guide(destinations, self.level_array, ants)
	#l.log("Out: ", run_status)
	if run_status == "stop":
	  return ["stop"]
	rankings = self.rank_ants_proximity(outpost_guide)
	for ant in rankings:
	  if self.ant_lookup[ant] == None:
	    self.ant_lookup[ant] = outpost_guide
	    a.append(ant)
	  if len(a) >= ant_num:
	    #l.log("Out Ants: ", str(len(a)) + ' ' + str(a))
	    #l.log("Out Guide: \n", util.array_to_string(outpost_guide, True))
	    return a
	#l.log("Out Ants: ", str(len(a)) + ' ' + str(a))
	#l.log("Out Guide: \n", util.array_to_string(outpost_guide, True))
      return a

    def will_live(self, dest, check):
      "Determines if ant will die at destination"
      if check:
	surrroundings = pathfind.extended_surroundings(int(self.attack_radius + 1), dest, self.level_array)
	my_ants = 0
	enemy_ants = 0
	for s in surrroundings: 
	  if s == 'a':
	    my_ants += 1
	  elif s in ['b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k']:
	    enemy_ants += 1
	if my_ants > enemy_ants:
	  return True
	else: return False
      else:return True

    def move(self, ants, ant_list, live=True):
      "Assigns ants order, and manipulates destination array in place"
      #l.log_on = True
      if len(ant_list) > 0 and ant_list[0] == "stop":
	return False
      for ant in ant_list:
	if self.ant_lookup[ant] != None:
	  directions = pathfind.move_directions(ant, self.ant_lookup[ant])
	  if directions != None:
	    for d in directions:
	      dest = ants.destination(ant, d)
	      if dest not in self.destinations and ants.unoccupied(dest) and self.will_live(dest, live):
		#l.log("ant:order ", (ant, d))
		ants.issue_order((ant, d))
		self.destinations.append(dest)
		break
	self.destinations.append(ant)
      return True
	  
    def assign_orders(self, ants):
      "Ranks the assignment functions in order of importance"
      #l.log("Time1: ", ants.time_remaining())
      if not self.move(ants, self.assign_food(ants)): 
	#l.log("TIME OUT", "")
	return None
      #l.log("Time2: ", ants.time_remaining())
      if not self.move(ants, self.assign_defense(ants), live=False): 
      	#print "TIME OUT"
      	return None
      #l.log("Time3: ", ants.time_remaining())
      if not self.move(ants, self.assign_hills(ants)): 
      	#l.log("TIME OUT", "")
      	return None
      #l.log("Time4: ", ants.time_remaining())
      if not self.move(ants, self.assign_unseen(ants)): 
      	#l.log("TIME OUT", "")
      	return None
      #l.log("Time5: ", ants.time_remaining())
      if not self.move(ants, self.assign_enemy(ants), live = False): 
      	#l.log("TIME OUT", "")
      	return None
      #l.log("Time6: ", ants.time_remaining())
      if not self.move(ants, self.assign_outposts(ants)): 
      	#l.log("TIME OUT", "")
      	return None
      #l.log("Time7: ", ants.time_remaining())
        
    def do_turn(self, ants):
      "Use each ants guide map to determine direction to give to server"
      #l.log_on = True
      self.turn += 1
      #l.log("Turn: ", self.turn)
      self.update_level(ants)
      self.update(ants)
      self.assign_orders(ants)

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
