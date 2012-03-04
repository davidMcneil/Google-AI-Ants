class log:
    def __init__(self):
      self.log_on = True
      self.f = open('/home/david/ants/log.txt', 'w')
    def log(self, tag, message):
      if self.log_on:
	string = tag + str(message) + '\n'
	self.f.write(string)
	self.f.flush()
l = log()

def safe_divide(n1, n2):
  "Checks if input is integer" 
  try: 
    n1 / n2
    return n1 / n2
  except ValueError:
    return 0

def is_int(s):
  "Checks if input is integer" 
  try: 
    int(s)
    return True
  except ValueError:
    return False

def same_items(items, value):
  return all(x == value for x in items)

def string_to_array(string):
  'Converts a level string to a 2D array'
  array = []
  for line in string.splitlines():
    l = []
    for char in line:
      if char != '#' and char != " ":
	l.append(char)
    array.append(l)
  return array

def array_to_string(array, double=False):
  'Converts a level array to a pretty string'
  string = ''
  for row in array:
    s = ''
    for col in row:
      if not double:
	if len(str(col)) < 2:
	  s = s + str(col)
	else: s = s + str(col)
      else:
	if len(str(col)) < 2:
	  s = s + '  ' + str(col)
	else: s = s + ' ' + str(col)
    string = string + s + '\n'
  return string

def strip_string(string):
  s = ''
  for char in string:
    if char != '#' and char != " ":
      s = s + char
  return s
  
def zero(num):
  if num > 0: num -= 1
  else: num += 1
  return num