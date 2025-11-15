# labyrinth_game/player_actions.py

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
    inventory = game_state["player_inventory"]

    if not inventory:
        print("Ваш инвентарь пуст.")
    else:
        print("Ваш инвентарь:")
        for item in inventory:
            print(f"  - {item}")

    print()
