![Alt text](screenshot.jpg)



# Google AI Challenge 2011

- Contest site: (http://aichallenge.org/)
- My profile: (http://aichallenge.org/profile.php?user=9790)

## Strategy
- Created basic breadth first path finding algorithum
  - Input destinations
  - Returns list of ants ranked from closest to farthest
- Prioritized destinations
  1. Gathering food
  2. Defending hills *(set up diamond configuration around hill)*
  3. Attacking enemy hills 
  4. Exploring unseen regions
  5. Charging enemy ants *(only with advantage in numbers)*
  6. Randomly patrol region of the board *(overlay grid of ants on map)*


![Alt text](screenshot2.jpg)
