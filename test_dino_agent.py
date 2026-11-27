import time

from dino_environment import DinoEnvironment
from dino_agent import DinoAgent

env = DinoEnvironment()

try:
    env.start()

    agent = DinoAgent(env)

    print("DinoAI подключена!")
    print("Начинаем тестирование...")

    for step in range(10):
        observation = env.get_observation()

        action = agent.act(observation)

        print(
            f"Шаг: {step + 1} | "
            f"Действие: {action}"
        )

        time.sleep(0.5)

    agent.actions.release_all()

    print("Тест DinoAI завершён!")

    input("Нажми Enter для закрытия...")
finally:
    env.close()