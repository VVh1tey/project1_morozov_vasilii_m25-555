# labyrinth_game/main.py
from .constants import ROOMS

def main():
    game_state = {
        'player_inventory': [], # Инвентарь игрока
        'current_room': 'entrance', # Текущая комната
        'game_over': False, # Значения окончания игры
        'steps_taken': 0 # Количество шагов
    }
  
    print("\nДобро пожаловать в Лабиринт сокровищ!")
    print("Доступные команты:")
    for x in ROOMS:
        print(x)

if __name__ == "__main__":
    main()