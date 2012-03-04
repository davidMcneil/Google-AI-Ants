import random, os

level_files = os.popen("find tools/maps -name '*.map'").read()
levels = []
line = ''
for char in level_files:
  if char == "\n":
    levels.append(line)
    line = ''
  else: line = line + char
levels.pop()
#levels = ["/home/david/ants/tools/maps/cell_maze/cell_maze_p09_03.map"]
other_players = ["/home/david/ants/tools/sample_bots/python/GreedyBot.py", "/home/david/ants/tools/sample_bots/python/HunterBot.py", "/home/david/ants/tools/sample_bots/python/LeftyBot.py"]
game_count = 0
rankings = {"MyBot.py" : [0, 0], "version4.py" : [0, 0]}
while game_count < 50:
  game_count +=1
  print "Game Number: ", game_count
  level = random.choice(levels)
  number_players = int(level[-9] + level[-8])
  players = ["/home/david/ants/MyBot.py", "/home/david/ants/src_version4/version4.py"]
  for p in range(0, number_players - 2):
    players.append(random.choice(other_players))
    
  player_string = ''
  for p in players:
    player_string =  player_string + " 'python " + p + "'" 

  #print number_players
  #print level
  #print len(players), players
  #print player_string

  command = "python tools/playgame.py " + player_string + " --map_file " + level + " --log_dir game_logs --turns 1000 --food --verbose -e"
  print "Command: ", command
  os.system(command)

  f = open('/home/david/ants/game_logs/0.replay', 'r')
  contents = ''
  for char in f:
    contents = contents + char
  dictionary = eval(contents)
  count = 0
  for player in dictionary["playernames"]:
    if player == "MyBot.py" or player == "version4.py":
      rankings[player] = [dictionary["rank"][count] + rankings[player][0], dictionary["score"][count] + rankings[player][1]]
    count +=1
  print rankings
  
  