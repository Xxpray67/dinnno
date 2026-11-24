import torch
import torch.nn as nn

class DinoCNN(nn.Module):

    def __init__(self):
        super().__init__()

        self.network = nn.Sequential(

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

    def forward(self, x):
        return self.network(x)
if __name__ == "__main__":
        device = torch.device(
        "cuda" if torch.cuda.is_available() else "cpu"
)

model = DinoCNN().to(device)

# Создаём тестовое изображение
test_image = torch.rand(
    1, 1, 84, 84
).to(device)

# Передаём изображение в CNN
features = model(test_image)

print("Устройство:", device)
print("Вход:", test_image.shape)
print("Выход CNN:", features.shape)

print("CNN успешно работает!")