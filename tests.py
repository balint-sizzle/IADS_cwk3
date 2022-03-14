import math
import graph


g=graph.Graph(12,"twelvenodes")
g.tourValue()
print(g.tour, g.perm)
g.swapHeuristic(12)
g.tourValue()
print(g.tour, g.perm)