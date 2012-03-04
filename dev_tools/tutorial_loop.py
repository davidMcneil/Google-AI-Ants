import random, os

rankings = {"MyBot.py" : [0, 0], "version4.py" : [0, 0]}
for x in range(0, 200):
  print "Game: ", x
  os.system('''python tools/playgame.py "python MyBot.py" "python /home/david/ants/src_version4/version4.py" --map_file /home/david/ants/tools/maps/example/tutorial1.map --log_dir game_logs --turns 1000 --food --verbose -e''')
  
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