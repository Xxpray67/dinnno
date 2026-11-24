import torch
import torch.nn as nn

class DinoBrain(nn.Module):

    def __init__(self, num_actions=3):
        super().__init__()

    # Часть 1. CNN извлекает признаки изображения
        self.cnn = nn.Sequential(
            nn.Conv2d(1, 32, kernel_size=8, stride=4),
            nn.ReLU(),

            nn.Conv2d(32, 64, kernel_size=4, stride=2),
            nn.ReLU(),

            nn.Conv2d(64, 64, kernel_size=3, stride=1),
            nn.ReLU(),

            nn.Flatten(),

            nn.Linear(64 * 7 * 7, 512),
            nn.ReLU()
        )

    # Часть 2. DQN оценивает действия
        self.dqn = nn.Sequential(
            nn.Linear(512, 256),
            nn.ReLU(),

            nn.Linear(256, 128),
            nn.ReLU(),

            nn.Linear(128, num_actions)
        )

    def forward(self, x):
        features = self.cnn(x)
        q_values = self.dqn(features)

        return q_values
if __name__ == "__main__":

    device = torch.device(
        "cuda" if torch.cuda.is_available() else "cpu"
    )

    model = DinoBrain().to(device)

    # Создаём тестовое изображение
    test_image = torch.rand(1, 1, 84, 84).to(device)

    # Передаём изображение через всю нейросеть
    q_values = model(test_image)

    print("Устройство:", device)
    print("Входное изображение:", test_image.shape)
    print("Выходные оценки:", q_values.shape)
    print("Оценки действий:", q_values)

    print("CNN + DQN успешно объединены!")