# labyrinth_game/player_actions.py

from .constants import ROOMS
from .utils import random_event

def get_input(prompt="> "):
    """
    Безопасный ввод данных от пользователя с обработкой исключений
    """
    try:
        return input(prompt).strip().lower()
    except (KeyboardInterrupt, EOFError):
        print("\nВыход из игры.")
        return "quit"

def show_inventory(game_state):
    """
    Отображает содержимое инвентаря игрока
    """
    inventory = game_state['player_inventory']
    
    if not inventory:
        print("Ваш инвентарь пуст.")
    else:
        print("Ваш инвентарь:")
        for item in inventory:
            print(f"  - {item}")
    
    print()

def move_player(game_state, direction):
    """
    Перемещает игрока в указанном направлении
    """
    current_room_name = game_state['current_room']
    current_room_data = ROOMS[current_room_name]
    
    if direction not in current_room_data['exits']:
        print(f"Нет выхода на {direction}.")
        print(f"Доступные направления: {', '.join(current_room_data['exits'].keys())}")
        return False
    
    destination_room = current_room_data['exits'][direction]
    
    if destination_room not in ROOMS:
        print(f"Ошибка: комната '{destination_room}' не существует!")
        return False
    
    game_state['current_room'] = destination_room
    
    print(f"Вы идете на {direction}...")
    print()
    
    from .utils import describe_current_room
    describe_current_room(game_state)
    
    # Увеличиваем счетчик шагов и проверяем случайные события
    game_state['steps'] += 1
    random_event(game_state)
    
    return True

def take_item(game_state, item_name):
    """
    Попытка взять предмет из текущей комнаты
    """
    if not item_name:
        print("Укажите, что вы хотите взять. Например: 'take torch' или 'взять факел'")
        return
    
    current_room_name = game_state['current_room']
    room_data = ROOMS[current_room_name]
    
    if item_name == 'treasure_chest':
        print("Вы не можете поднять сундук, он слишком тяжелый.")
        return
    
    if item_name in room_data['items']:
        room_data['items'].remove(item_name)
        
        game_state['player_inventory'].append(item_name)
        
        print(f"Вы взяли: {item_name}")
        print()
    else:
        available_items = room_data['items']
        if available_items:
            print(f"Предмет '{item_name}' здесь не найден.")
            print(f"Доступные предметы: {', '.join(available_items)}")
        else:
            print("В этой комнате нет предметов для взятия.")
        print()

def get_direction_aliases():
    """
    Возвращает словарь с псевдонимами направлений
    """
    return {
        'north': 'north',
        'south': 'south', 
        'east': 'east',
        'west': 'west',
        'n': 'north',
        's': 'south',
        'e': 'east',
        'w': 'west',

        'север': 'north',
        'юг': 'south',
        'восток': 'east',
        'запад': 'west',
        'с': 'north',
        'ю': 'south',
        'в': 'east',
        'з': 'west',
    }

def parse_direction(direction_input):
    """
    Преобразует ввод пользователя в стандартное направление
    """
    aliases = get_direction_aliases()
    return aliases.get(direction_input.lower(), direction_input.lower())