import chess.pgn

def load_chess_game(file_path):
    try:
        pgn = open(file_path)
        game = chess.pgn.read_game(pgn)
        return game
    except Exception as e:
        print(f"Error loading the chess game: {e}")
        return None

def determine_winner(game):
    result = game.headers.get("Result", "*")
    if result == "1-0":
        return "White"
    elif result == "0-1":
        return "Black"
    else:
        return None

def play_guess_the_move(game):
    board = game.board()
    moves = list(game.mainline_moves())
    correct_moves = []
    incorrect_moves = []
    winner = determine_winner(game)

    if winner is None:
        print("Unable to determine the winner.")
        return

    print(f"Guess the moves of the winning side ({winner})!\n")

    for idx, move in enumerate(moves):
        if (idx % 2 == 0 and winner == "White") or (idx % 2 != 0 and winner == "Black"):
            print(f"Move {idx // 2 + 1}. Your guess: ")
            guess = input()

            if guess.lower() == board.san(move).lower() or guess.lower() == move.uci()[:4].lower():
                print("Correct!")
                correct_moves.append((idx // 2 + 1, move.uci()[:4]))  # Store correct move in start-destination format
            else:
                print("Incorrect.")
                incorrect_moves.append((idx // 2 + 1, move.uci()[:4]))  # Store incorrect move in start-destination format

            # Print the winner's move in start-destination format
            print(f"Winner's move: {move.uci()[:4]}")

            # Print the opponent's move
            if idx + 1 < len(moves):
                opponent_move = moves[idx + 1]
                opponent_move_str = opponent_move.uci()[:4]  # Convert to start-destination UCI format
                print(f"Opponent's move: {opponent_move_str}")

            board.push(move)

    print("\nGame Over!")
    print("Correct Moves:")
    for move in correct_moves:
        print(f"Move {move[0]}. {move[1]}")
    print("\nIncorrect Moves:")
    for move in incorrect_moves:
        print(f"Move {move[0]}. {move[1]}")

if __name__ == "__main__":
    file_path = "niemann_petrov_2023.pgn"  # Set the file path to your specific PGN file
    game = load_chess_game(file_path)

    if game:
        play_guess_the_move(game)
