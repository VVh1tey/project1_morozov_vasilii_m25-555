# labyrinth_game/main.py

from .constants import ROOMS
from .player_actions import get_input, show_inventory, parse_direction,move_player
from .utils import describe_current_room, show_help, solve_puzzle


def process_command(command, game_state):
    """
    Обрабатывает команды пользователя
    """
    if command in ["quit", "выход", "q"]:
        print("Спасибо за игру! До свидания!")
        game_state['game_over'] = True
        
    elif command in ["look", "осмотреться", "l"]:
        describe_current_room(game_state)
        
    elif command in ["inventory", "инвентарь", "i"]:
        show_inventory(game_state)
        
    elif command in ["solve", "загадка", "s"]:
        solve_puzzle(game_state)
        
    elif command in ["help", "помощь", "h"]:
        show_help()
        
    elif command.startswith("take ") or command.startswith("взять "):
        item_name = command.split(" ", 1)[1] if " " in command else ""
        take_item(game_state, item_name)
        
    elif command.startswith("go ") or command.startswith("move ") or command.startswith("идти "):
        direction_input = command.split(" ", 1)[1] if " " in command else ""
        direction = parse_direction(direction_input)
        move_player(game_state, direction)
        
    elif command.startswith("m "):
        direction_input = command.split(" ", 1)[1] if " " in command else ""
        direction = parse_direction(direction_input)
        move_player(game_state, direction)
        
    elif command in ["north", "south", "east", "west", "n", "s", "e", "w",
                     "север", "юг", "восток", "запад", "с", "ю", "в", "з"]:
        direction = parse_direction(command)
        move_player(game_state, direction)
        
    else:
        print(f"Неизвестная команда: '{command}'. Попробуйте 'help' для списка команд.")
        print()


def take_item(item_name, game_state):
    """
    Попытка взять предмет
    """
    current_room_name = game_state['current_room']
    room_data = ROOMS[current_room_name]
    
    if item_name == 'treasure_chest':
        print("Вы не можете поднять сундук, он слишком тяжелый.")
        return
    
    if item_name in room_data['items']:
        room_data['items'].remove(item_name)
        
        game_state['player_inventory'].append(item_name)
        
        print(f"Вы взяли: {item_name}")
    else:
        print(f"Предмет '{item_name}' здесь не найден.")

def main():
    """
    Основная функция игры - главный игровой цикл
    """
    # Создаем начальное состояние игры
    game_state = {
        'current_room': 'entrance',
        'player_inventory': [],
        'game_over': False
    }
    
    print("Добро пожаловать в Лабиринт сокровищ!")
    print("Ваша цель - найти сокровище в сокровищнице!")
    
    describe_current_room(game_state)
    
    while not game_state['game_over']:
        user_command = get_input("Введите команду: ")
        
        process_command(user_command, game_state)

if __name__ == "__main__":
    main()