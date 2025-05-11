"""Example of Missionaries and Cannibals for use with AIMA code"""

#! /usr/bin/python

from search import *

class MC(Problem):
    """ Classic missionaries and Cannibals problem.  A state is
     represented by a three typle (M,C,B) where M, C and B are the
     number of missionaries, cannibals and boats on the left bank,
     repsectively.  A state is legal if it is not the case that there
     are missionaries on a bank that re outnumbered by canniabls.
     Actions are that one or two people can row the boat from one bank
     to the other.  The problem is to find a sequence of actions to go
     from (3,3,1) to (0,0,0)."""

    def __init__(self, *args):
        super().__init__((3, 3, 1), (0, 0, 0))
        self.visited = set([])
        
    def h(self, node):
        print(node.state)
        return node.state[0] + node.state[1]

    def __repr__(self):
        """returns a string representing the object"""
        return str(self.initial)

    def goal_test (self, state):
        """returns true if state is a goal state"""
        return super().goal_test(state)

    def is_valid_bank(self, m, c):
        return m >= 0 and c >= 0 and ((m & c) == 0 or m >= c)

    def is_valid(self, state):
        m, c, s = state
        return self.is_valid_bank(m, c) and self.is_valid_bank(3-m, 3-c) and (m + c > 0 or s == 0)

    def successor(self, state):
        """returns a list of successors to state"""
        if state not in self.visited:
            self.visited.add(state)
        successors = []
        (m, c), s = state[:2], state[2]
        max_m, max_c = (3 - m, 3 - c) if s == 0 else (m, c)
        max_m, max_c = min(max_m,2), min(max_c,2)
        a = 'L' if s == 1 else 'R'
        ss = -1 if s == 1 else 1
        #print('here', state, max_m, max_c)
        for n in range(1, max_m+1):
            new_state = m + n*ss, c, 1-s
            if self.is_valid(new_state) and new_state not in self.visited:
                successors.append((a, new_state))
                self.visited.add(new_state)
        for n in range(1, max_c+1):
            new_state = m, c + n*ss, 1-s
            if self.is_valid(new_state) and new_state not in self.visited:
                successors.append((a, new_state))
                self.visited.add(new_state)
        new_state = m + ss, c + ss, 1-s
        if self.is_valid(new_state) and new_state not in self.visited:
            successors.append((a, new_state))
            self.visited.add(new_state)
        #print(successors)
        return successors

def main():
    searchers = [breadth_first_tree_search, breadth_first_graph_search, depth_first_graph_search,
                 iterative_deepening_search, depth_limited_search, 
                 greedy_best_first_graph_search, astar_search]
    problems =[MC()]
    for p in problems:
        for s in searchers:
            print("Solution to %s found by %s" % (p, s.__name__))
            path = s(MC()).path()
            path.reverse()
            print(path)
            print()

    print("SUMMARY: successors/goal tests/states generated/solution")
    compare_searchers(problems=problems, header=['', ''], searchers=searchers)

# if called from the command line, call main()
if __name__ == "__main__":
    main()
