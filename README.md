![Alt text](Google-AI-Ants/raw/master/screenshot.jpg)



# Google AI Challenge 2011

- Contest site: (http://aichallenge.org/)
- My profile: (http://aichallenge.org/profile.php?user=9790)

## Strategy
- Created basic breadth first path finding algorithum
  - Input destinations
  - Returns list of ants ranked from closest to farthest
- Prioritized destinations
  1. Gathering food
  2. Defending hills *(set up diamond configuration)*
  3. Attacking enemy hills 
  4. Exploring unseen regions
  5. Charging enemy ants* (only with advantage in number)*
  6. Randomly patrole region of the board *(set up grid)*


![Alt text](Google-AI-Ants/raw/master/screenshot2.jpg)
