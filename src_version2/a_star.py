
#f = open('/home/david/ants/log.txt', 'w')
#log_on = False
#def log(tag, message):
  #if log_on:
    #string = tag + ': ' + str(message) + '\n'
    #f.write(string)
    #f.flush()

def get_symbol_at_loc(loc, array):
  "Returns symbol at location in array"
  y, x = loc
  symbol_at_loc = array[y][x]
  return symbol_at_loc

def is_int(s):
  "Checks if input is integer" 
  try: 
    int(s)
    return True
  except ValueError:
    return False

def place_numbers(loc, array):
  "Manipulates array, places numbers around location, returns tiles changes"
  y, x = loc
  loc_symbol = get_symbol_at_loc(loc, array)
  replace_symbols = ['.', '*']
  changed_tiles = []
  
  w = x - 1
  if w < 0: w = len(array[0]) - 1
  e= x + 1
  if e > len(array[0]) - 1: e = 0
  n = y - 1
  if n < 0: n = len(array) - 1
  s = y + 1
  if s > len(array) - 1: s = 0
  w_symbol = get_symbol_at_loc((y, w), array)
  e_symbol = get_symbol_at_loc((y, e), array)
  n_symbol = get_symbol_at_loc((n, x), array)
  s_symbol = get_symbol_at_loc((s, x), array)
  
  if not is_int(loc_symbol):
    if w_symbol in replace_symbols:
      array[y][w] = 1
      changed_tiles.append((y, w))
    if e_symbol in replace_symbols:
      array[y][e] = 1
      changed_tiles.append((y, e))
    if n_symbol in replace_symbols:
      array[n][x] = 1
      changed_tiles.append((n, x))
    if s_symbol in replace_symbols:
      array[s][x] = 1
      changed_tiles.append((s, x))
  elif is_int(loc_symbol):
    if w_symbol in replace_symbols:
      array[y][w] = int(loc_symbol) + 1
      changed_tiles.append((y, w))
    if e_symbol in replace_symbols:
      array[y][e] = int(loc_symbol) + 1
      changed_tiles.append((y, e))
    if n_symbol in replace_symbols:
      array[n][x] = int(loc_symbol) + 1
      changed_tiles.append((n, x))
    if s_symbol in replace_symbols:
      array[s][x] = int(loc_symbol) + 1
      changed_tiles.append((s, x))
  return changed_tiles

def place_all_numbers(destinations, array):
  "Manipulates array, place all numbers for list of destinations, returns array"
  for dest in destinations:
    y, x = dest
    array[y][x] = 'D'
  change_tiles = destinations
  while len(change_tiles) > 0:
    new_change_tiles = []
    for tile in change_tiles:
      new_change_tiles = new_change_tiles + place_numbers(tile, array)
    change_tiles = new_change_tiles
  return array

def move_direction(loc, array):
  "Returns list sorted by the shortest directions to move"
  y, x = loc
  w = x - 1
  if w < 0: w = len(array[0]) - 1
  e= x + 1
  if e > len(array[0]) - 1: e = 0
  n = y - 1
  if n < 0: n = len(array) - 1
  s = y + 1
  if s > len(array) - 1: s = 0
  west = ['w', array[y][w]]
  east = ['e', array[y][e]]
  north = ['n', array[n][x]]
  south = ['s', array[s][x]]
  directions_dist = [west, east, north, south]
  for d in directions_dist:
    if d[1] == "D":
      d[1] = 0
    elif not is_int(d[1]):
      directions_dist.remove(d)
  directions_dist = sorted(directions_dist, key=lambda d: d[1])
  directions = []
  for d in directions_dist:
    directions.append(d[0])
  if get_symbol_at_loc(loc, array) != 'D':
    return directions
  else: return None

def place_destinations_around_point(loc, array):
  "Makes every tile around point a destination"
  y, x = loc
  replace_symbols = ['.', '*', 'a']
  changed_tiles = []
  w = x - 1
  if w < 0: w = len(array[0]) - 1
  e= x + 1
  if e > len(array[0]) - 1: e = 0
  n = y - 1
  if n < 0: n = len(array) - 1
  s = y + 1
  if s > len(array) - 1: s = 0
  w_symbol = get_symbol_at_loc((y, w), array)
  e_symbol = get_symbol_at_loc((y, e), array)
  n_symbol = get_symbol_at_loc((n, x), array)
  s_symbol = get_symbol_at_loc((s, x), array)
  if w_symbol in replace_symbols:
    changed_tiles.append((y, w))
  if e_symbol in replace_symbols:
    changed_tiles.append((y, e))
  if n_symbol in replace_symbols:
    changed_tiles.append((n, x))
  if s_symbol in replace_symbols:
    changed_tiles.append((s, x))
  return changed_tiles

def defensive_destinations(hill, array):
  "Returns list of points to be defended"
  destinations = []
  change_tiles = place_destinations_around_point(hill, array)
  count = 0
  while count < 1:
    new_change_tiles = []
    for tile in change_tiles:
      destinations.append(tile)
      new_change_tiles = new_change_tiles + place_destinations_around_point(tile, array)
    change_tiles = new_change_tiles
    count += 1
  return destinations

def ant_distance(loc, level):
  "Determines ants distance base on level array"
  y, x = loc
  if level[y][x] == 'D':
    return 0
  elif level[y][x] == -1:
    return -1
  w = x - 1
  if w < 0: w = len(level[0]) - 1
  e= x + 1
  if e > len(level[0]) - 1: e = 0
  n = y - 1
  if n < 0: n = len(level) - 1
  s = y + 1
  if s > len(level) - 1: s = 0
  west = level[y][w]
  east = level[y][e]
  north = level[n][x]
  south = level[s][x]
  directions = [west, east, north, south]
  return sorted(directions)[0]

def surroundings(loc, level):
  "Returns list of the symbols of the four surrounding tiles"
  y, x = loc
  w = x - 1
  if w < 0: w = len(level[0]) - 1
  e= x + 1
  if e > len(level[0]) - 1: e = 0
  n = y - 1
  if n < 0: n = len(level) - 1
  s = y + 1
  if s > len(level) - 1: s = 0
  w_symbol = get_symbol_at_loc((y, w), level)
  e_symbol = get_symbol_at_loc((y, e), level)
  n_symbol = get_symbol_at_loc((n, x), level)
  s_symbol = get_symbol_at_loc((s, x), level)
  return [w_symbol, e_symbol, n_symbol, s_symbol]




