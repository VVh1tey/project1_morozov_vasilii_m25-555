# labyrinth_game/utils.py

from .constants import ROOMS
import math

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
    player_answer = input("Ваш ответ: ").strip().lower()
    
    # Проверка альтернативных вариантов ответа
    correct_answers = [correct_answer.lower()]
    if correct_answer == '10':
        correct_answers.extend(['десять', 'ten'])
        
    if player_answer in correct_answers:
        print("Правильно! Отличная работа!")
        room_data['puzzle'] = None
        give_puzzle_reward(game_state, current_room_name)
        
    else:
        print("Неверно. Попробуйте снова.")
        if current_room_name == 'trap_room':
            trigger_trap(game_state)


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
    want_code = input("Ввести код? (да/нет): ").strip().lower()
    
    if want_code in ['да', 'yes', 'д', 'y']:
        if room_data['puzzle']:
            _, correct_code = room_data['puzzle']
            
            player_code = input("Введите код: ").strip()
            
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
    from .constants import COMMANDS
    
    print("Доступные команды:")
    for cmd, desc in COMMANDS.items():
        # Форматируем вывод с выравниванием по левому краю (16 символов)
        print(f"  {cmd.ljust(16)} - {desc}")
    print()

def pseudo_random(seed, modulo):
    """
    Генерирует псевдослучайное число в диапазоне [0, modulo)
    на основе синуса и математических преобразований
    """
    x = math.sin(seed * 12.9898) * 43758.5453
    fractional = x - math.floor(x)
    return int(fractional * modulo)

def trigger_trap(game_state):
    """
    Обрабатывает срабатывание ловушки с различными последствиями
    """
    print("\nЛовушка активирована! Пол стал дрожать...\n")
    
    inventory = game_state['player_inventory']
    if inventory:
        index = pseudo_random(len(inventory), len(inventory))
        lost_item = inventory.pop(index)
        print(f"Вы потеряли предмет: {lost_item}!")
    else:
        damage = pseudo_random(game_state['steps_taken'], 10)
        if damage < 3:
            print("Каменная плита падает на вас! Игра окончена.")
            game_state['game_over'] = True
        else:
            print("Вам удалось увернуться в последний момент!")

def random_event(game_state):
    """
    Создает случайные события во время перемещения игрока
    """
    if pseudo_random(game_state['steps_taken'], 10) != 0:
        return
    
    event_type = pseudo_random(game_state['steps_taken'], 3)
    current_room = game_state['current_room']
    inventory = game_state['player_inventory']
    
    if event_type == 0:
        print("\nВы заметили блестящую монетку на полу!\n")
        ROOMS[current_room]['items'].append('coin')
    elif event_type == 1:
        print("\nВы слышите странный шорох позади себя...\n")
        if 'sword' in inventory:
            print("Вы резко оборачиваетесь с мечом в руке - существо убегает!\n")
    elif event_type == 2:
        if current_room == 'trap_room' and 'torch' not in inventory:
            print("\nВы чувствуете, как пол под ногами начинает двигаться...\n")
            trigger_trap(game_state)