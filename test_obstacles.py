from dino_environment import DinoEnvironment
from dino_game_state import DinoGameState
import time

env = DinoEnvironment()

try:
    env.start()

    game_state = DinoGameState(env.page)

    print("\nНачинаем измерение скорости...\n")

    for i in range(100):
        state = game_state.get_state()

        speed = env.page.evaluate("""
            () => {
                const runner = window.Runner?.instance_;
                return runner ? runner.currentSpeed : null;
            }
        """)

        print(
            f"Шаг: {i + 1} | "
            f"Статус: {state['status']} | "
            f"Расстояние: {state.get('distance')} | "
            f"Препятствий: {state.get('obstacle_count')} | "
            f"Скорость: {speed}"
        )

        if state["status"] == "DEAD":
            print("\nДинозаврик столкнулся с препятствием!")
            break

        time.sleep(0.05)
finally:
    env.close()