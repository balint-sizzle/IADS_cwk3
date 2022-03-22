import math
import graph
import itertools
from random import randint
# g=graph.Graph(12, "twelvenodes")
# g.antColonyOptimisation()

# g50 = graph.Graph(-1, "cities50")
# g.antColonyOptimisation()

# g6 =graph.Graph(6, "sixnodes")
# g.antColonyOptimisation()

# gn = graph.Graph(-1, "newtown")
# gn.antColonyOptimisation()


def random_euclid(span, n):
    """
    Writes a random euclidian TSP to a file called "newtown" in current directory
    span: the dimensions of the square shaped map to generate towns in
    n: number of towns
    """
    tsp = [(randint(0, span), randint(0, span)) for _ in range(n)]
    with open("newtown", "w") as f:
        for P in tsp:
            f.write(str(P[0])+"  "+str(P[1])+"\n")
    f.close()

def exact_solution(graph):
    best = float("inf")
    for p in list(itertools.permutations(graph.perm)):
        graph.perm = p
        graph.tourValue()
        if graph.tour < best:
            best = graph.tour
    return best

random_euclid(500, 10)

g = graph.Graph(-1, "newtown")
exact = round(exact_solution(g))
g = graph.Graph(-1, "newtown")
g.antColonyOptimisation()
ant = round(g.tour)
g = graph.Graph(-1, "newtown")
g.Greedy()
greedy = round(g.tour)
g = graph.Graph(-1, "newtown")
g.TwoOptHeuristic(12)
topt = round(g.tour)
g = graph.Graph(-1, "newtown")
g.swapHeuristic(12)
swap = round(g.tour)
print(f"exact: {exact}\ngreed: {greedy} {round((exact/greedy)*100, 2)}\n2-opt: {topt} {round((exact/topt)*100, 2)}\nswap: {swap} {round((exact/swap)*100, 2)}\nant: {ant} {round((exact/ant)*100, 2)}")