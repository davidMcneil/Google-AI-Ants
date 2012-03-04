
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

def array_to_string(array):
  'Converts a level array to a pretty string'
  string = ''
  for row in array:
    s = ''
    for col in row:
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