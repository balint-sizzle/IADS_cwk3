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
        pass

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
        pass
