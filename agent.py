import numpy as np
from network import Network
class Agent:
    def __init__(self,deterministic, learning_rate,discount_factor, exploration_rate):
        self.deterministic = deterministic
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.exploration_rate = exploration_rate
        self.move_probabilities = np.random.uniform(0,1,4)
        self.q_table = {}
    def updateQValue(self, state, action, next_state,reward, is_terminal):
        if next_state not in self.q_table:
            self.q_table[next_state] = {}
            self.q_table[next_state][0] = 0.0
            self.q_table[next_state][1] = 0.0
            self.q_table[next_state][2] = 0.0
            self.q_table[next_state][3] = 0.0
        if is_terminal:
            self.q_table[state][action] = self.q_table[state][action] + self.learning_rate * (reward - self.q_table[state][action])
        else:
            self.q_table[state][action] = self.q_table[state][action] + self.learning_rate * (reward + self.discount_factor * max(self.q_table[next_state].values()) - self.q_table[state][action])
    def takeActionFromPosition(self, position):
        if position not in self.q_table:
            self.q_table[position] = {}
            self.q_table[position][0] = 0.0
            self.q_table[position][1] = 0.0
            self.q_table[position][2] = 0.0
            self.q_table[position][3] = 0.0
        if np.random.uniform(0,1) < self.exploration_rate:
            action = np.random.choice([0,1,2,3])
        else:
            action = max(self.q_table[position],key=self.q_table[position].get)
        return action
    def __str__(self) -> str:
        return str(self.q_table)