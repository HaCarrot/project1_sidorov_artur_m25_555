def show_inventory(game_state: dict):
    if len(game_state['player_inventory']) > 0:
        print("\033[32m * ИНВЕНТАРЬ * \033[0m")
        for item in game_state['player_inventory']:
            print(f"\033[33m{item}\033[0m")

def get_input(prompt="> "):
    try:
        pass
    except (KeyboardInterrupt, EOFError):
        print("\nВыход из игры.")
        return "quit" 