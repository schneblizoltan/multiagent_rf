""" SARSA-Agent module """

import numpy as np
import random

class SarsaAgent(object):
    """
    Agent implementing SARSA algorithm.
    """

    def __init__(self, observation_space, state_n, action_n, dist_file_name, reward_file_name):
        self.obs = observation_space
        self.state_n = state_n
        self.action_n = action_n
        self.location_distance = dist_file_name
        self.location_reward = reward_file_name
        self.q = np.zeros((self.state_n, self.action_n)).astype("float32")
        self.state = 0
        self.action = 0
        self.distance = 0
        self.cumulative_reward = 0
        self.config = {
            "alpha" : 10**-6,                                                                       # Learning rate
            "eps": 1.0,                                                                             # Exploration rate
            "eps_decay": 0.995,                                                                     # Speed of epsilon decay
            "eps_min": 0.01,         
            "gamma": 0.95,                                                                          # Discount
            "n_iter": 20000 }                                                                       # Number of iterations
        
    def act(self, eps=None):
        if eps is None:
            eps = self.config["eps"]
        
        if np.random.rand() <= eps:                                                                 # epsilon greedy
            return self.action_sample()
        else:
            return np.argmax(self.q[self.state])
        
    def get_action(self, state, eps=None):
        if eps is None:
            eps = self.config["eps"]
        
        if np.random.rand() <= eps:                                                                 # epsilon greedy
            return self.action_sample()
        else:
            return np.argmax(self.q[state])
        
    def action_sample(self):
        return random.randrange(self.action_n)

    def learn(self, env):
        open(self.location_distance, 'w').close()
        open(self.location_reward, 'w').close()
        
        for t in range(self.config["n_iter"]):
            self.distance = 0
            self.cumulative_reward = 0
            self.obs = env.reset()
            self.state = env.get_state(self.obs)
            self.action = self.act()
            done = False
        
            while not done:
                obs2, reward, done, coordinates = env.step(self.action, self.obs)
                
                self.cumulative_reward += reward

                state2 = env.get_state(obs2)
                action2 = self.get_action(state2)

                if self.distance < coordinates[1]:
                    self.distance = coordinates[1]
                
                open('q_matrix_sarsa.txt', 'w').close()
                np.savetxt('q_matrix_sarsa.txt', self.q, fmt='%10.3f')

                self.update_q(self.state, self.action, state2, action2, reward)

                self.state = state2
                self.action = action2
                self.obs = obs2
            
            if self.config["eps"] > self.config["eps_min"]:
                self.config["eps"] *= self.config["eps_decay"]

            with open(self.location_distance, 'a') as out:
                out.write(str(self.distance) + '\n')
                
            with open(self.location_reward, 'a') as out:
                out.write(str(self.cumulative_reward) + '\n')  
            
    def update_q(self, state, action, state2, action2, reward):
        self.q[self.state, action] += self.config["alpha"] * (reward + self.config["gamma"] * self.q[state2][action2] - self.q[self.state, action])

        # renormalize row to be between 0 and 1 => doesn't help
        # rn = self.q[self.state][self.q[self.state] > 0] / np.sum(self.q[self.state][self.q[self.state] > 0])
        # self.q[self.state][self.q[self.state] > 0] = rn