# labyrinth_game/input_handler.py

def get_input(prompt="> "):
    """
    Безопасный ввод данных от пользователя с обработкой исключений
    """
    try:
        return input(prompt).strip().lower()
    except (KeyboardInterrupt, EOFError):
        print("\nВыход из игры.")
        return "quit"