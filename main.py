import time

print("[1] Запуск main.py")

from dino_environment import DinoEnvironment
from dino_controller import DinoController

print("[2] Импорты выполнены!")

def main():
    print("[3] MAIN FUNCTION STARTED")

    env = DinoEnvironment()
    print("[4] ENVIRONMENT CREATED")

    try:
        print("[5] Запускаем Chrome...")
        env.start()

        print("[6] Chrome запущен!")

        controller = DinoController(env.page)
        print("[7] DinoAI подключена!")

        print("Начинаем игру! Для остановки нажми Ctrl+C.")

        while True:
            result = controller.update()

            if result in ["DEAD", "NO_RUNNER", "NOT_PLAYING"]:
                print("Игра завершена:", result)
                break

            if result not in ["RUN", "WAIT"]:
                print(result)

            time.sleep(0.05)

    except KeyboardInterrupt:
        print("Остановка пользователем.")

    except Exception as error:
        print("ОШИБКА:", repr(error))

    finally:
        env.close()
        print("Игровая среда закрыта.")
        input("Нажми Enter для выхода...")
if __name__ == "__main__":
    print("[START] Вызываем main()")
    main()