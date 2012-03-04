from ants import *
import copy, math
import util, diffusion
from util import l

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
	self.level_fog = []
	self.level_guide = []
	self.level_size = ()
	self.total_tiles = 0
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
	self.level_fog.append(row)

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
      ###Update level fog
      for y in range(0, self.level_size[1]):
	for x in range(0, self.level_size[0]):
	  point = (y, x)
	  if ants.visible(point):
	    self.level_fog[y][x] = self.level_array[y][x]
      ###Reset destinations
      self.destinations = []
	 
    def create_guide(self):
      self.level_guide = copy.copy(self.level_fog)
      for y in range(0, self.level_size[1]):
	for x in range(0, self.level_size[0]):
	  if self.level_fog[y][x] == '*':
	    diffusion.diffuse_point(self.level_guide, (y, x), 10)
      l.log("Guide:\n", util.array_to_string(self.level_guide, True))
	    
    def move(self, ants):
      for ant in ants.my_ants():
	directions = diffusion.move_directions(ant, self.level_guide)
	if directions != None:
	  for d in directions:
	    dest = ants.destination(ant, d)
	    if dest not in self.destinations and ants.unoccupied(dest):
	      ants.issue_order((ant, d))
	      self.destinations.append(dest)
	      break
	  self.destinations.append(ant)
    
    def do_turn(self, ants):
      "Use each ants guide map to determine direction to give to server"
      l.log_on = True
      self.turn += 1
      l.log("Turn: ", self.turn)
      self.update_level(ants)
      self.create_guide()
      self.move(ants)

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
