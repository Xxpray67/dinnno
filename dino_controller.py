import time

from dino_game_state import DinoGameState
from dino_actions import DinoActions

class DinoController:

    def __init__(self, page):
        self.game_state = DinoGameState(page)
        self.actions = DinoActions(page)

        self.handled_obstacle = None
        self.ducking = False
        self.jump_started = False
        self.last_action_time = 0

    def update(self):

        state = self.game_state.get_state()

        if state["status"] != "OK":
            self.actions.release_all()
            self.ducking = False
            return state["status"]

        obstacles = state["obstacles"]
        speed = max(state["speed"], 1)

        # Проверяем, продолжается ли прыжок
        if state["jumping"]:
            self.jump_started = True
        elif self.jump_started:
            self.jump_started = False
            self.handled_obstacle = None

        # Продолжаем приседание под средней птицей
        if self.ducking:

            birds = [
                obstacle for obstacle in obstacles
                if obstacle["type"] == "PTERODACTYL"
                and obstacle["y"] == 75
            ]

            if birds:
                bird = min(
                    birds,
                    key=lambda item: abs(item["distance"])
                )

                bird_end = bird["distance"] + bird["width"]

                if bird_end > 0:
                    self.actions.perform(2)
                    return f"DUCKING | До конца птицы: {bird_end:.1f}"

            self.actions.release_all()
            self.ducking = False
            self.handled_obstacle = None

            return "BIRD PASSED | RUN"

        # Выбираем ближайшее препятствие
        upcoming = [
            obstacle for obstacle in obstacles
            if obstacle["distance"] > 0
        ]

        if not upcoming:
            self.actions.release_all()
            self.handled_obstacle = None
            return "RUN"

        obstacle = min(
            upcoming,
            key=lambda item: item["distance"]
        )

        distance = obstacle["distance"]
        width = obstacle["width"]
        obstacle_type = obstacle["type"]
        y = obstacle["y"]

        # Рассчитываем расстояние реакции с учётом скорости
        reaction_distance = max(170, speed * 16)

        if distance > reaction_distance:
            return "WAIT"

        # Не повторяем действие для того же препятствия
        obstacle_id = (
            obstacle_type,
            y,
            round(distance + width)
        )

        if self.handled_obstacle is not None:
            return "OBSTACLE ALREADY HANDLED"

        # Средняя птица
        if obstacle_type == "PTERODACTYL" and y == 75:

            self.actions.perform(2)
            self.ducking = True
            self.handled_obstacle = obstacle_id

            return f"DUCK START | Distance: {distance:.1f}"

        # Низкая птица и кактусы
        if obstacle_type == "PTERODACTYL" and y == 100:
            action = 1

        elif obstacle_type and "CACTUS" in obstacle_type:
            action = 1

        # Высокая птица
        elif obstacle_type == "PTERODACTYL" and y == 50:
            action = 0

        else:
            action = 0

        self.actions.perform(action)
        self.handled_obstacle = obstacle_id
        self.last_action_time = time.time()

        return (
            f"{obstacle_type} | Y: {y} | "
            f"Distance: {distance:.1f} | "
            f"Speed: {speed:.2f} | Action: {action}"
        )