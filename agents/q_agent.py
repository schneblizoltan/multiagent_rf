""" Q-Agent module """

import numpy as np
import random
from agents.Agent import Agent

class QAgent(Agent):
    """
    Agent implementing Q-learning algorithm.
    """

    def __init__(self, id, curX, curY, state_n, action_n):
        super().__init__(id, curX, curY)
        self.state_n = state_n
        self.action_n = action_n
        self.q = np.zeros((self.state_n, self.action_n)).astype("float32")
        self.state = 0
        self.cumulative_reward = 0
        self.config = {
            "alpha" : 0.01,                                                                 # Learning rate
            "eps": 0.1,                                                                     # Exploration rate
            "eps_decay": 0.995,                                                             # Speed of epsilon decay
            "eps_min": 0.01,         
            "gamma": 0.95 }                                                               # Number of iterations
        self.q_matrix_name = "q_matrix_" + str(self.id)
        
    def load_from_file(self, file):
        i = 0
        print(self.q)
        for line in open(file):
            self.q[i] = np.fromstring(line, dtype="float32", sep="     ")
            i += 1

    def act(self, eps=None):
        if eps is None:
            eps = self.config["eps"]
        
        if np.random.rand() < eps:                                                          # epsilon greedy
            return self.action_sample()
        elif np.sum(self.q[self.state]) > 0:
            return np.argmax(self.q[self.state])
        else:
            return self.action_sample()
            
    def action_sample(self):
        return random.randrange(self.action_n)

    def update_eps(self):
        if self.config["eps"] > self.config["eps_min"]:
                self.config["eps"] *= self.config["eps_decay"]
            
    def update_q(self, future, action, reward):
        self.q[self.state, action] *= 1 - self.config["alpha"]
        self.q[self.state, action] += self.config["alpha"] * (reward + self.config["gamma"] * future)
        
        # renormalize row to be between 0 and 1 => doesn't help
        # rn = self.q[self.state][self.q[self.state] > 0] / np.sum(self.q[self.state][self.q[self.state] > 0])
        # self.q[self.state][self.q[self.state] > 0] = rn
    
    def step(self, env):
        self.state = env.getState(self.id)
        action = self.act()
        reward, done = env.step(self.id, action)
        
        self.cumulative_reward += reward
        
        open(self.q_matrix_name, 'w').close()
        np.savetxt(self.q_matrix_name, self.q, fmt='%10.3f')

        future_reward = 0.0
        next_state = env.getState(self.id)
        if not done:
            future_reward = np.max(self.q[next_state])

        self.update_q(future_reward, action, reward)
