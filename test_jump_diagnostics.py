from dino_environment import DinoEnvironment
import time

env = DinoEnvironment()

try:
    env.start()

    previous_distance = 1000
    jump_count = 0

    for i in range(400):
        state = env.page.evaluate("""
            () => {
                const runner = window.Runner?.instance_;

                if (!runner) {
                    return {status: "NO_RUNNER"};
                }

                const dino = runner.tRex;
                const obstacles = runner.horizon?.obstacles || [];
                const obstacle = obstacles[0];

                return {
                    status: runner.crashed ? "DEAD" : "OK",
                    distance: obstacle
                        ? obstacle.xPos - dino.xPos
                        : 1000,
                    width: obstacle?.width ?? null,
                    type: obstacle?.typeConfig?.type ?? null,
                    dino_y: dino.yPos,
                    jumping: !!dino.jumping,
                    ducking: !!dino.ducking
                };
            }
        """)

        if state["status"] == "DEAD":
            print("СТОЛКНОВЕНИЕ:", state)
            break

        distance = state["distance"]

        if state["type"] == "CACTUS_LARGE":
            jump_distance = 120
        else:
            jump_distance = 200

        if (
            previous_distance > jump_distance
            and distance <= jump_distance
        ):
            env.page.keyboard.press("Space")
            jump_count += 1

            print(
                f"\n>>> ПРЫЖОК №{jump_count} "
                f"| Тип: {state['type']} "
                f"| Расстояние: {distance}"
            )

        if distance <= 300:
            print(
                f"Шаг {i + 1} | "
                f"Тип: {state['type']} | "
                f"Ширина: {state['width']} | "
                f"Расстояние: {distance} | "
                f"Высота динозавра: {state['dino_y']} | "
                f"Прыгает: {state['jumping']}"
            )

        previous_distance = distance
        time.sleep(0.05)

    print("\nВсего прыжков:", jump_count)
finally:
    env.close()