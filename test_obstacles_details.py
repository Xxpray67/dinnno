from dino_environment import DinoEnvironment
import time

env = DinoEnvironment()

try:
    env.start()

    for i in range(20):
        state = env.page.evaluate("""
            () => {
                const runner = window.Runner?.instance_;

                if (!runner) {
                    return {status: "NO_RUNNER"};
                }

                const obstacles = runner.horizon?.obstacles || [];

                return {
                    status: runner.crashed ? "DEAD" : "OK",
                    dino_x: runner.tRex.xPos,
                    obstacles: obstacles.map(o => ({
                        x: o.xPos,
                        y: o.yPos,
                        width: o.width,
                        type: o.typeConfig?.type
                    }))
                };
            }
        """)

        print(f"Шаг {i + 1}: {state}")
        time.sleep(0.3)
finally:
    env.close()