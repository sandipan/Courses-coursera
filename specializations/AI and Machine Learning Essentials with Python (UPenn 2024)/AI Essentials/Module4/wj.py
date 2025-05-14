"""Example of two water jugs problem for use with AIMA code"""

#! /usr/bin/python

from search import *

class WJ(Problem):

    """The classic two water jugs problem.  We are given two jugs J0
    and J1 of capacies C0 and C1 liters and initially they contain W1
    and W2 liters of water.  Can you end up with exactly G0 liters in
    J0 and G1 liters in J1?  You are allowed just the following
    actions: dump the contents of either jug onto the floor, or pour
    the contents of one jug into the other untill either the jug from
    which you are ouring is empty or the one you are filling is full.

    A state is a tuple like (3,2) which says that jug J0 has 3 liters
    and J1 2 liters.

    A goal is a state except that a value of '*' is a "don't care", so
    valid goals might look like (1,1) or (*,2).

    Specifying a two jug problem requires specifying the capacities of
    each jug, the initial state and the goal.

    It's relatively easy to generalize this to N jugs.
    """

    def __init__(self, capacities=(5,2), initial=(5,0), goal=(0,1)):
        self.capacities = capacities
        self.initial = initial
        self.goal = goal

    def __repr__(self):
        """returns a string representing the object"""
        return "WJ(%s,%s,%s)" % (self.capacities, self.initial, self.goal)

    def goal_test(self, state):
        """returns true if state is a goal state"""
        g = self.goal
        return (state[0] == g[0] or g[0] == '*' ) and \
               (state[1] == g[1] or g[1] == '*')

    def successor(self, J0J1):
        """returns a list of successors to state"""
        J0, J1 = J0J1
        successors = []
        (C0, C1) = self.capacities
        if J0 > 0:
            successors.append(('dump jug 0', (0, J1)))
        if J1>0:
             successors.append(('dump jug 1', (J0, 0)))
        if J1 < C1 and J0 > 0:
            delta = min(J0, C1 - J1)
            successors.append(('pour jug 0 into jug 1', (J0 - delta, J1 + delta)))
        if J0 < C0 and J1 > 0: 
            delta = min(J1, C0 - J0)
            successors.append(('pour jug 1 into jug 0', (J0 + delta, J1 - delta)))
        return successors


def main():
    searchers = [breadth_first_tree_search, breadth_first_graph_search, depth_first_graph_search,
                 iterative_deepening_search, depth_limited_search]
    problems = [WJ((5,2),(5,0),(0,1)),WJ((5,2),(5,0),(2,0))]
    for p in problems:
        for s in searchers:
            print("Solution to %s found by %s" % (p, s.__name__))
            path = s(p).path()
            path.reverse()
            print(path)
            print()
    print("SUMMARY: successors/goal tests/states generated/solution")
    compare_searchers(problems=problems,
            header=['SEARCHER', 'GOAL:(0,1)', 'GOAL:(2,0)'],
            searchers=[breadth_first_tree_search,
                      breadth_first_graph_search, depth_first_graph_search,
                      iterative_deepening_search, depth_limited_search])

# if called from the command line, call main()
if __name__ == "__main__":
    main()
