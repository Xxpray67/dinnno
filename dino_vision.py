import time
from io import BytesIO

from PIL import Image
from playwright.sync_api import sync_playwright

GAME_URL = "https://wayou.github.io/t-rex-runner/"

IMAGE_SIZE = (84, 84)
FRAME_COUNT = 10
FRAME_DELAY = 0.5

def main():
    print("Запускаем DinoVision...")

    with sync_playwright() as p:
        browser = p.chromium.launch(
            channel="chrome",
            headless=False
        )

        page = browser.new_page(
            viewport={
                "width": 800,
                "height": 600
            }
        )

        print("Открываем игру...")
        page.goto(GAME_URL, wait_until="networkidle")
        time.sleep(2)

        canvas = page.locator("canvas").first
        canvas.wait_for(state="visible")

        print("Запускаем динозавра...")
        canvas.click()
        page.keyboard.press("Space")

        time.sleep(1)

        print("Начинаем сбор кадров...")

        for frame in range(1, FRAME_COUNT + 1):
            screenshot = canvas.screenshot()

            image = Image.open(
                BytesIO(screenshot)
            )

            image = image.convert("L")
            image = image.resize(IMAGE_SIZE)

            filename = f"frame_{frame:02d}.png"
            image.save(filename)

            print(
                f"Кадр {frame}/{FRAME_COUNT} сохранён: "
                f"{filename}, размер: {image.size}"
            )

            time.sleep(FRAME_DELAY)

        print("\nСбор кадров завершён!")

        input("Нажми Enter для закрытия...")
        browser.close()
if __name__ == "__main__":
    main()