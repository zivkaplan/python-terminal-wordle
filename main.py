from wordle import Wordle


def parse_choice(choice):
    while True:
        choice = choice.upper()
        if choice in ["Y", "YES"]:
            return True
        elif choice in ["N", "NO"]:
            return False
        else:
            choice = input("invalid input. Try again: ")


def main():
    game = Wordle()
    is_playing = True
    while is_playing:
        game.start()
        is_playing = parse_choice(input("Would you like to play again? [Y/n]: "))


if __name__ == "__main__":
    main()
