from labyrinth_game.constants import COMMANDS, ROOMS, COLORS


def describe_current_room(game_state: dict):
    if game_state is None: 
        return
    print(f"{COLORS['BLUE']}== {game_state['current_room'].upper()} =={COLORS['RESET']}")
    print(f"{ROOMS[game_state['current_room']]['description']}")
    if len(ROOMS[game_state['current_room']]['items']) > 0:
        print("Заметные предметы:")
        for item in ROOMS[game_state['current_room']]['items']:
            print(f"{COLORS['YELLOW']}{item}{COLORS['RESET']}")
    if len(ROOMS[game_state['current_room']]['exits']) > 0:
        print("Выходы:")
        for exit in ROOMS[game_state['current_room']]['exits']:
            print(f"{COLORS['MAGENTA']}{exit}{COLORS['RESET']}")
    if ROOMS[game_state['current_room']]['puzzle'] is not None:
        print(f"{COLORS['BLUE']}Кажется, здесь есть загадка (используйте команду solve).{COLORS['RESET']}")

def solve_puzzle(game_state: dict):
    from labyrinth_game.player_actions import get_input
    if ROOMS[game_state['current_room']]['puzzle'] is not None:
        print(ROOMS[game_state['current_room']]['puzzle'][0])
        answer = get_input("> Ваш ответ: ")
        if answer == "quit":
            game_state['game_over'] = True
        elif answer == ROOMS[game_state['current_room']]['puzzle'][1] or answer == 'десять' and game_state['current_room'] == 'hall':
            print(f"Отличное решение! Ваша награда:{COLORS['YELLOW']}{ROOMS[game_state['current_room']]['items']}{COLORS['RESET']}")
            for item in ROOMS[game_state['current_room']]['items']:
                game_state['player_inventory'].append(item) 
                ROOMS[game_state['current_room']]['items'].remove(item)
                print(f"Вы подобрали: {COLORS['YELLOW']}{item}{COLORS['RESET']}")
            ROOMS[game_state['current_room']]['puzzle'] = None
        else:
            if game_state['current_room'] == 'trap_room':
                trigger_trap(game_state)
            else:
                print("Неверно. Попробуйте снова.")
    else:
        print("Загадок здесь нет.")

def attempt_open_treasure(game_state: dict):
    from labyrinth_game.player_actions import get_input
    if 'treasure_key' in game_state['player_inventory']:
        print("Вы применяете ключ, и замок щёлкает. Сундук открыт!")
        ROOMS[game_state['current_room']]['items'].remove('treasure_chest')
        print(f"{COLORS['BOLD']}В сундуке сокровище! Вы победили!{COLORS['RESET']}")
        game_state['game_over'] = True
    else:
        answer = get_input("Сундук заперт. ... Ввести код? (да/нет) ")
        if answer == "quit":
            game_state['game_over'] = True
        elif answer == "да":
            print(ROOMS[game_state['current_room']]['puzzle'][0])
            answer = get_input("> Ваш ответ: ")
            if answer == ROOMS[game_state['current_room']]['puzzle'][1]:
                print("Вы угадываете код, и замок щёлкает. Сундук открыт!")
                ROOMS[game_state['current_room']]['items'].remove('treasure_chest')
                print(f"{COLORS['BOLD']}В сундуке сокровище! Вы победили!{COLORS['RESET']}")
                game_state['game_over'] = True
            else:
                print("Неверно. Попробуйте снова.")
        else:
            print("Вы отступаете от сундука.")

def pseudo_random(seed, modulo:int) -> int:
    from math import floor, sin
    x = sin(seed)*12.9898*43758.5453
    x -= floor(x)
    return floor(x*modulo)

def trigger_trap(game_state: dict):
    print("Ловушка активирована! Пол стал дрожать...")
    if len(game_state["player_inventory"]) > 0:
        game_state['player_inventory'].pop(pseudo_random(game_state['steps_taken'],len(game_state['player_inventory'])))
    else:
        if pseudo_random(game_state['steps_taken'], 9) < 3:
            print('\033[31mВы упали в яму с шипами! Игра окончена!\033[0m')
            game_state['game_over'] = True
        else:
            print("\033[1mВы героически отпрыгнули и уцелели!\033[0m")

def random_event(game_state: dict):
    if pseudo_random(game_state['steps_taken'], 10) == 0:
        match pseudo_random(game_state['steps_taken'], 10):
            case 0:
                print("На полу неожиданно появилась монетка! Магия...")
                ROOMS[game_state['current_room']]['items'].append('coin')
            case 1:
                print("Кажется где-то раздаётся шорох...")
                if 'sword' in game_state['player_inventory']:
                    print("Вы отпугнули неизвестность своим мечом.")
            case 2:
                if game_state['current_room'] == 'trap_room' \
                    and 'torch' not in game_state['player_inventory']:
                    trigger_trap()

def show_help():
    print("\nДоступные команды:")
    for key, value in COMMANDS.items():
        print(f"{key:16} - {value}")