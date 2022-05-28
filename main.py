from wordle import Wordle

def ParseChoice(choice):
    while True:
        choice = choice.upper()
        if choice in ["Y","YES"]:
            return True
        elif choice in ["N","NO"]:
            return False
        else:
            choice = input("invalid input. Try again:\n")
            
    

def main():
    
    game = Wordle()
    is_playing = True
    while is_playing:
        game.Start()
        is_playing = ParseChoice(input("Would you like to play again? [Y/n]"))
        


if __name__ == "__main__":
    main()
