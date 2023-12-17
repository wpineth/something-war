from agent import *
import time
import math
import random
import game as g
import copy


class AIAgent(Agent):
    def decide_action(self, gametosearch: g.Game):
        actiontotake = mcts(timeLimit=1000).search(gametosearch, needDetails=True)
        return actiontotake


# Some of the following code taken from the MCTS.py package on PyPi


def randomPolicy(game2):
    game = copy.deepcopy(game2)
    while not game.is_terminal():
        try:
            action = random.choice(game.get_possible_actions())
        except IndexError:
            raise Exception("Non-terminal game has no possible actions: " + str(game))
        try:
            game.take_action(action)
        except Exception as e:
            print("oops, threw an exception!")
            print(e.args[0])
            game.print_board()
            game.print_sideboard()
            print(action.action_type)
            print(action.space)
            print(action.heading)
            print(action.piece_type)
            raise Exception(e)
    return game.get_reward()


class treeNode:
    def __init__(self, game, parent):
        self.game = game
        self.is_terminal = game.is_terminal()
        self.isFullyExpanded = self.is_terminal
        self.parent = parent
        self.numVisits = 0
        self.totalReward = 0
        self.children = {}

    def __str__(self):
        s=[]
        s.append("totalReward: %s"%(self.totalReward))
        s.append("numVisits: %d"%(self.numVisits))
        s.append("is_terminal: %s"%(self.is_terminal))
        s.append("possibleActions: %s"%(self.children.keys()))
        return "%s: {%s}"%(self.__class__.__name__, ', '.join(s))

class mcts():
    def __init__(self, timeLimit=None, iterationLimit=None, explorationConstant=1 / math.sqrt(2),
                 rolloutPolicy=randomPolicy):
        if timeLimit != None:
            if iterationLimit is not None:
                raise ValueError("Cannot have both a time limit and an iteration limit")
            # time taken for each MCTS search in milliseconds
            self.timeLimit = timeLimit
            self.limitType = 'time'
        else:
            if iterationLimit is None:
                raise ValueError("Must have either a time limit or an iteration limit")
            # number of iterations of the search
            if iterationLimit < 1:
                raise ValueError("Iteration limit must be greater than one")
            self.searchLimit = iterationLimit
            self.limitType = 'iterations'
        self.explorationConstant = explorationConstant
        self.rollout = rolloutPolicy

    def search(self, initialgame, needDetails=False):
        self.root = treeNode(copy.deepcopy(initialgame), None)

        if self.limitType == 'time':
            timeLimit = time.time() + self.timeLimit / 1000
            while time.time() < timeLimit:
                self.executeRound()
        else:
            for i in range(self.searchLimit):
                self.executeRound()

        bestChild = self.getBestChild(self.root, 0)
        action = (action for action, node in self.root.children.items() if node is bestChild).__next__()
        if needDetails:
            print("action: ", str(action), "expectedReward:", str(bestChild.totalReward / bestChild.numVisits))
        return action

    def executeRound(self):
        # execute a selection-expansion-simulation-backpropagation round
        node = self.selectNode(self.root)
        reward = self.rollout(node.game)
        self.backpropagate(node, reward)

    def selectNode(self, node):
        while not node.is_terminal:
            if node.isFullyExpanded:
                node = self.getBestChild(node, self.explorationConstant)
            else:
                return self.expand(node)
        return node

    def expand(self, node):
        actions = node.game.get_possible_actions()
        for action in actions:
            if action not in node.children:
                newNode = treeNode(copy.deepcopy(node.game), node)
                newNode.game.take_action(action)
                node.children[action] = newNode
                if len(actions) == len(node.children):
                    node.isFullyExpanded = True
                return newNode
        raise Exception("Should never reach here")

    def backpropagate(self, node, reward):
        while node is not None:
            node.numVisits += 1
            node.totalReward += reward
            node = node.parent

    def getBestChild(self, node, explorationValue):
        bestValue = float("-inf")
        bestNodes = []
        for child in node.children.values():
            nodeValue = node.game.get_player_to_move() * child.totalReward / child.numVisits + explorationValue * math.sqrt(
                2 * math.log(node.numVisits) / child.numVisits)
            if nodeValue > bestValue:
                bestValue = nodeValue
                bestNodes = [child]
            elif nodeValue == bestValue:
                bestNodes.append(child)
        return random.choice(bestNodes)
