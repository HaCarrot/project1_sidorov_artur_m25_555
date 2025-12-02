from labyrinth_game.constants import ROOMS
from labyrinth_game.utils import describe_current_room


def show_inventory(game_state: dict):
    if len(game_state['player_inventory']) > 0:
        print("\033[32m * ИНВЕНТАРЬ * \033[0m")
        for item in game_state['player_inventory']:
            print(f"\033[33m{item}\033[0m")
    else:
        print("Инвентарь пуст!")

def get_input(prompt="> "):
    try:
        command = input(prompt)
        return command
    except (KeyboardInterrupt, EOFError):
        print("\nВыход из игры.")
        return "quit" 

def move_player(game_state: dict, direction: str):
    if direction in ROOMS[game_state['current_room']]['exits']:
        game_state['current_room'] = ROOMS[game_state['current_room']]['exits'][direction]
        game_state['steps_taken'] += 1
        describe_current_room(game_state)
    else:
        print("\033[31mНельзя пойти в этом направлении!\033[0m")

def take_item(game_state: dict, item_name: str):
    if item_name == 'treasure_chest':
        print("Вы не можете поднять сундук, он слишком тяжелый.")
    elif item_name in ROOMS[game_state['current_room']]['items']\
    and ROOMS[game_state['current_room']]['puzzle'] is None:
        game_state['player_inventory'].append(item_name) 
        ROOMS[game_state['current_room']]['items'].remove(item_name)
        print(f"Вы подобрали: \033[35m{item_name}\033[0m")
        describe_current_room(game_state)
    elif item_name in ROOMS[game_state['current_room']]['items']\
    and ROOMS[game_state['current_room']]['puzzle'] is not None:
        print("Предмет так просто не даётся! Решите загадку.")
    else:
        print("\033[31mТакого предмета здесь нет.\033[0m")

def use_item(game_state: dict, item_name: str):
    if item_name in game_state['player_inventory']:
        match item_name:
            case 'torch':
                print('Определённо стало светлее.')
            case 'sword':
                print('Вы чувствуете себя увереннее!')
            case 'bronze_box':
                print('Вы открыли шкатулку и обнаружили там \033[35mrusty_key\033[0m"!')
                game_state['player_inventory'].append('rusty_key')
            case _:
                print("Крутая штука! Жаль, игрок не знает как это использовать.")
    else:
        print("У вас нет такого предмета.")