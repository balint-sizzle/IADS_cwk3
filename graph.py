from email.mime import base
import math
import random


def euclid(p,q):
    x = p[0]-q[0]
    y = p[1]-q[1]
    return math.sqrt(x*x+y*y)
                
class Graph:

    # Complete as described in the specification, taking care of two cases:
    # the -1 case, where we read points in the Euclidean plane, and
    # the n>0 case, where we read a general graph in a different format.
    # self.perm, self.dists, self.n are the key variables to be set up.
    def __init__(self,n,filename):
        with open(filename, "r") as f:
            if n < 0:
                lines = list(map(lambda x: list(map(int, x.split("  "))), list(map(str.strip, f.readlines()))))
            else:
                lines = list(map(lambda x: list(map(int, x.split(" "))), list(map(str.strip, f.readlines()))))
        f.close()
        if n < 0: 
            self.n = len(lines)
            self.dists = [[euclid(lines[i], lines[j]) for j in range(self.n)] for i in range(self.n)]
        else: 
            self.n = n
            self.dists = [[0 for j in range(self.n)] for i in range(self.n)]
            for node in lines:
                start = node[0]
                end = node[1]
                weight = node[2]
                self.dists[start][end] = weight
                self.dists[end][start] = weight
        self.perm = [i for i in range(self.n)]
        self.tour = float("inf")

    # Complete as described in the spec, to calculate the cost of the
    # current tour (as represented by self.perm).
    def tourValue(self):
        cost = 0
        current = self.perm[0]
        for next in self.perm[1:]:
            cost += self.dists[current][next] # potential bad
            #print(current,"-",self.dists[current][next],"->",next, ":", cost)
            current = next
        cost += self.dists[self.perm[0]][current]
        #print(self.perm[0],"-",self.dists[self.perm[0]][current],"->",next, ":", cost)
        self.tour = cost

    # Attempt the swap of cities i and i+1 in self.perm and commit
    # commit to the swap if it improves the cost of the tour.
    # Return True/False depending on success.
    def trySwap(self,i):
        basecost = self.tour
        if i+1 >= self.n:
            return False
        self.perm[(i+1)], self.perm[i] = self.perm[i], self.perm[(i+1)]
        self.tourValue()
        if self.tour < basecost: 
            return True
        else: 
            self.perm[(i+1)], self.perm[i] = self.perm[i], self.perm[(i+1)]
            self.tour = basecost
            return False


    # Consider the effect of reversiing the segment between
    # self.perm[i] and self.perm[j], and commit to the reversal
    # if it improves the tour value.
    # Return True/False depending on success.              
    def tryReverse(self,i,j):
        basecost = self.tour
        pre = self.perm[:i]
        post = self.perm[j+1:]
        segment = self.perm[i:j+1]
        self.perm = pre+segment[::-1]+post
        self.tourValue()
        if self.tour < basecost:
            return True
        else:
            self.tour = basecost
            self.perm = pre+segment+post

    def swapHeuristic(self,k):
        better = True
        count = 0
        while better and (count < k or k == -1):
            better = False
            count += 1
            for i in range(self.n):
                if self.trySwap(i):
                    better = True

    def TwoOptHeuristic(self,k):
        better = True
        count = 0
        while better and (count < k or k == -1):
            better = False
            count += 1
            for j in range(self.n-1):
                for i in range(j):
                    if self.tryReverse(i,j):
                        better = True

                        
    # Implement the Greedy heuristic which builds a tour starting
    # from node 0, taking the closest (unused) node as 'next'
    # each time.
    def Greedy(self):
        import time
        unused_nodes = [i for i in range(self.n)]
        perm_i = 0
        current_node = 0
        while len(unused_nodes) > 0:
            best_town = 0
            lowest_dst = float("inf")
            for i in unused_nodes:
                if self.dists[current_node][i] < lowest_dst:
                    lowest_dst = self.dists[current_node][i]
                    best_town = i
            self.perm[perm_i] = best_town
            perm_i += 1
            current_node = best_town
            unused_nodes.remove(best_town)
            # visualise.draw_best(self.perm)
            # visualise.draw_towns()
            # visualise.update_screen()
            time.sleep(0.04)
        self.tourValue()
        #print(self.tour)
        # visualise.hold()

    
    #Upper bound decided by number of ants, n, number of iterations
    #O(sn), where s=number of ants * number of iterations and n=number of towns
    def antColonyOptimisation(self, ants=40, alpha=2, beta=3.7, Q=1, p=0.3, iter=50):
        """ 
            Approximation algorithm for metric TSP problems

            ants: number of ants to simulate each iteration
            alpha: weight of pheromone amplification heuristic in probability function
            beta: weight of closest city heuristic in probability function
            Q: arbitary constant
            p: pheromone decay parameter
            iter: number of iterations
        
        dists for 12
       [[0, 4, 4, 4, 2, 3, 4, 6, 5, 2, 1, 3],
       [4, 0, 3, 3, 4, 5, 3, 2, 3, 6, 7, 4],
       [4, 3, 0, 3, 3, 3, 3, 3, 2, 4, 3, 4],
       [4, 3, 3, 0, 1, 3, 3, 2, 3, 3, 4, 2],
       [2, 4, 3, 1, 0, 2, 4, 5, 5, 3, 4, 3],
       [3, 5, 3, 3, 2, 0, 2, 1, 3, 2, 3, 1],
       [4, 3, 3, 3, 4, 2, 0, 3, 4, 3, 5, 3],
       [6, 2, 3, 2, 5, 1, 3, 0, 3, 2, 4, 5],
       [5, 3, 2, 3, 5, 3, 4, 3, 0, 4, 5, 4],
       [2, 6, 4, 3, 3, 2, 3, 2, 4, 0, 3, 4],
       [1, 7, 3, 4, 4, 3, 5, 4, 5, 3, 0, 3],
       [3, 4, 4, 2, 3, 1, 3, 5, 4, 4, 3, 0]])
        """
        #import numpy as np
        #import visualise
        
        self.pheromone_trails = [[1 if i!=j else 0 for j in range(self.n)] for i in range(self.n)]
        best = float("inf")
        #best_path = []
        for i in range(iter):
            #print("iter:",i)
            ant_paths = []
            for k in range(ants):
                start = random.randint(0,self.n-1)
                path = [start]
                self.remaining_towns = [i for i in range(self.n) if start != i]

                while len(path) < self.n:
                    path.append(self.pick_next_town(path[-1], alpha, beta))
                    #visualise.update_screen()

                self.perm = path
                self.tourValue()
                if self.tour < best:
                    
                    #best_path = path
                    best = self.tour
                # visualise.draw_best(path)
                # visualise.draw_towns()
                # visualise.update_screen()
                ant_paths.append((path, self.tour))
                #print(path, self.tour)
            #print(np.array(self.pheromone_trails))
            self.update_pheromone_trails(Q, p, ant_paths)
        self.tour = best
        # visualise.draw_best(best_path)
        # visualise.draw_towns()
        # visualise.hold()

    def update_pheromone_trails(self, Q, p, ant_paths):
        
        for i in range(self.n):
            for j in range(self.n):
                pheromone_delta = sum([Q/L if (path.index(j)-1 == path.index(i) and i != j) else 0 for (path, L) in ant_paths])
                #print("D:", pheromone_delta)
                self.pheromone_trails[i][j] = (1-p)*self.pheromone_trails[i][j] + pheromone_delta

    def pick_next_town(self, current_town, alpha, beta):
        numerators = [0 if current_town==j else (self.pheromone_trails[current_town][j]**alpha)*((1/self.dists[current_town][j])**beta) for j in self.remaining_towns]
        denominator = sum(numerators)
        weights = [n/denominator for n in numerators]
        next_town = random.choices(self.remaining_towns, weights=weights, k=1)[0]
        self.remaining_towns.remove(next_town)
        return next_town