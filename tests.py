import math
import graph

g=graph.Graph(12, "twelvenodes")
g.antColonyOptimisation()

g50 = graph.Graph(-1, "cities50")
g.antColonyOptimisation()

g6 =graph.Graph(6, "sixnodes")
g.antColonyOptimisation()