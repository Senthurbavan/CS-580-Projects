# valueIterationAgents.py
# -----------------------
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


# valueIterationAgents.py
# -----------------------
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


import mdp, util

from learningAgents import ValueEstimationAgent
import collections

class ValueIterationAgent(ValueEstimationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A ValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100):
        """
          Your value iteration agent should take an mdp on
          construction, run the indicated number of iterations
          and then act according to the resulting policy.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state, action, nextState)
              mdp.isTerminal(state)
        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter() # A Counter is a dict with default 0
        self.runValueIteration()

    def runValueIteration(self):
        # Write value iteration code here
        "*** YOUR CODE HERE ***"
        states = self.mdp.getStates()
        newvalues = util.Counter()
        for _ in range(self.iterations):
            for state in states:
                if self.mdp.isTerminal(state):
                    continue    # don't update, keep it 0 to be consistent
                actions = self.mdp.getPossibleActions(state)
                maxValue = -float("inf")
                for action in actions:
                    val = 0
                    nextStates = self.mdp.getTransitionStatesAndProbs(state, action)
                    for nextState, prob in nextStates:
                        r = self.mdp.getReward(state, action, nextState) + \
                            self.discount*self.values[nextState]
                        val += prob*r
                    maxValue = max(val, maxValue)
                newvalues[state] = maxValue
            self.values = newvalues.copy()


    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]


    def computeQValueFromValues(self, state, action):
        """
          Compute the Q-value of action in state from the
          value function stored in self.values.
        """
        "*** YOUR CODE HERE ***"
        qVal = 0
        nextStates = self.mdp.getTransitionStatesAndProbs(state, action)
        for nextState, prob in nextStates:
            r = self.mdp.getReward(state, action, nextState) + \
                self.discount * self.values[nextState]
            qVal += prob * r
        return qVal
        # util.raiseNotDefined()

    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        "*** YOUR CODE HERE ***"
        if self.mdp.isTerminal(state):
            return None
        actions = self.mdp.getPossibleActions(state)
        qValues = util.Counter()
        for action in actions:
            val = 0
            nextStates = self.mdp.getTransitionStatesAndProbs(state, action)
            for nextState, prob in nextStates:
                r = self.mdp.getReward(state, action, nextState) + \
                    self.discount * self.values[nextState]
                val += prob * r
            qValues[action] = val
        return qValues.argMax()
        # util.raiseNotDefined()

    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)

class AsynchronousValueIterationAgent(ValueIterationAgent):
    """
        * Please read learningAgents.py before reading this.*

        An AsynchronousValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs cyclic value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 1000):
        """
          Your cyclic value iteration agent should take an mdp on
          construction, run the indicated number of iterations,
          and then act according to the resulting policy. Each iteration
          updates the value of only one state, which cycles through
          the states list. If the chosen state is terminal, nothing
          happens in that iteration.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state)
              mdp.isTerminal(state)
        """
        ValueIterationAgent.__init__(self, mdp, discount, iterations)

    def runValueIteration(self):
        "*** YOUR CODE HERE ***"
        states = self.mdp.getStates()
        newvalues = util.Counter()
        for i in range(self.iterations):
            state = states[i % len(states)]
            if self.mdp.isTerminal(state):
                continue  # don't update, keep it 0 to be consistent
            actions = self.mdp.getPossibleActions(state)
            maxValue = -float("inf")
            for action in actions:
                val = 0
                nextStates = self.mdp.getTransitionStatesAndProbs(state, action)
                for nextState, prob in nextStates:
                    r = self.mdp.getReward(state, action, nextState) + \
                        self.discount * self.values[nextState]
                    val += prob * r
                maxValue = max(val, maxValue)
            self.values[state] = maxValue

class PrioritizedSweepingValueIterationAgent(AsynchronousValueIterationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A PrioritizedSweepingValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs prioritized sweeping value iteration
        for a given number of iterations using the supplied parameters.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100, theta = 1e-5):
        """
          Your prioritized sweeping value iteration agent should take an mdp on
          construction, run the indicated number of iterations,
          and then act according to the resulting policy.
        """
        self.theta = theta
        ValueIterationAgent.__init__(self, mdp, discount, iterations)

    def runValueIteration(self):
        "*** YOUR CODE HERE ***"
        states = self.mdp.getStates()
        predecessors = {}
        pq = util.PriorityQueue()
        for state in states:
            if self.mdp.isTerminal(state):
                continue
            actions = self.mdp.getPossibleActions(state)
            maxValue = -float("inf")
            for action in actions:
                val = 0
                for nextState, p in self.mdp.getTransitionStatesAndProbs(state, action):
                    if p > 0:
                        if nextState in predecessors:
                            predecessors[nextState].add(state)
                        else:
                            predecessors[nextState] = {state}
                    r = self.mdp.getReward(state, action, nextState) + \
                        self.discount * self.values[nextState]
                    val += p * r
                maxValue = max(val, maxValue)
            absDiff = abs(maxValue - self.values[state])
            pq.push(state, -absDiff)

        for i in range(self.iterations):
            if pq.isEmpty():
                break
            state = pq.pop()
            if self.mdp.isTerminal(state):
                continue  # don't update, keep it 0 to be consistent
            actions = self.mdp.getPossibleActions(state)
            maxValue = -float("inf")
            for action in actions:
                val = 0
                nextStates = self.mdp.getTransitionStatesAndProbs(state, action)
                for nextState, prob in nextStates:
                    r = self.mdp.getReward(state, action, nextState) + \
                        self.discount * self.values[nextState]
                    val += prob * r
                maxValue = max(val, maxValue)
            self.values[state] = maxValue
            for predState in predecessors[state]:
                actions = self.mdp.getPossibleActions(predState)
                maxValue = -float("inf")
                for action in actions:
                    val = 0
                    nextStates = self.mdp.getTransitionStatesAndProbs(predState, action)
                    for nextState, prob in nextStates:
                        r = self.mdp.getReward(predState, action, nextState) + \
                            self.discount * self.values[nextState]
                        val += prob * r
                    maxValue = max(val, maxValue)
                absDiff = abs(maxValue - self.values[predState])
                if absDiff > self.theta:
                    pq.update(predState, -absDiff)