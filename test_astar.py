from combat_simulator.grid import Grid
from combat_simulator.astar import astar

g = Grid((5, 3))
g._grid[1, 1] = 1 
g._grid[2, 0] = 1 
g._grid[2, 1] = 1 
g._grid[3, 1] = 1 
adj = g.to_adjacency()

start = (0, 2)
end = (4, 0)
g._grid[start] = 3
g._grid[end] = 4
print("Goal")
print(g)
path = astar(start, end, adj, moves=-1)
for (i, n) in enumerate(path):
    g._grid[n] = 2
g._grid[start] = 3
g._grid[end] = 4
print("Path")
print(g)
print(path)


g = Grid((12, 8))
g._grid[0, 2] = 1
g._grid[1, 2:6] = 1
g._grid[3, 2:8] = 1
g._grid[3:7, 1] = 1
g._grid[3:7, 5] = 1
g._grid[7, 2:4] = 1
g._grid[8:10, 2] = 1
g._grid[11:12, 2] = 1
adj = g.to_adjacency()

start = (0, 7)
end = (4, 4)
g._grid[start] = 3
g._grid[end] = 4
print("Goal")
print(g)
path = astar(start, end, adj, moves=-1)
for (i, n) in enumerate(path):
    g._grid[n] = 2
g._grid[start] = 3
g._grid[end] = 4
print("Path")
print(g)
print(path)
