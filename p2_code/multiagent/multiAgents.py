# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        return successorGameState.getScore()

def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        # number of agents
        n = gameState.getNumAgents()
        max_moves = n * self.depth

        def value(state, moves_made):
            # terminal layer
            if moves_made == max_moves:
                return scoreEvaluationFunction(state)

            agent_num = moves_made % n

            # max layer (i.e. agent number 0)
            """if agent_num == 0:
                v = -999999
                v_action = 9999 # SENTINEL

                if len(state.getLegalActions(agent_num)) > 0:
                    for action in state.getLegalActions(agent_num):
                        if v < self.evaluationFunction(state.generateSuccessor(agent_num, action)):
                            v = self.evaluationFunction(state.generateSuccessor(agent_num, action))
                            v_action = action

                    #print("pacman")
                    #print(action)
                    return value(state.generateSuccessor(agent_num, v_action), moves_made+1)
                # max layer (i.e. agent number 0)"""
            if agent_num == 0:
                v = -999999
                if len(state.getLegalActions(agent_num)) > 0:
                    for action in state.getLegalActions(agent_num):
                        v = max(v, value(state.generateSuccessor(agent_num, action), moves_made + 1))
                    return v

                # Terminal State
                else:
                    return scoreEvaluationFunction(state)
            # min layer
            else:
                """v = 999999
                v_action = 9999 # SENTINEL

                if len(state.getLegalActions(agent_num)) > 0:

                    for action in state.getLegalActions(agent_num):
                        if v > self.evaluationFunction(state.generateSuccessor(agent_num, action)):
                            v = self.evaluationFunction(state.generateSuccessor(agent_num, action))
                            v_action = action
                    #print("ghost")
                    #print(action)
                    return value(state.generateSuccessor(agent_num, v_action), moves_made + 1)"""

                if len(state.getLegalActions(agent_num)) > 0:
                    v = 999999
                    for action in state.getLegalActions(agent_num):
                        v = min(v, value(state.generateSuccessor(agent_num, action), moves_made + 1))
                    return v

                else:
                    #Terminal
                     return scoreEvaluationFunction(state)

        # for all the moves possible check values pick max
        val = -999999
        val_index = 0
        legal_actions = gameState.getLegalActions()

        if len(legal_actions) > 0:
            for i, action in enumerate(legal_actions):
                if value(gameState.generateSuccessor(0, action), 1) > val:
                      val = value(gameState.generateSuccessor(0, action), 1)
                      val_index = i
                #print "current action: " + str(legal_actions[i])
                #print "current value: " + str(value(gameState.generateSuccessor(0, action), 1))
                #print "global value: " + str(val)

            #print "FINAL ACTION: " + str(legal_actions[val_index])
            return legal_actions[val_index]
        else:
            #print "TERMINAL STATE"
            raise AttributeError()

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        # number of agents
        n = gameState.getNumAgents()
        max_moves = n * self.depth

        def value(state, moves_made, a, B):
            # terminal layer
            if moves_made == max_moves:
                return scoreEvaluationFunction(state)

            agent_num = moves_made % n

            # max layer (i.e. agent number 0)
            if agent_num == 0:
                v = -999999
                if len(state.getLegalActions(agent_num)) > 0:
                    for action in state.getLegalActions(agent_num):
                        v = max(v, value(state.generateSuccessor(agent_num, action), moves_made + 1, a, B))
                        if v > B:
                            return v
                        a = max(a, v)
                    return v

                # Terminal State
                else:
                    return scoreEvaluationFunction(state)
            # min layer
            else:
                v = 999999
                if len(state.getLegalActions(agent_num)) > 0:
                    for action in state.getLegalActions(agent_num):
                        v = min(v, value(state.generateSuccessor(agent_num, action), moves_made + 1, a, B))
                        if v < a:
                            return v
                        B = min(B, v)
                    return v

                else:
                    #Terminal
                    return scoreEvaluationFunction(state)

        # for all the moves possible check values pick max
        val = -999999
        val_index = 0
        legal_actions = gameState.getLegalActions()

        if len(legal_actions) > 0:
            for i, action in enumerate(legal_actions):
                action_val = value(gameState.generateSuccessor(0, action), 1, val, 999999)
                if action_val > val:
                      val = action_val
                      val_index = i
                #print "current action: " + str(legal_actions[i])
                #print "current value: " + str(value(gameState.generateSuccessor(0, action), 1))
                #print "global value: " + str(val)

            #print "FINAL ACTION: " + str(legal_actions[val_index])
            return legal_actions[val_index]
        else:
            #print "TERMINAL STATE"
            raise AttributeError()



class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """

        # number of agents
        n = gameState.getNumAgents()
        max_moves = n * self.depth

        def value(state, moves_made):
            # terminal layer
            if moves_made == max_moves:
                return scoreEvaluationFunction(state)

            agent_num = moves_made % n

            # max layer (Pacman)
            if agent_num == 0:
                v = -999999
                if len(state.getLegalActions(agent_num)) > 0:
                    for action in state.getLegalActions(agent_num):
                        v = max(v, value(state.generateSuccessor(agent_num, action), moves_made + 1))
                    return v
                # Terminal State
                else:
                    return scoreEvaluationFunction(state)

            # expectation layer (ghost)
            else:
                legal_actions = state.getLegalActions(agent_num)
                if len(legal_actions) > 0:

                    values = [value(state.generateSuccessor(agent_num, action), moves_made + 1) for action in legal_actions]
                    sum_vals = sum(values)
                    return (1.0 / float(len(legal_actions))) * float(sum_vals)

                else:
                    #Terminal
                     return scoreEvaluationFunction(state)

        # for all the moves possible check values pick max
        val = -999999
        val_index = 0
        legal_actions = gameState.getLegalActions()

        if len(legal_actions) > 0:
            for i, action in enumerate(legal_actions):
                if value(gameState.generateSuccessor(0, action), 1) > val:
                      val = value(gameState.generateSuccessor(0, action), 1)
                      val_index = i

            return legal_actions[val_index]
        else:
            #print "TERMINAL STATE"
            raise AttributeError()

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

