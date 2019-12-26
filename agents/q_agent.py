""" Q-Agent module """

import numpy as np
import random

class QAgent(object):
    """
    Agent implementing Q-learning algorithm.
    """

    def __init__(self, observation_space, state_n, action_n, dist_file_name, reward_file_name):
        self.obs = observation_space
        self.state_n = state_n
        self.action_n = action_n
        self.location_distance = dist_file_name
        self.location_reward = reward_file_name
        self.q = np.zeros((self.state_n, self.action_n)).astype("float32")
        self.state = 0
        self.load_from_file('q_matrix.txt')
        self.distance = 0
        self.cumulative_reward = 0
        self.config = {
            "alpha" : 0.01,                                                                 # Learning rate
            "eps": 0.1,                                                                     # Exploration rate
            "eps_decay": 0.995,                                                             # Speed of epsilon decay
            "eps_min": 0.1,         
            "gamma": 0.95,                                                                  # Discount
            "n_iter": 15000 }                                                               # Number of iterations

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

    def learn(self, env):
        open(self.location_distance, 'w').close()
        open(self.location_reward, 'w').close()
        
        for t in range(self.config["n_iter"]):
            self.distance = 0
            self.cumulative_reward = 0
            self.obs = env.reset()
            self.state = env.get_state(self.obs)
            done = False
            
            while not done:
                action = self.act()
                obs2, reward, done, coordinates = env.step(action, self.obs)
                
                self.cumulative_reward += reward

                if self.distance < coordinates[1]:
                    self.distance = coordinates[1]
                
                open('q_matrix.txt', 'w').close()
                np.savetxt('q_matrix.txt', self.q, fmt='%10.3f')

                future_reward = 0.0
                next_state = env.get_state(obs2)
                if not done:
                    future_reward = np.max(self.q[next_state])

                self.update_q(future_reward, action, reward)

                self.state = next_state
                self.obs = obs2
            
            if self.config["eps"] > self.config["eps_min"]:
                self.config["eps"] *= self.config["eps_decay"]

            with open(self.location_distance, 'a') as out:
                out.write(str(self.distance) + '\n')    
            with open(self.location_reward, 'a') as out:
                out.write(str(self.cumulative_reward) + '\n')    
            
    def update_q(self, future, action, reward):
        self.q[self.state, action] *= 1 - self.config["alpha"]
        self.q[self.state, action] += self.config["alpha"] * (reward + self.config["gamma"] * future)
        
        # renormalize row to be between 0 and 1 => doesn't help
        # rn = self.q[self.state][self.q[self.state] > 0] / np.sum(self.q[self.state][self.q[self.state] > 0])
        # self.q[self.state][self.q[self.state] > 0] = rn
