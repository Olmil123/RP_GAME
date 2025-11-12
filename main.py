from game.models import Player
from game.game import Game
from game.score import ScoreHandler
from game.settings import MODES, SCORE_FILE


def create_player() -> tuple[Player, str]:
    name = input("Enter your name: ")
    print("Choose game mode:")
    for key, mode_name in MODES.items():
        print(f"{key} - {mode_name}")

    mode_choice = None
    while mode_choice not in MODES:
        mode_choice = input("Your choice (1/2):")
        if mode_choice not in MODES:
            print("Incorrect input, please try again")
    mode = MODES[mode_choice]
    player = Player(name)
    return player, mode


def play_game():
    player, mode = create_player()
    game = Game(player=player, mode=mode)
    game.play()


def show_scores():
    handler = ScoreHandler(SCORE_FILE)
    handler.display()


def exit_game():
    print("Bye daddy!)")


def main():
    while True:
        print("\n--- Rock-Paper-Scissors Game from Sasha ---")
        print("1 - Play game")
        print("2 - Show scores")
        print("3 - Exit")

        choice = input("Your choice: ")
        if choice == "1":
            play_game()
        elif choice == "2":
            show_scores()
        elif choice == "3":
            exit_game()
            break
        else:
            print("Incorect input, pls try again!")


if __name__ == "__main__":
    main()
