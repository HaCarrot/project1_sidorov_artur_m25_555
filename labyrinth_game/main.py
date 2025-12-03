# usr/bin/env python3
from labyrinth_game.constants import COLORS
from labyrinth_game.player_actions import (
    get_input,
    move_player,
    show_inventory,
    take_item,
    use_item,
)
from labyrinth_game.utils import (
    attempt_open_treasure,
    describe_current_room,
    show_help,
    solve_puzzle,
)

game_state = {
    "player_inventory": [],  # Инвентарь игрока
    "current_room": "entrance",  # Текущая комната
    "game_over": False,  # Значения окончания игры
    "steps_taken": 0,  # Количество шагов
}


def process_command(game_state: dict, command: str):
    """Обрабочтик внутриигровых комманд."""
    try:
        word_list = command.split()
        match word_list[0]:
            case "look":
                describe_current_room(game_state)
            case "use":
                use_item(game_state, word_list[1])
            case "go" | "north" | "east" | "west" | "south":
                move_player(
                    game_state, word_list[1] if word_list[0] == "go" else word_list[0]
                )
            case "take":
                take_item(game_state, word_list[1])
            case "inventory":
                show_inventory(game_state)
            case "solve":
                if game_state["current_room"] == "treasure_room":
                    attempt_open_treasure(game_state)
                else:
                    solve_puzzle(game_state)
            case "help":
                show_help()
            case "quit" | "exit":
                return 0
            case _:
                raise Exception()
    except Exception:
        print("Неверная команда!")
    return None


def main():
    print(f"{COLORS['BOLD']}Добро пожаловать в Лабиринт сокровищ!{COLORS['RESET']}")
    describe_current_room(game_state)
    while not game_state["game_over"]:
        command = get_input()
        if process_command(game_state, command) == 0:
            break


if __name__ == "__main__":
    main()
