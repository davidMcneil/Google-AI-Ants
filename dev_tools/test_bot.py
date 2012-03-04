import cProfile
import os
from MyBot import *

os.system("cat output.txt > input.txt")

def test_my_bot():
  f = open('/home/david/ants/input.txt', 'r')
  run_my_bot(f)

cProfile.run('test_my_bot()')