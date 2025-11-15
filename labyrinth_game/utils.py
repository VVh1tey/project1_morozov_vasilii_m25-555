# labyrinth_game/utils.py

from .constants import ROOMS


def describe_current_room(game_state):
    """
    Выводит описание текущей комнаты игрока
    """
    current_room_name = game_state["current_room"]
    room_data = ROOMS[current_room_name]

    print(f"== {current_room_name.upper()} ==")

    print(room_data["description"])

    if room_data["items"]:
        print(f"Заметные предметы: {', '.join(room_data['items'])}")

    exits = list(room_data["exits"].keys())
    print(f"Выходы: {', '.join(exits)}")

    if room_data["puzzle"] is not None:
        print("Кажется, здесь есть загадка (используйте команду solve).")

    print()
