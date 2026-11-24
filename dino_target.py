import torch
import torch.nn as nn

from dino_brain import DinoBrain

class DQNAgent:

    def __init__(self, device):

        self.device = device

        # Основная нейросеть
        self.policy_net = DinoBrain().to(device)

        # Целевая нейросеть
        self.target_net = DinoBrain().to(device)

        # Копируем веса основной сети
        self.target_net.load_state_dict(
            self.policy_net.state_dict()
        )

        # Отключаем обучение целевой сети
        self.target_net.eval()

    def update_target_network(self):

        self.target_net.load_state_dict(
            self.policy_net.state_dict()
        )
if __name__ == "__main__":

    device = torch.device(
        "cuda" if torch.cuda.is_available() else "cpu"
    )

    agent = DQNAgent(device)

    print("Устройство:", device)

    print(
        "Policy Network:",
        sum(p.numel() for p in agent.policy_net.parameters())
    )

    print(
        "Target Network:",
        sum(p.numel() for p in agent.target_net.parameters())
    )

    print("Target Network успешно создана!")