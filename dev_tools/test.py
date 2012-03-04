import util, pathfind, MyBot, random, cProfile

world = """# .a%%%...........%%%%%%%................
# aa%%%...........a...a......a............
# .a%%%....%........................%....
# .a%%%...%a%.....a.................%....
# .%%%...%aaa%.....a................%....
# .%%...%.aaaa%.....a...............%....
# %%%%...%aaaa......................%....
# %%%%%...aaa...........a...........%....
# %%%%%....a................a.......%....
# %%%%%.............*...............%....
# %%%%%..................................
# .%%%%..................................
# .%%%%......*.....%...%.....*...........
# ..%%%.............%%%.a................
# ...%%..................................
# ..................%%%..................
# .................%...%.................
# ......*.........a...%...*........*.....
# ...................%.%.................
# ....................%..................
# ............b........b.................
# ...%%...........!......................
# ...%%...................*..............
# ...%%....*......!......................
# ..%%%..............a...................
# ..%%%..................................
# ..%%%...........%%%%%%%................"""
###Util Tests
world_string = util.strip_string(world)
print world_string
world_array = util.string_to_array(world_string)
#print util.array_to_string(world_array, True)
#world_array[1][1] = -2
food = []
my_ants = []
enemy_ants = []
for y in range(0, len(world_array)):
  for x in range(0, len(world_array[0])):
    if world_array[y][x] == '*':
      food.append((y, x))
    elif world_array[y][x] == 'a':
      my_ants.append((y, x))
    elif world_array[y][x] == 'b':
      enemy_ants.append((y, x))
#print "Food", food
#print "My Ants", my_ants

def create_random_list():
  l = []
  for y in range(0, 3):
    row = []
    for x in range(0, 3):
      row.append(random.choice(['.',1, 2, 3]))
    l.append(row)
  return l, (random.randint(0, 2), random.randint(0, 2))

def test_is_int():
  return util.is_int('h')
###A* Tests
def test_get_symbol_at_loc():
  return pathfind.get_symbol_at_loc((3, 3), world_array)

def test_surroundings():
  return pathfind.surroundings((1, 3), world_array, True) 
  
def test_extended_surroundings():
  return pathfind.extended_surroundings(4, (5, 5), world_array) 
  
def test_place_numbers():
  return pathfind.place_numbers((1, 0), world_array, ['.', '*', '!'], 'a') 
  
def test_create_guide():
  return pathfind.create_guide([(10, 10), (0, 0), (20, 20)], world_array)
  
def test_create_individual_guides():
  return pathfind.create_individual_guides([(10, 10), (20, 20)], world_array)
  
def test_move_direction():
  return pathfind.move_directions((6, 6), guide) 
  
def test_ant_distance():
  return pathfind.ant_distance((10, 9), guide)
  
def test_defense_place_numbers():
  return pathfind.defense_place_numbers((1, 1), world_array, ['.', '*', '!'])  

def test_set_defensive_perimeter():
  return pathfind.set_defensive_perimeter(5, [(10, 10)], world_array)
  
def test_create_defensive_guide():
  return pathfind.create_defensive_guide(3, [(5, 9)], world_array)
 
def test_four_corner_defense():
  return pathfind.four_corner_defense([(1, 1), (10, 10)], world_array)
  
def test_get_all_outposts():
  return pathfind.get_all_outposts([(20, 20)], 20, 4, world_array)
  
def test_get_outposts():
  return pathfind.get_outposts((24, 36), 3, world_array)
  
#print test_get_symbol_at_loc()
#print test_is_int(), 
#print test_surroundings()
#print test_extended_surroundings()
#print test_place_numbers()
#print util.array_to_string(world_array, True)
#guide = test_create_guide()
#print util.array_to_string(guide, True)
#print guide[1]
#print util.array_to_string(world_array)
#print test_move_direction()
#print test_ant_distance()
#print "Destinations: ", perimeter[1]
#print util.array_to_string(world_array, True)
#print "Changed Tiles: ", perimeter[0]
#guide = test_create_defensive_guide()
#print util.array_to_string(guide[0], True)
#print "Destinations: ", guide[1]
#print util.array_to_string(world_array, True)
#print test_four_corner_defense()
#test_get_all_outposts()
for p in test_get_all_outposts()[0]:
  y, x = p
  world_array[y][x] = 'D'
print util.array_to_string(world_array, True)
#print util.array_to_string(pathfind.create_guide(test_get_all_outposts(), world_array), True)
#print util.array_to_string(pathfind.create_guide([(1, 1)], world_array), True)
#perimeter = test_set_defensive_perimeter()
##print "Changed: ", perimeter[0]

def profile_place_numbers():
  for n in range(0 ,800000):
    l, p = create_random_list()
    #print "Starting:\n", util.array_to_string(l)
    #print "Changed point:", p
    pathfind.place_numbers(p, l, ['.', '*', '!', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k'], None)
    
    #print "Ending:\n", util.array_to_string(l)

def profile_surroundings():
  l, p = create_random_list()
  for n in range(0 , 8000000):
    pathfind.surroundings(p, l)
  

#cProfile.run('profile_surroundings()')
  

