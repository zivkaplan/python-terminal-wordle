import string
from random import randint
import os

def _ClearScreen():
    clear_command = "clear"
    if os.name == 'nt':
        clear_command = "cls"
        
    os.system(clear_command)

class _Colors:
    RESET = "\033[0m"
    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"
    BOLD_BLACK = "\033[1m\033[30m"      
    BOLD_RED = "\033[1m\033[31m"      
    BOLD_GREEN = "\033[1m\033[32m"      
    BOLD_YELLOW = "\033[1m\033[33m"      
    BOLD_BLUE = "\033[1m\033[34m"      
    BOLD_MAGENTA = "\033[1m\033[35m"      
    BOLD_CYAN = "\033[1m\033[36m"      
    BOLD_WHITE = "\033[1m\033[37m"
    DIMMED = "\x1b[2m"


class _Letter:
    def __init__(self, letter, color=_Colors.BOLD_WHITE):
        self._letter = letter
        self._color = color
    
    def Print(self, end="\n"):
        print(f"{self._color + self._letter + _Colors.RESET}", end=end)


    def ChangeColor(self, color):
        self._color = color


class _Dict:
    def __init__(self):
        self._content = self._LoadDict()

    def _LoadDict(self):
        file_location = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "words.txt")
        
        with open(file_location, "r") as dict:
            return [line.split()[0].upper() for line in dict]

    def GetRandomWord(self):
        return self._content[randint(0, len(self._content) -1)]

    def Exists(self, key):
        return key in self._content


class Wordle:
    def __init__(self):
        self._MAX_ROUNDS = 6
        self._dictionary = _Dict()
    
    def _ReInit(self):
        self._secret_word = self._GetSecretWord()
        self._guesses_letters = {
            letter: _Letter(letter) for letter in string.ascii_uppercase }
        self._keyboard = {
            letter: _Letter(letter) for letter in string.ascii_uppercase }
        self._current_round = 0
        self._guesses = [[] for _ in range(self._MAX_ROUNDS)]

    def _GetSecretWord(self):
        """
        a method to chose new secret word for the game
        """
        SECRET_WORD_LENGTH = 5
        word = self._dictionary.GetRandomWord()
        while (not word.isalpha()) or (len(word) != SECRET_WORD_LENGTH):
            word = self._dictionary.GetRandomWord()
        return word


    def _DetermineColor(self, letter):
        color = _Colors.WHITE
        if letter in self._guesses:
            color = _Colors.DIMMED
        if letter in self._secret_word:
            color += _Colors.GREEN
        return color


    def _PrintKeyboard(self):
        for letter in self._keyboard.values():
            letter.Print(end=" ")
        print() # newline


    def _PrintGuesses(self):
        for idx, guess in enumerate(self._guesses):
            print(f"{_Colors.DIMMED + _Colors.CYAN}{idx + 1} > {_Colors.RESET}", end="")
            for letter in guess:
                letter.Print(end=" ")
            print() # new line


    def _analyze_guess(self, guess):
        color = None
        for idx, letter in enumerate(guess):
            if letter in self._secret_word:
                if letter == self._secret_word[idx]:
                    color = _Colors.BOLD_GREEN
                else:
                    color = _Colors.BOLD_YELLOW   
            else:
                color = _Colors.BOLD_RED

            self._guesses[self._current_round].append(_Letter(letter,color))
            self._keyboard[letter].ChangeColor(_Colors.DIMMED + color)


    def _ValidateGuess(self, guess):
        return (guess.isalpha() and 
                len(guess) == 5 and
                self._dictionary.Exists(guess))


    def _PrintWinScreen(self):
        print(f"\n{_Colors.BOLD_GREEN}Success!")
        print(f"You have guessed the word ", end="")
        print(f"{_Colors.BOLD_CYAN + self._secret_word} ", end="")
        print(f"{_Colors.BOLD_GREEN}correctly!{_Colors.RESET}")


    def _PrintLoseScreen(self):
        print(f"{_Colors.BOLD_RED}Game Over!")
        print(f"The secret word was {_Colors.BOLD_YELLOW + self._secret_word}.")
        print(f"{_Colors.BOLD_MAGENTA}Better luck next time!{_Colors.RESET}")


    def Start(self):
        """
        Start new game
        """        
        self._ReInit()
        
        was_invalid_guess = False
        has_guessed_correctly = False
        while self._current_round < self._MAX_ROUNDS and not has_guessed_correctly:
            _ClearScreen()
            
            if was_invalid_guess:
                print(f"{_Colors.BOLD_WHITE}Invalid guess{_Colors.RESET}")
                was_invalid_guess = False
            
            self._PrintGuesses()
            self._PrintKeyboard()
            new_guess = input("Enter your guess:\n").upper()
            if not self._ValidateGuess(new_guess):
                was_invalid_guess = True
                
            else:
                has_guessed_correctly = new_guess == self._secret_word
                self._analyze_guess(new_guess)
                self._current_round += 1
                
                
        if has_guessed_correctly:
            self._PrintWinScreen()
        else:
            self._PrintLoseScreen()