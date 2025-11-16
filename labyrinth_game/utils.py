# labyrinth_game/utils.py

from .constants import ROOMS
from .player_actions import get_input


def describe_current_room(game_state):
    """
    Выводит описание текущей комнаты игрока
    """
    current_room_name = game_state['current_room']
    room_data = ROOMS[current_room_name]
    
    print(f"== {current_room_name.upper()} ==")
    
    print(room_data['description'])
    
    if room_data['items']:
        print(f"Заметные предметы: {', '.join(room_data['items'])}")
    
    exits = list(room_data['exits'].keys())
    print(f"Выходы: {', '.join(exits)}")
    
    if room_data['puzzle'] is not None:
        print("Кажется, здесь есть загадка (используйте команду solve).")
    print()

def solve_puzzle(game_state):
    """
    Функция для решения загадок в текущей комнате
    """
    current_room_name = game_state['current_room']
    room_data = ROOMS[current_room_name]
    
    if room_data['puzzle'] is None:
        print("Загадок здесь нет.")
        return
    
    if current_room_name == 'treasure_room':
        attempt_open_treasure(game_state)
        return
    
    puzzle_question, correct_answer = room_data['puzzle']
    print(puzzle_question)
    player_answer = get_input("Ваш ответ: ").strip().lower()
    
    if player_answer == correct_answer.lower():
        print("Правильно! Отличная работа!")
        room_data['puzzle'] = None
        give_puzzle_reward(game_state, current_room_name)
        
    else:
        print("Неверно. Попробуйте снова.")


def give_puzzle_reward(game_state, room_name):
    """
    Даёт награду игроку за решение загадки
    """
    rewards = {
        'hall': 'small_key',
        'trap_room': 'safe_passage',
        'library': 'treasure_key',
        'garden': 'magic_water',
        'observatory': 'star_knowledge',
        'underground': 'ancient_wisdom',
        'secret_chamber': 'power_crystal'
    }
    
    reward = rewards.get(room_name)
    if reward:
        if reward == 'safe_passage':
            print("Теперь вы можете безопасно проходить через эту комнату!")
        elif reward == 'treasure_key':
            print("Среди свитков вы находите ЗОЛОТОЙ КЛЮЧ от сокровищницы!")
            game_state['player_inventory'].append('treasure_key')
        else:
            print(f"За решение загадки вы получаете: {reward}")
            game_state['player_inventory'].append(reward)


def attempt_open_treasure(game_state):
    """
    Попытка открыть сундук с сокровищами
    """
    current_room_name = game_state['current_room']
    room_data = ROOMS[current_room_name]
    
    if 'treasure_key' in game_state['player_inventory']:
        print("Вы применяете ключ, и замок щёлкает. Сундук открыт!")
        
        if 'treasure_chest' in room_data['items']:
            room_data['items'].remove('treasure_chest')
        
        print("В сундуке сокровище! Вы победили!")
        game_state['game_over'] = True
        return
    
    print("Сундук заперт массивным замком.")
    want_code = get_input("Ввести код? (да/нет): ").strip().lower()
    
    if want_code in ['да', 'yes', 'д', 'y']:
        if room_data['puzzle']:
            _, correct_code = room_data['puzzle']
            
            player_code = get_input("Введите код: ").strip()
            
            if player_code == correct_code:
                print("Код верный! Замок открывается с тихим щелчком.")
                
                if 'treasure_chest' in room_data['items']:
                    room_data['items'].remove('treasure_chest')
                
                print("В сундуке сокровище! Вы победили!")
                game_state['game_over'] = True
            else:
                print("Неверный код. Замок остается заперт.")
        else:
            print("Нет подсказок для кода.")
    else:
        print("Вы отступаете от сундука.")

def show_help():
    """
    Показывает список доступных команд
    """
    print("Доступные команды:")
    print("  look/осмотреться/l        - описание текущей комнаты")
    print("  inventory/инвентарь/i     - показать ваши предметы")
    print("  solve/загадка/s           - решить загадку в комнате")
    print("  take [предмет]/взять      - взять предмет")
    print("  quit/выход/q              - выйти из игры")
    print("  help/помощь/h             - показать эту справку")
    print()