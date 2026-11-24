import torch
import torch.nn as nn
import torch.optim as optim

from dino_target import DQNAgent
from dino_replay import ReplayBuffer

class DQNTrainer:

    def __init__(self, agent, replay_buffer):

        self.agent = agent
        self.replay_buffer = replay_buffer

        self.gamma = 0.99
        self.batch_size = 32

        # Функция измерения ошибки
        self.loss_function = nn.SmoothL1Loss()

        # Оптимизатор для изменения весов
        self.optimizer = optim.AdamW(
            self.agent.policy_net.parameters(),
            lr=0.0001
        )

    def train_step(self):

        # Проверяем, достаточно ли опыта
        if len(self.replay_buffer) < self.batch_size:
            return None

        # Получаем случайную выборку
        batch = self.replay_buffer.sample(self.batch_size)

        states, actions, rewards, next_states, dones = zip(*batch)

        # Преобразуем данные в тензоры
        states = torch.stack(states).to(self.agent.device)
        actions = torch.tensor(
            actions, dtype=torch.long, device=self.agent.device
        )
        rewards = torch.tensor(
            rewards, dtype=torch.float32, device=self.agent.device
        )
        next_states = torch.stack(next_states).to(self.agent.device)
        dones = torch.tensor(
            dones, dtype=torch.bool, device=self.agent.device
        )

        # Получаем оценки выбранных действий
        current_q = self.agent.policy_net(states)
        current_q = current_q.gather(
            1, actions.unsqueeze(1)
        ).squeeze(1)

        # Вычисляем целевые значения
        with torch.no_grad():
            next_q = self.agent.target_net(next_states).max(dim=1).values

            target_q = rewards + self.gamma * next_q * (~dones)

        # Вычисляем ошибку
        loss = self.loss_function(current_q, target_q)

        # Обновляем веса основной сети
        self.optimizer.zero_grad()
        loss.backward()

        torch.nn.utils.clip_grad_norm_(
            self.agent.policy_net.parameters(), 10.0
        )

        self.optimizer.step()

        return loss.item()
if __name__ == "__main__":

    device = torch.device(
        "cuda" if torch.cuda.is_available() else "cpu"
    )

    agent = DQNAgent(device)
    replay = ReplayBuffer(capacity=10000)

    trainer = DQNTrainer(agent, replay)

    # Создаём 100 тестовых игровых ситуаций
    for i in range(100):

        state = torch.rand(1, 84, 84)
        next_state = torch.rand(1, 84, 84)

        action = i % 3
        reward = 1.0
        done = False

        replay.add(
            state,
            action,
            reward,
            next_state,
            done
        )

    print("Устройство:", device)
    print("Размер памяти:", len(replay))

    # Выполняем один шаг обучения
    loss = trainer.train_step()

    print("Ошибка обучения:", loss)
    print("DQN успешно обучилась на тестовых данных!")