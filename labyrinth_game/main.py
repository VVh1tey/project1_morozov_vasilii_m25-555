from .player_actions import get_input, show_inventory
from .utils import describe_current_room


def main():

    game_state = {
        "player_inventory": [],  # Инвентарь игрока
        "current_room": "entrance",  # Текущая комната
        "game_over": False,  # Значения окончания игры
        "steps_taken": 0,  # Количество шагов
    }

    print("Добро пожаловать в Лабиринт сокровищ!")
    print()

    describe_current_room(game_state)

    while not game_state["game_over"]:
        user_command = get_input("Введите команду: ")

        # Обрабатываем основные команды
        if user_command == "quit" or user_command == "выход" or user_command == "q":
            print("Спасибо за игру! До свидания!")
            game_state["game_over"] = True

        elif user_command == "look" or user_command == "осмотреться":
            describe_current_room(game_state)

        elif user_command == "inventory" or user_command == "инвентарь":
            show_inventory(game_state)

        elif user_command == "help" or user_command == "помощь":
            print("Доступные команды:")
            print("  look/осмотреться - описание текущей комнаты")
            print("  inventory/инвентарь - показать ваши предметы")
            print("  quit/выход - выйти из игры")
            print("  help/помощь - показать эту справку")
            print()

        else:
            print(
                f"Неизвестная команда: '{user_command}'."
                " Попробуйте 'help' для списка команд."
            )
            print()


if __name__ == "__main__":
    main()
