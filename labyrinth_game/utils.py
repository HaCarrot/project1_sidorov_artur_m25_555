from labyrinth_game.constants import ROOMS


def describe_current_room(game_state: dict):
    if game_state is None: 
        return
    print(f"\033[32m== {game_state['current_room'].upper()} ==\033[0m")
    print(f"{ROOMS[game_state['current_room']]['description']}")
    if len(ROOMS[game_state['current_room']]['items']) > 0:
        print("Заметные предметы:")
        for item in ROOMS[game_state['current_room']]['items']:
            print(f"\033[33m{item}\033[0m")
    if len(ROOMS[game_state['current_room']]['exits']) > 0:
        print("Выходы:")
        for exit in ROOMS[game_state['current_room']]['exits']:
            print(f"\033[35m{exit}\033[0m")
    if ROOMS[game_state['current_room']]['puzzle'] is not None:
        print("\033[34mКажется, здесь есть загадка (используйте команду solve).\033[0m")