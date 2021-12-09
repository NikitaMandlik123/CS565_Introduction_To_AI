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
        
def getActionSequence(backpointers, pos):
    actions = []
    temp = pos
    while backpointers.has_key(temp):
        actions.append(temp[1])
        temp = backpointers[temp]
    actions.reverse()
    #print actions
    #print closed
    return actions        


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    "*** YOUR CODE HERE ***"
    next = util.Stack()
    #already explored states
    expNodes = []
    #start node
    startState = problem.getStartState()
    startNode = (startState, [])
    
    next.push(startNode)
    
    while not next.isEmpty():
        # last node that is pushed on next
        currState, actions = next.pop()
        
        if currState not in expNodes:
            #mark current node as explored
            expNodes.append(currState)

            if problem.isGoalState(currState):
                return actions
            else:
                #list of successor nodes  
            
                successors = problem.getSuccessors(currState)
                
                #push each successor to frontier
                for succState, succAction, succCost in successors:
                    newAction = actions + [succAction]
                    newNode = (succState, newAction)
                    next.push(newNode)

    return actions  
    
  

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
      
    next = util.Queue()
    
    #previously expanded states 
    expNodes = []
    
    startState = problem.getStartState()
    startNode = (startState, [], 0) #(state, action, cost)
    
    next.push(startNode)
    
    while not next.isEmpty():
        #first pushed node on next
        currState, actions, currCost = next.pop()
        
        if currState not in expNodes:
            #popped node state into list
            expNodes.append(currState)

            if problem.isGoalState(currState):
                return actions
            else:
                #successor, action, stepCost
                successors = problem.getSuccessors(currState)
                
                for succState, succAction, succCost in successors:
                    newAction = actions + [succAction]
                    newCost = currCost + succCost
                    newNode = (succState, newAction, newCost)

                    next.push(newNode)

    return actions
    
    

    util.raiseNotDefined()

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    
    closed = []
    #define a fringe priority queue for ucs 
    fr = util.PriorityQueue()
    fr.push((problem.getStartState(), 'Start'), 0)
    start = problem.getStartState()
    actions = []
    backptrs = dict()
    while not fr.isEmpty():
        position = fr.pop()
        
        if problem.isGoalState(position[0]):
            actions = getActionSequence(backptrs, position)
            return actions
        else:
            if position[0] not in closed:
                closed.append(position[0])
                children = problem.getSuccessors(position[0])
                for child in children:
                    if child[0] not in closed:
                        backptrs[child] = position
                        actionSeq = getActionSequence(backptrs, child)
                        fr.push(child, problem.getCostOfActions(actionSeq))
    
    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    
    closed = []
    #define a fringe priority queue
    fr = util.PriorityQueue()
    fr.push((problem.getStartState(), 'Start'), 0)
    start = problem.getStartState()
    actions = []
    backptrs = dict()
    while not fr.isEmpty():
        position = fr.pop()
        
        if problem.isGoalState(position[0]):
            actions = getActionSequence(backptrs, position)
            return actions
        else:
            if position[0] not in closed:
                closed.append(position[0])
                children = problem.getSuccessors(position[0])
                for child in children:
                    if child[0] not in closed:
                        backptrs[child] = position
                        actionSeq = getActionSequence(backptrs, child)
                        fr.push(child, problem.getCostOfActions(actionSeq) + heuristic(child[0], problem))
    util.raiseNotDefined()
                       

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
