import random
from collections import deque

class ReplayBuffer:

    def __init__(self, capacity=10000):
        # Максимальный размер памяти
        self.memory = deque(maxlen=capacity)

    def add(self, state, action, reward, next_state, done):
        # Сохраняем один игровой опыт
        experience = (
            state,
            action,
            reward,
            next_state,
            done
        )

        self.memory.append(experience)

    def sample(self, batch_size):
        # Случайно выбираем несколько опытов
        return random.sample(self.memory, batch_size)

    def __len__(self):
        # Возвращаем количество сохранённых опытов
        return len(self.memory)

if __name__ == "__main__":

    replay = ReplayBuffer(capacity=10000)

    # Добавляем тестовые игровые ситуации
    for i in range(100):
        state = f"Состояние {i}"
        action = random.randint(0, 2)
        reward = 1
        next_state = f"Следующее состояние {i}"
        done = False

        replay.add(
            state,
            action,
            reward,
            next_state,
            done
        )

    print("Размер памяти:", len(replay))

    # Получаем 5 случайных опытов
    batch = replay.sample(5)

    print("Получено опытов:", len(batch))
    print("Пример опыта:", batch[0])

    print("Replay Buffer успешно работает!")