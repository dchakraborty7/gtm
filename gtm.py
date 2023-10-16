import chess.engine
import chess.pgn

def evaluate_position(fen, path_to_stockfish):
    with chess.engine.SimpleEngine.popen_uci(path_to_stockfish) as engine:
        info = engine.analyse(chess.Board(fen), chess.engine.Limit(time=1))
        return info["score"].relative.score()

def play_guess_the_move(game, path_to_stockfish):
    board = game.board()
    correct_moves = []
    incorrect_moves = []

    print("Guess the moves of the winning side (White)!\n")
    white_turn = True
    idx = 0  # Initialize move index

    for move in game.mainline_moves():
        idx += 1  # Increment move index
        print(f"Move {idx}. FEN: {board.fen()}")
        print(f"Position Evaluation: {evaluate_position(board.fen(), path_to_stockfish)}")

        if white_turn:
            print(f"Your guess (UCI format, e.g., 'e2e4'): ")
            guess = input()

            if guess.lower() == board.san(move).lower() or guess.lower() == move.uci()[:4].lower():
                print("Correct!")
                correct_moves.append((idx, move.uci()[:4]))  # Store correct move in start-destination format
            else:
                print("Incorrect.")
                incorrect_moves.append((idx, move.uci()[:4]))  # Store incorrect move in start-destination format

            print(f"Winner's move: {move.uci()[:4]}")

            # Apply the move to the board
            board.push(move)

        else:
            # Automatically play Black's moves
            board.push(move)

        white_turn = not white_turn

    print("\nGame Over!")
    print("Correct Moves:")
    for move in correct_moves:
        print(f"Move {move[0]}. {move[1]}")
    print("\nIncorrect Moves:")
    for move in incorrect_moves:
        print(f"Move {move[0]}. {move[1]}")

if __name__ == "__main__":
    pgn_file = "niemann_petrov_2023.pgn"  # Replace with the path to your PGN file
    with open(pgn_file) as pgn:
        game = chess.pgn.read_game(pgn)
    path_to_stockfish = "./Stockfish/src/stockfish"  # Replace with the correct path to Stockfish
    play_guess_the_move(game, path_to_stockfish)
