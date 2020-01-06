#!/usr/bin/env python
"""
This module implements the lilypond model solver specified in
the Heveling & Last (2005) paper.

Works in O(n^2) but is apparently much faster in the normal case.
The current implementation is actually O(n^3) since we're not
intelligently culling pairs. We're more interested in the number
of global steps this algorith will takes (worst case n but is usually
much less).
"""
import math
import sys
import csv
import fileinput

from typing import List

import lp

def dist(grain1, grain2):
    """
    Calculates the distance between two objects assuming both
    objects have an x and y attribute.

    This function is designed to be easily swapped out with any
    metric you want. 3D or even manhattan.
    """
    assert hasattr(grain1, 'x') and hasattr(grain1, 'y')
    assert hasattr(grain2, 'x') and hasattr(grain2, 'y')
    return math.sqrt((grain1.x - grain2.x)**2 + (grain1.y - grain2.y)**2)

def create_dist_mat(grains: List[object]):
    """ Creates a function that has all the distances cached """
    # We're creating an bottom triangle matrix
    dist_mat = [[dist(grains[row], grains[col]) for col in range(row)] \
            for row in range(len(grains))]

    def dist_get(i, j):
        if i == j:
            return math.inf
        # column must be less than row
        i, j = (j, i) if j > i else (i, j)
        return dist_mat[i][j]

    return dist_get

def solve(args: dict):
    """ Takes a dictionary called args. Usually gathered from the lp module """
    assert "grains" in args
    if "dims" in args:
        # Handle the border case
        #raise NotImplementedError()
        print("Handling borders is not implemented yet", file=sys.stderr)

    # Create two sets. One for undetermined (growing) grains and one for solved grains
    grains = args["grains"]

    # create a 2d matrix to store all distances between grains. dist[row][col]
    # The diagonal should be all zeros. Remove any chance of floating point errors to pop up
    dist_mat = create_dist_mat(grains)

    old_f = [0] * len(grains)
    f = [min((max(dist_mat(x, y)/2, dist_mat(x, y) - old_f[y]) \
            for y in range(len(grains)))) \
            for x in range(len(grains))]
    global_steps = 1

    while old_f != f:
        # we define our radii function as a list that is generated from a mapping (maybe)
        old_f = f
        # for each grain calculate
        f = [min((max(dist_mat(x, y)/2, dist_mat(x, y) - old_f[y]) \
                for y in range(len(grains)))) \
                for x in range(len(grains))]

        global_steps += 1
        print(__file__, "currently on step:", global_steps, file=sys.stderr)

    # Should be solved now
    print("ZZZZZZZZZZ")
    for grain, r in zip(grains, f):
        grain.r = r
        grain.i = -1
        print(grain)

    # TODO: Should probably print the dimensions and other stuff
    print(__file__, "global steps:", global_steps, file=sys.stderr)

if __name__ == "__main__":
    READER = csv.reader(row for row in fileinput.input() if not row.startswith('#'))

    PARSED = lp.parse_all(READER)
    solve(PARSED)
