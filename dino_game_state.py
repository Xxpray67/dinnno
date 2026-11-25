class DinoGameState:

    def __init__(self, page):
        self.page = page

    def get_state(self):

        return self.page.evaluate("""
            () => {
                const runner = window.Runner?.instance_;

                if (!runner) {
                    return {status: "NO_RUNNER"};
                }

                if (runner.crashed) {
                    return {status: "DEAD"};
                }

                if (!runner.playing) {
                    return {status: "NOT_PLAYING"};
                }

                const dino = runner.tRex;
                const obstacles = runner.horizon?.obstacles || [];

                return {
                    status: "OK",

                    obstacles: obstacles.map(obstacle => ({
                        type: obstacle.typeConfig?.type ?? null,
                        distance: obstacle.xPos - dino.xPos,
                        y: obstacle.yPos,
                        width: obstacle.width
                    })),

                    dino_y: dino.yPos,
                    jumping: !!dino.jumping,
                    ducking: !!dino.ducking,
                    speed: runner.currentSpeed
                };
            }
        """)

    def is_game_over(self):
        return self.get_state()["status"] == "DEAD"