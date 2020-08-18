""" SARSA-Agent module """

import numpy as np
import random
from agents.Agent import Agent

class SarsaAgent(Agent):
    """
    Agent implementing SARSA algorithm.
    """

    def __init__(self, id, curX, curY, state_n, action_n):
        super().__init__(id, curX, curY)
        self.state_n = state_n
        self.action_n = action_n
        self.q = np.zeros((self.state_n, self.action_n)).astype("float32")
        self.state = 0
        self.action = 0
        self.cumulative_reward = 0
        self.config = {
            "alpha" : 10**-6,                                                                       # Learning rate
            "eps": 1.0,                                                                             # Exploration rate
            "eps_decay": 0.995,                                                                     # Speed of epsilon decay
            "eps_min": 0.1,         
            "gamma": 0.95 }                                                                         # Number of iterations
        self.q_matrix_name = "q_matrix_" + str(self.id)
        
    def act(self, eps=None):
        if eps is None:
            eps = self.config["eps"]
        
        if np.random.rand() <= eps:                                                                 # epsilon greedy
            return self.action_sample()
        elif np.sum(self.q[self.state]) > 0:
            return np.argmax(self.q[self.state])
        else:
            return self.action_sample()
        
    def get_action(self, state, eps=None):
        if eps is None:
            eps = self.config["eps"]
        
        if np.random.rand() <= eps:                                                                 # epsilon greedy
            return self.action_sample()
        else:
            return np.argmax(self.q[state])
        
    def action_sample(self):
        return random.randrange(self.action_n)

    def update_eps(self):
        if self.config["eps"] > self.config["eps_min"]:
                self.config["eps"] *= self.config["eps_decay"]

    def update_q(self, state, action, state2, action2, reward):
        self.q[self.state, action] += self.config["alpha"] * (reward + self.config["gamma"] * self.q[state2][action2] - self.q[self.state, action])

        # renormalize row to be between 0 and 1 => doesn't help
        # rn = self.q[self.state][self.q[self.state] > 0] / np.sum(self.q[self.state][self.q[self.state] > 0])
        # self.q[self.state][self.q[self.state] > 0] = rn

    def step(self, env):
        self.state = env.getState(self.id)
        self.action = self.act()

        reward, done = env.step(self.id, self.state, self.action)
        
        self.cumulative_reward += reward

        state2 = env.getState(self.id)
        action2 = self.get_action(state2)
        
        open(self.q_matrix_name, 'w').close()
        np.savetxt(self.q_matrix_name, self.q, fmt='%10.3f')

        self.update_q(self.state, self.action, state2, action2, reward)

        self.state = state2
        self.action = action2
