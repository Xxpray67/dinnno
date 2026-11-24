import time
from io import BytesIO

import torch
from PIL import Image
from playwright.sync_api import sync_playwright

GAME_URL = "https://wayou.github.io/t-rex-runner/"
IMAGE_SIZE = (84, 84)

class DinoEnvironment:
    def __init__(self):
        self.device = torch.device(
            "cuda" if torch.cuda.is_available() else "cpu"
        )

        self.playwright = None
        self.browser = None
        self.page = None
        self.canvas = None

    def start(self):
        print("Запускаем игровую среду...")

        self.playwright = sync_playwright().start()

        self.browser = self.playwright.chromium.launch(
            channel="chrome",
            headless=False
        )

        self.page = self.browser.new_page(
            viewport={
                "width": 800,
                "height": 600
            }
        )

        self.page.goto(
            GAME_URL,
            wait_until="networkidle"
        )

        time.sleep(2)

        self.canvas = self.page.locator("canvas").first
        self.canvas.wait_for(state="visible")

        self.canvas.click()
        self.page.keyboard.press("Space")

        time.sleep(1)

        print("Игровая среда запущена!")

    def get_observation(self):
        screenshot = self.canvas.screenshot()

        image = Image.open(
            BytesIO(screenshot)
        )

        image = image.convert("L")
        image = image.resize(IMAGE_SIZE)

        image_tensor = torch.tensor(
            list(image.getdata()),
            dtype=torch.float32
        ).reshape(1, 84, 84) / 255.0

        return image_tensor.to(self.device)

    def close(self):
        if self.browser:
            self.browser.close()

        if self.playwright:
            self.playwright.stop()
if __name__ == "__main__":
    env = DinoEnvironment()

    try:
        env.start()

        observation = env.get_observation()

        print("Размер наблюдения:", observation.shape)
        print("Устройство:", observation.device)
        print("Минимум:", observation.min().item())
        print("Максимум:", observation.max().item())

        print("DinoEnvironment успешно работает!")

        input("Нажми Enter для закрытия...")

    finally:
            env.close()