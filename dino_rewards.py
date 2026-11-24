class DinoRewards:
    def __init__(self):
        self.survival_reward = 1.0
        self.collision_penalty = -10.0
        self.obstacle_reward = 5.0

    def calculate(self, game_over, obstacle_passed=False):
        if game_over:
            return self.collision_penalty

        reward = self.survival_reward

        if obstacle_passed:
            reward += self.obstacle_reward

        return reward