from labyrinth_game.constants import ROOMS
from labyrinth_game.player_actions import get_input


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

def solve_puzzle(game_state):
    if ROOMS[game_state['current_room']]['puzzle'] is not None:
        print(ROOMS[game_state['current_room']]['puzzle'][0])
        answer = get_input("> Ваш ответ: ")
        if answer == ROOMS[game_state['current_room']]['puzzle'][1]:
            print(f"Отличное решение! Ваша награда:\
                   \033[33m{game_state['puzzle'][2]}\033[0m")
            game_state['inventory'].append(ROOMS[game_state['current_room']]['item'])
            ROOMS[game_state['current_room']]['puzzle'] = None
        else:
            print("Неверно. Попробуйте снова.")
    else:
        print("Загадок здесь нет.")

def attempt_open_treasure(game_state):
    if 'treasure_key' in game_state['inventory']:
        print("Вы применяете ключ, и замок щёлкает. Сундук открыт!")
        ROOMS[game_state['current_room']]['items'].remove('treasure_chest')
        print("\033[1mВ сундуке сокровище! Вы победили!\033[0m")
        game_state['game_over'] = True
    else:
        answer = get_input("Сундук заперт. ... Ввести код? (да/нет) ")
        if answer == "да":
            solve_puzzle(game_state)
            attempt_open_treasure(game_state)
        else:
            print("Вы отступаете от сундука.")

def show_help():
    print("\nДоступные команды:")
    print("  go <direction>  - перейти в направлении (north/south/east/west)")
    print("  look            - осмотреть текущую комнату")
    print("  take <item>     - поднять предмет")
    print("  use <item>      - использовать предмет из инвентаря")
    print("  inventory       - показать инвентарь")
    print("  solve           - попытаться решить загадку в комнате")
    print("  quit            - выйти из игры")
    print("  help            - показать это сообщение") 