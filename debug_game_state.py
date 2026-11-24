import inspect
from dino_game_state import DinoGameState

print("Файл класса:")
print(inspect.getfile(DinoGameState))

print("\nКонструктор:")
print(inspect.signature(DinoGameState.__init__))

print("\nМетоды класса:")
print(dir(DinoGameState))

game_state = DinoGameState("TEST")
print("Объект успешно создан:", game_state)