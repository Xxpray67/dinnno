class DinoActions:
    def __init__(self, page):
        self.page = page

    def perform(self, action):
        if action == 0:
            # Ничего не делаем
            self.page.keyboard.up("Space")
            self.page.keyboard.up("ArrowDown")

        elif action == 1:
            # Прыжок
            self.page.keyboard.up("ArrowDown")
            self.page.keyboard.down("Space")

        elif action == 2:
            # Приседание
            self.page.keyboard.up("Space")
            self.page.keyboard.down("ArrowDown")

        else:
            raise ValueError("Неизвестное действие!")

    def release_all(self):
        self.page.keyboard.up("Space")
        self.page.keyboard.up("ArrowDown")