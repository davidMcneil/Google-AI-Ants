import util, copy

def surroundings(loc, array, need_directions = False):
  "Returns list of the west, east, north, south values and the symbols of the four surrounding tiles"
  y, x = loc
  w = x - 1
  if w < 0: w = len(array[0]) - 1
  e= x + 1
  if e > len(array[0]) - 1: e = 0
  n = y - 1
  if n < 0: n = len(array) - 1
  s = y + 1
  if s > len(array) - 1: s = 0
  w_symbol = array[y][w]
  e_symbol = array[y][e]
  n_symbol = array[n][x]
  s_symbol = array[s][x]
  if need_directions:
    return {'w' : w_symbol, 'e' : e_symbol, 'n' : n_symbol, 's' : s_symbol}
  else: return {(y, w) : w_symbol, (y, e) : e_symbol, (n, x) : n_symbol, (s, x) : s_symbol}
  
def extended_surroundings(radius, loc, array):
  "Returns list of all tiles within radius"
  surroundings_lookup = surroundings(loc, array)
  points = surroundings_lookup.keys()
  for n in range(0, radius - 1):
    new_points = []
    for p in points:
      new_surroundings_lookup = surroundings(p, array)
      new_points += new_surroundings_lookup.keys()
      surroundings_lookup.update(new_surroundings_lookup)
    points = list(set(new_points))
  return surroundings_lookup.values()

def place_numbers(loc, level, replace_symbols):
  "Manipulates array: places numbers around location, returns tiles changes and point stopped"
  y, x = loc
  loc_symbol = level[y][x]
  if loc_symbol == 'A':
    return [], loc
  changed_tiles = []
  x_size = len(level[0])
  y_size = len(level)
  w = x - 1
  if w < 0: w = x_size - 1
  e= x + 1
  if e > x_size - 1: e = 0
  n = y - 1
  if n < 0: n = y_size - 1
  s = y + 1
  if s > y_size - 1: s = 0
  points = [(y, w), (y, e), (n, x), (s, x)]
  for point in points:
    y, x = point
    s = level[y][x]
    if s in replace_symbols:
      is_int = util.is_int(loc_symbol)
      if not is_int and loc_symbol != 'A':
	level[y][x] = 1
      elif is_int:
	level[y][x] = int(level[loc[0]][loc[1]]) + 1
      changed_tiles.append((y, x))
  return changed_tiles, None
  
def create_guide(destinations, level, depth=None, unseen = None):
  "Places all numbers for list of destinations and successive points, returns changed array perserves old one"
  l = copy.deepcopy(level)
  replace_symbols = ['.', '*', '!', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k']
  ###d = destination with ant, D = destination without ant
  for dest in destinations:
    y, x = dest
    if l[y][x] == 'a':
      l[y][x] = 'A'
    else: l[y][x] = 'D'
  changed_tiles = destinations
  while len(changed_tiles) > 0:
    if depth != None:
      if depth <= 0: break
      else: depth -= 1
    new_change_tiles = []
    for tile in changed_tiles:
      tiles, point = place_numbers(tile, l, replace_symbols)
      new_change_tiles = new_change_tiles + tiles
    changed_tiles = new_change_tiles
  return l

def move_directions(loc, guide):
  "Returns list sorted by the shortest direction to move"
  y, x = loc
  if guide[y][x] == "A":
    return None
  surroundings_lookup = surroundings(loc, guide, True)
  for d in surroundings_lookup:
    if util.is_int(surroundings_lookup[d]): 
      surroundings_lookup[d] = abs(surroundings_lookup[d])
  ###Sets all destinations to zero making them the closest
  for d in surroundings_lookup:
    if surroundings_lookup[d] == "D":
      surroundings_lookup[d] = 0
  directions = []
  for d in sorted(surroundings_lookup, key=surroundings_lookup.get):
    if util.is_int(surroundings_lookup[d]): 
      directions.append(d)
  return directions

def ant_distance(loc, guide):
  "Determines ants distance based on level array"
  y, x = loc
  if guide[y][x] == 'A':
    return 0
  elif util.is_int(guide[y][x]): 
    return guide[y][x]
  else: return None

###
  
def defense_place_numbers(loc, level, replace_symbols):
  "Places numbers around point, loc must be a number, if surrouding == 0 adds to destinations"
  y, x = loc
  loc_symbol = level[y][x]
  changed_tiles = []
  destinations = []
  surroundings_lookup = surroundings(loc, level)
  for point in surroundings_lookup:
    y, x = point
    if surroundings_lookup[point] in replace_symbols:
      new_value = int(loc_symbol) + 1
      if new_value != 0:
	level[y][x] = new_value
	changed_tiles.append(point)
      else:
	destinations.append(point)
  return changed_tiles, destinations

def set_defensive_perimeter(radius, hills, level):
  "Places numbers starting from hill going out to specified radius"
  l = copy.deepcopy(level)
  replace_symbols = ['.', '*', '!', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']
  for h in hills:
    y, x = h
    l[y][x] = radius * -1
  count = radius
  change_tiles = hills[:]
  all_changed_tiles = change_tiles
  destinations = []
  while count > 0:
    new_change_tiles = []
    for point in change_tiles:
      tiles, d = defense_place_numbers(point, l, replace_symbols)
      new_change_tiles = new_change_tiles + tiles
      destinations = destinations + d
    change_tiles = new_change_tiles
    all_changed_tiles += change_tiles
    count -= 1
  return all_changed_tiles, list(set(destinations))
  
def create_defensive_guide(radius, hills, level):
  inside_perimeter, destinations = set_defensive_perimeter(int(radius), hills, level)
  guide = create_guide(destinations, level, depth=5)
  for point in inside_perimeter:
    y, x = point
    if not util.is_int(guide[y][x]):
      guide[y][x] = -1
    else:
      guide[y][x] = guide[y][x] * -1
  return guide, len(destinations)
  
	



  
  
  
  
  




