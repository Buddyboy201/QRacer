from environment import Environment
import gym
from gym import error, spaces, utils
from gym.utils import seeding
import numpy as np

class RacerEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self):
        super(RacerEnv, self).__init__()
        self.env = None
        self.action_space = spaces.Discrete(7)
        self.observation_space = spaces.Box(low=np.array([0, 0, 0, 0]), high=np.array([1000, 1000, 1000, 1000]),
                                            dtype=np.float64)
        self.frames = 0

    def 


