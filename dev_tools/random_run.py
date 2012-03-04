import random, os

level_files = os.popen("find tools/maps -name '*.map'").read()
levels = []
line = ''
for char in level_files:
  if char == "\n":
    levels.append(line)
    line = ''
  else: line = line + char

other_players = ["/home/david/ants/tools/sample_bots/python/GreedyBot.py", "/home/david/ants/tools/sample_bots/python/HunterBot.py", "/home/david/ants/tools/sample_bots/python/LeftyBot.py"]
players = ["/home/david/ants/src_version2/version2.py", "/home/david/ants/MyBot.py"]

level = random.choice(levels)
number_players = int(level[-10] + level[-9])
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
os.system(command)