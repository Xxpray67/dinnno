import random
import torch

from dino_brain import DinoBrain
from dino_actions import DinoActions

class DinoAgent:
    def __init__(self, env):
        self.env = env
        self.device = env.device

        self.brain = DinoBrain().to(self.device)
        self.actions = DinoActions(env.page)

        self.epsilon = 1.0

    def choose_action(self, observation):
        if random.random() < self.epsilon:
            return random.randrange(3)

        with torch.no_grad():
            q_values = self.brain(
                observation.unsqueeze(0)
            )

        return q_values.argmax(dim=1).item()

    def act(self, observation):
        action = self.choose_action(observation)
        self.actions.perform(action)

        return action