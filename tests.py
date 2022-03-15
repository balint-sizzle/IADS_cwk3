import math
import graph


g=graph.Graph(12,"twelvenodes")
g.Greedy()
g.tourValue()
print(g.tour, g.perm)