from labyrinth_game.constants import COLORS, ROOMS
from labyrinth_game.utils import describe_current_room, random_event


def show_inventory(game_state: dict):
    """Функция отображения инвентаря."""
    if len(game_state["player_inventory"]) > 0:
        print(f"{COLORS['GREEN']} * ИНВЕНТАРЬ * {COLORS['RESET']}")
        for item in game_state["player_inventory"]:
            print(f"{COLORS['YELLOW']}{item}{COLORS['YELLOW']}")
    else:
        print("Инвентарь пуст!")


def get_input(prompt="> "):
    """Функция для ввода пользователя. Принимает на вход строку-подсказку."""
    try:
        command = input(prompt)
        return command
    except (KeyboardInterrupt, EOFError):
        print("\nВыход из игры.")
        return "quit"


def move_player(game_state: dict, direction: str):
    """Функция движения игрока. 
    Принимает игровое состояние и направление движения."""
    if direction in ROOMS[game_state["current_room"]]["exits"]:
        if ROOMS[game_state["current_room"]]["exits"][direction] == "treasure_room":
            if "rusty_key" in game_state["player_inventory"]:
                print(
                    "Вы используете найденный ключ,\
чтобы открыть путь в комнату сокровищ."
                )
            else:
                print("Дверь заперта. Нужен ключ, чтобы пройти дальше.")
                return
        game_state["current_room"] = ROOMS[game_state["current_room"]]["exits"][
            direction
        ]
        game_state["steps_taken"] += 1
        describe_current_room(game_state)
        random_event(game_state)
    else:
        print(f"{COLORS['RED']}Нельзя пойти в этом направлении!{COLORS['RESET']}")


def take_item(game_state: dict, item_name: str):
    """Функция поднятия предмета игроком. 
    Принимает игровое состояние и название предмета."""
    if item_name == "treasure_chest":
        print("Вы не можете поднять сундук, он слишком тяжелый.")
    elif (
        item_name in ROOMS[game_state["current_room"]]["items"]
        and ROOMS[game_state["current_room"]]["puzzle"] is None
    ):
        game_state["player_inventory"].append(item_name)
        ROOMS[game_state["current_room"]]["items"].remove(item_name)
        print(f"Вы подобрали: {COLORS['MAGENTA']}{item_name}{COLORS['RESET']}")
        describe_current_room(game_state)
    elif (
        item_name in ROOMS[game_state["current_room"]]["items"]
        and ROOMS[game_state["current_room"]]["puzzle"] is not None
    ):
        print("Предмет так просто не даётся! Решите загадку.")
    else:
        print(f"{COLORS['RED']}Такого предмета здесь нет.{COLORS['RESET']}")


def use_item(game_state: dict, item_name: str):
    """Функция использования предмета игроком.
    Принимает игровое состояние и название предмета."""
    if item_name in game_state["player_inventory"]:
        match item_name:
            case "torch":
                print("Определённо стало светлее.")
            case "sword":
                print("Вы чувствуете себя увереннее!")
            case "bronze_box":
                print(
                    f"Вы открыли шкатулку и обнаружили\
там {COLORS['MAGENTA']}treasure_key{COLORS['RESET']}!"
                )
                game_state["player_inventory"].append("treasure_key")
            case _:
                print("Крутая штука! Жаль, игрок не знает как это использовать.")
    else:
        print("У вас нет такого предмета.")
