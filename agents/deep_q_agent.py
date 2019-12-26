""" Deep Q-Agent module """

import numpy as np
import random

from collections import deque
from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.optimizers import RMSprop
from keras.utils.vis_utils import plot_model

class DeepQAgent(object):
    """
    Agent implementing DeepQ-learning algorithm.
    """

    def __init__(self, observation_space, state_n, action_n, dist_file_name, reward_file_name):
        self.obs = observation_space
        self.state_n = state_n
        self.action_n = action_n
        self.location_distance = dist_file_name
        self.location_reward = reward_file_name
        self.memory = deque(maxlen=55000)
        self.state = 0
        self.distance = 0
        self.cumulative_reward = 0
        self.config = {
            "alpha" : 10**-6,                                                               # Learning rate
            "eps": 1.0,                                                                     # Exploration rate
            "eps_decay": 0.995,                                                             # Speed of epsilon decay
            "eps_min": 0.01,         
            "gamma": 0.95,                                                                  # Discount
            "batch_size": 8192,      
            "n_iter": 50000 }                                                               # Number of iterations
        self.model = self._create_model() 
        plot_model(self.model, to_file='model.png')
        print(self.model.summary())

    def _create_model(self):
        model = Sequential()

        model.add(Dense(128, activation='relu', input_dim=self.state_n))
        model.add(Dropout(0.1))
        model.add(Dense(128, activation='relu'))
        model.add(Dropout(0.1))
        model.add(Dense(128, activation='relu'))
        model.add(Dropout(0.1))
        model.add(Dense(units=self.action_n, activation='linear'))

        opt = RMSprop(lr=self.config["alpha"])
        model.compile(loss='mse', optimizer=opt)
        return model

    def save(self):
        self.model.save("model.h5")

    def train(self, x, y, epoch=1, verbose=0):
        self.model.fit(x, y, batch_size=self.config["batch_size"], epochs=epoch, verbose=verbose)

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

        if len(self.memory) > self.memory.maxlen:
            self.memory.pop(0)

    def memory_sample(self, n):
        n = min(n, len(self.memory))
        return random.sample(list(self.memory), n)

    def act(self, eps=None):
        if eps is None:
            eps = self.config["eps"]
        
        if np.random.rand() <= eps:                                                         # epsilon greedy
            return self.action_sample()
        else:
            act_values = self.model.predict(self.state)
            return np.argmax(act_values[0])
            
    def action_sample(self):
        return random.randrange(self.action_n)

    def replay(self, batch_size):
        batch = self.memory_sample(batch_size)
        batch_len = len(batch)

        no_state = []
        no_state.append(np.zeros(self.state_n))

        states = np.array([ o[0] for o in batch ])                                          # all states
        states_ = np.array([ (no_state if o[4] is True else o[3]) for o in batch ])         # end states

        states = states.reshape(batch_len, self.state_n)                                    # reshape to batch_size*state_number format
        states_ = states_.reshape(batch_len, self.state_n)                                  # reshape to batch_size*state_number format

        p = self.model.predict(states)                                                      # value of each action for the states
        p_ = self.model.predict(states_)                                                    # value of each action for the end states
    
        x = np.zeros((batch_len, self.state_n))                                             # results
        y = np.zeros((batch_len, self.action_n))                                            # results

        for i in range(batch_len):                                                          # replay from memory
            o = batch[i]
            s = o[0]; a = o[1]; r = o[2]; s_ = o[3]; d = o[4]
            
            t = p[i]                                                                        # result from a given state
            if d is True:   
                t[a] = r                                                                    # at the end of episode we get the full reward
            else:
                t[a] = r + self.config['gamma'] * np.amax(p_[i])                            # we get only learning_rate*reward

            x[i] = s
            y[i] = t

        self.train(x, y)

        if self.config["eps"] > self.config["eps_min"]:
            self.config["eps"] *= self.config["eps_decay"]


    def learn(self, env):
        open(self.location_distance, 'w').close()
        open(self.location_reward, 'w').close()

        for t in range(self.config["n_iter"]):
            self.obs = env.reset()
            self.distance = 0
            self.cumulative_reward = 0

            state = env.get_state(self.obs)
            states = np.zeros(self.state_n)
            states[state] = 1
            self.state = states
            self.state = np.reshape(self.state, [1, self.state_n])
            
            done = False
            while not done:
                action = self.act()
                obs2, reward, done, coordinates = env.step(action, self.obs)
                
                self.cumulative_reward += reward

                nextstate = env.get_state(obs2)
                states = np.zeros(self.state_n)
                states[nextstate] = 1
                next_state = states
                next_state = np.reshape(next_state, [1, self.state_n])

                self.remember(self.state, action, reward, next_state, done)
                
                if self.distance < coordinates[1]:
                    self.distance = coordinates[1]

                self.state = next_state
                self.obs = obs2
    
            with open(self.location_distance, 'a') as out:
                out.write(str(self.distance) + '\n')
                
            with open(self.location_reward, 'a') as out:
                out.write(str(self.cumulative_reward) + '\n')  

            if len(self.memory) > self.config["batch_size"]:
                self.replay(self.config["batch_size"])
            