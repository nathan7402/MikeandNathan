# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

# generic search function based on graph search pseudocode from lecture
def genericSearch(problem, empty_fringe):

    # intitalize fringe
    # NOTE: fringe stored as tuples of xy state, path (direction list), & cost
    fringe = empty_fringe
    start = problem.getStartState()
    fringe.push((start, [], 0))

    # initialize empty set of visited nodes
    visited = set()

    while True:
        if fringe.isEmpty():
            print "Empty fringe!"
            util.raiseNotDefined()

        # expand next node in fringe
        node = fringe.pop()
        # define a position variable?
        # if node[0] is tuple tuple then pos = node[0][0]
        # else pos = node[0]

        # if node contains goal state, return directions to that solution
        if problem.isGoalState(node[0]):
            return node[1]

        # if node hasn't been visited
        # if node[0] is not a tuple just add it
        # else add node[0][0]
        if node[0] not in visited:
            # add to visited set
            visited.add(node[0])

            # add children to fringe
            for item in problem.getSuccessors(node[0]):
                # copy existing directions and add latest direction
                old_dirs = node[1][:]
                old_dirs.append(item[1])

                # add state, path, & updated cost as new element in fringe
                fringe.push((item[0], old_dirs, node[2] + item[2]))

def depthFirstSearch(problem):
    # generic search using LIFO Stack as fringe
    fringe = util.Stack()
    return genericSearch(problem, fringe)

def breadthFirstSearch(problem):
    # generic search using FIFO Queue as fringe
    fringe = util.Queue()
    return genericSearch(problem, fringe)

def uniformCostSearch(problem):
    def assignPriority(item):
        return item[2]

    fringe = util.PriorityQueueWithFunction(assignPriority)
    return genericSearch(problem, fringe)

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    def assignPriority(item):
        return item[2] + heuristic(item[0], problem)

    fringe = util.PriorityQueueWithFunction(assignPriority)
    return genericSearch(problem, fringe)


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
