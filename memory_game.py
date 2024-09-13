import random


def init_game() -> dict[str, any]:
    rows = 4
    columns = 4
    cards: list[str] = ['A', 'A', 'B', 'B', 'C', 'C', 'D', 'D', 'E', 'E', 'F', 'F', 'G', 'G', 'H', 'H']

    game_data: dict[str, any] = {
        'rows': rows,
        'columns': columns,
        'score': {'player1': 0, 'player2': 0},
        'turn': 'player1',
        'game_over': False,
        'board': prepare_board(rows, columns, cards),
        'move_history': []
    }
    return game_data


def prepare_board(rows: int, columns: int, cards: list[str]) ->\
        dict[tuple[int, int], dict[str, any]]:
    random.shuffle(cards)
    board: dict[tuple[int, int], dict[str, any]] = {}
    card_index = 0

    for row in range(rows):
        for col in range(columns):
            board[(row, col)] = {'card': cards[card_index],
                                 'flipped': False, 'matched': False}
            card_index += 1

    return board


def display_board(game_data: dict[str, any]) -> None:
    board: dict[tuple[int, int], dict[str, any]] = game_data['board']
    rows: int = game_data['rows']
    columns: int = game_data['columns']

    print("\nCurrent Board:\n")
    print("    ", end=" ")
    print("   ".join(str(col) for col in range(columns)))

    print("   +" + "---+" * columns)


    for row in range(rows):
        print(f" {row} |", end="")
        for col in range(columns):
            cell: dict[str, any] = board[(row, col)]
            if cell['flipped'] or cell['matched']:
                print(f" {cell['card']} ", end=" ")
            else:
                print(" * ", end=" ")
        print()

    print("   +" + "---+" * columns)  # Separator line



def get_valid_card(game_data: dict[str, any]) -> tuple[int, int]:
    rows: int = game_data['rows'];
    columns: int = game_data['columns'];
    board: dict[tuple[int, int], dict[str, any]] = game_data['board'];

    while True:
        try:
            row: int = int(input(f"Enter the row number (0 to {rows - 1}): "));
            col: int = int(input(f"Enter the column number (0 to {columns - 1}): "));

            if (row, col) not in board:
                raise ValueError("Invalid position.");
            if board[(row, col)]['flipped'] or board[(row, col)]['matched']:
                raise ValueError("Card already flipped or matched.");

            return row, col;

        except ValueError as e:
            print(f"Error: {e}. Please try again.");


def check_match(game_data: dict[str, any], pos1: tuple[int, int], pos2: tuple[int, int]) -> bool:
    board: dict[tuple[int, int], dict[str, any]] = game_data['board'];
    return board[pos1]['card'] == board[pos2]['card'];


def flip_back_cards(game_data: dict[str, any], pos1: tuple[int, int], pos2: tuple[int, int]) -> None:
    board: dict[tuple[int, int], dict[str, any]] = game_data['board'];
    board[pos1]['flipped'] = False;
    board[pos2]['flipped'] = False;


def play(game_data: dict[str, any]) -> None:
    display_board(game_data)

    while True:
        while not game_data['game_over']:
            for player in ['player1', 'player2']:
                if game_data['game_over']:
                    break  # Exit the loop if the game is over

                game_data['turn'] = player
                player_has_another_turn: bool = True  # control consecutive turns

                while player_has_another_turn:
                    print(f"\n{player}'s turn:")

                    # Player selects the first card
                    guess1 = get_valid_card(game_data)
                    game_data['board'][guess1]['flipped'] = True;
                    display_board(game_data)

                    # Player selects the second card
                    guess2: tuple[int, int] = get_valid_card(game_data)
                    game_data['board'][guess2]['flipped'] = True
                    display_board(game_data)

                    # Record the move
                    game_data['move_history'].append({
                        'player': player,
                        'guesses': [guess1, guess2],
                        'matched': check_match(game_data, guess1, guess2)
                    })

                    if game_data['move_history'][-1]['matched']:
                        print("It's a match!");
                        game_data['board'][guess1]['matched'] = True
                        game_data['board'][guess2]['matched'] = True
                        game_data['score'][player] += 1
                    else:
                        print('Not a match')
                        flip_back_cards(game_data, guess1, guess2)
                        player_has_another_turn = False  # End the turn for this player

                    # Check if the game is over
                    if all(cell['matched'] for cell in game_data['board'].values()):
                        game_data['game_over'] = True  # End the game
                        player_has_another_turn = False

        print("\nGame Over!")
        player1_score: int = game_data['score']['player1']
        player2_score: int = game_data['score']['player2']
        print(f"Final Scores: Player 1: {player1_score}, Player 2: {player2_score}")

        if player1_score > player2_score:
            print("Player 1 wins!")
        elif player2_score > player1_score:
            print("Player 2 wins!")
        else:
            print("It's a tie!")

        # Print the move history
        print("\nMove History:")
        for i, move in enumerate(game_data['move_history']):
            player = move['player']
            guess1, guess2 = move['guesses']
            matched = "Matched" if move['matched'] else "Did not match"
            print(f"Move {i + 1}: {player} guessed {guess1} and {guess2} - {matched}")

        # Ask if the players want to start a new game or quit
        while True:
            choice: str = input("Would you like to start a new game or quit? (new/quit): ").strip().lower();
            if choice == "new":
                game_data = init_game()  # Reinitialize the game data for a new game
                break;  # Start the new game loop
            elif choice == "quit":
                print("Thanks for playing!")
                return  # end the game
            else:
                print("Invalid choice. Please enter 'new' to start a new game or 'quit' to exit.");


if __name__ == "__main__":
    game_data = init_game()
    play(game_data)
