#usr/bin/env python3
from labyrinth_game.utils import describe_current_room

game_state = {
    'player_inventory': [], # Инвентарь игрока
    'current_room': 'entrance', # Текущая комната
    'game_over': False, # Значения окончания игры
    'steps_taken': 0 # Количество шагов
}

def main():
    print("\033[1mДобро пожаловать в Лабиринт сокровищ!\033[0m")
    describe_current_room(game_state)
    #while True:
    #   command = input("> Введите команду:")

if __name__ == "__main__":
    main()