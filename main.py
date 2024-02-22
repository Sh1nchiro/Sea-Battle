import random

def print_board(board):
    for row in board:
        print(" ".join(row))

def create_board():
    return [["O" for _ in range(5)] for _ in range(5)]

def is_valid_move(row, col):
    return 0 <= row < 5 and 0 <= col < 5

def place_ship(board, size):
    while True:
        orientation = random.choice(["horizontal", "vertical"])
        if orientation == "horizontal":
            ship_row = random.randint(0, 4)
            ship_col = random.randint(0, 4 - size + 1)
            if all(board[ship_row][c] == "O" for c in range(ship_col, ship_col + size)):
                for c in range(ship_col, ship_col + size):
                    board[ship_row][c] = "■"
                return [(ship_row, c) for c in range(ship_col, ship_col + size)]
        else:
            ship_row = random.randint(0, 4 - size + 1)
            ship_col = random.randint(0, 4)
            if all(board[r][ship_col] == "O" for r in range(ship_row, ship_row + size)):
                for r in range(ship_row, ship_row + size):
                    board[r][ship_col] = "■"
                return [(r, ship_col) for r in range(ship_row, ship_row + size)]

def user_turn(board, previous_guesses):
    while True:
        guess_row = int(input("Введите номер строки для выстрела (0-4): "))
        guess_col = int(input("Введите номер столбца для выстрела (0-4): "))

        if not is_valid_move(guess_row, guess_col):
            print("Ошибка! Введите корректные координаты (от 0 до 4).")
        elif (guess_row, guess_col) in previous_guesses:
            print("Ошибка! Вы уже выстрелили сюда. Выберите другую клетку.")
        else:
            return guess_row, guess_col

def computer_turn(board, previous_guesses):
    while True:
        guess_row = random.randint(0, 4)
        guess_col = random.randint(0, 4)

        if (guess_row, guess_col) not in previous_guesses:
            return guess_row, guess_col

def display_hidden_board(board, previous_guesses):
    hidden_board = [["O" for _ in range(5)] for _ in range(5)]
    for guess_row, guess_col in previous_guesses:
        if board[guess_row][guess_col] == "■":
            hidden_board[guess_row][guess_col] = "X"  # Hit
    print("\nДоска противника:")
    print_board(hidden_board)

def is_ship_destroyed(ship_coordinates, previous_guesses):
    return all(coord in previous_guesses for coord in ship_coordinates)

def main():
    user_board = create_board()
    computer_board = create_board()

    user_ships = []
    computer_ships = []

    for size in [3, 2, 2, 1, 1, 1, 1]:
        user_ships.extend(place_ship(user_board, size))
        computer_ships.extend(place_ship(computer_board, size))

    print("Ваша доска:")
    print_board(user_board)

    user_previous_guesses = set()
    computer_previous_guesses = set()

    while True:
        user_guess_row, user_guess_col = user_turn(computer_board, user_previous_guesses)

        if (user_guess_row, user_guess_col) in computer_ships:
            print("Попадание!")
            computer_ships.remove((user_guess_row, user_guess_col))
            if is_ship_destroyed(user_ships, user_previous_guesses):
                print("Поздравляем! Вы потопили корабль противника!")
                if not computer_ships:
                    print("Вы победили!")
                    break
        else:
            print("Промах! Попробуйте снова.")
            computer_board[user_guess_row][user_guess_col] = "X"

        user_previous_guesses.add((user_guess_row, user_guess_col))

        display_hidden_board(computer_board, user_previous_guesses)

        while (user_guess_row, user_guess_col) in computer_ships:
            print("Отличный выстрел! У вас есть еще один ход.")
            user_guess_row, user_guess_col = user_turn(computer_board, user_previous_guesses)

            if (user_guess_row, user_guess_col) in computer_ships:
                print("Попадание!")
                computer_ships.remove((user_guess_row, user_guess_col))
                if is_ship_destroyed(user_ships, user_previous_guesses):
                    print("Поздравляем! Вы потопили корабль противника!")
                    if not computer_ships:
                        print("Вы потопили все корабли противника. Победа!")
                        break
            else:
                print("Промах! Попробуйте снова.")
                computer_board[user_guess_row][user_guess_col] = "X"

            user_previous_guesses.add((user_guess_row, user_guess_col))
            display_hidden_board(computer_board, user_previous_guesses)

        computer_guess_row, computer_guess_col = computer_turn(user_board, computer_previous_guesses)

        if (computer_guess_row, computer_guess_col) in user_ships:
            print("Противник потопил ваш корабль!")
            user_ships.remove((computer_guess_row, computer_guess_col))
            if not user_ships:
                print("Противник потопил все ваши корабли. Игра окончена.")
                break
        else:
            print("Противник промахнулся.")

        computer_previous_guesses.add((computer_guess_row, computer_guess_col))
        user_board[computer_guess_row][computer_guess_col] = "X"

        print("Ваша доска:")
        print_board(user_board)

        display_hidden_board(computer_board, user_previous_guesses)

if __name__ == "__main__":
    main()

#Динар