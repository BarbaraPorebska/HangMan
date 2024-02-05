import random
from colorama import init
from colorama import Fore, Back, Style
init(autoreset=True)

HANGMANPICS = ['''
  +---+
  |   |
      |
      |
      |
      |
=========''', '''
  +---+
  |   |
  O   |
      |
      |
      |
=========''', '''
  +---+
  |   |
  O   |
  |   |
      |
      |
=========''', '''
  +---+
  |   |
  O   |
 /|   |
      |
      |
=========''', '''
  +---+
  |   |
  O   |
 /|\  |
      |
      |
=========''', '''
  +---+
  |   |
  O   |
 /|\  |
 /    |
      |
=========''', '''
  +---+
  |   |
  O   |
 /|\  |
 / \  |
      |
=========''']

with open("countries-and-capitals.txt", "r") as file:
    countries_cities = file.read()

countries_cities = countries_cities.split('\n')
countries = [i.split(' | ')[0] for i in countries_cities]
cities = [i.split(' | ')[-1] for i in countries_cities]

while True:
    already_tried_letters = []
    wrong_letters = []

    result = ""
    word_to_guess = ""

    start_again = False
    quit = False

    print(f"\n{Fore.MAGENTA}Welcome to the Hangman!")
    print("\n[Type QUIT to exit anytime you want]\n")
    while True:
        print("Available difficulties:")
        print(Fore.GREEN + "1 [easy] - countries, 7 lives")
        print(Fore.YELLOW + "2 [medium] - capitals, 5 lives")
        print(Fore.RED + "3 [hard] - random country or capital, 4 lives")
        print(Back.RED + "4 [nightmare] - random country or capital, only long words, 3 lives")
        difficulty = input("Choose difficulty (1-4): ")
        difficulty = difficulty.upper()
        if difficulty == "1":
            lives = 7
            word_to_guess = random.choice(countries)
            break
        elif difficulty == "2":
            lives = 5
            word_to_guess = random.choice(cities)
            break
        elif difficulty == "3":
            lives = 4
            word_to_guess = random.choice(cities + countries)
            break
        elif difficulty == "4":
            lives = 3
            while len(word_to_guess) < 10:
                word_to_guess = random.choice(cities + countries)
            break
        elif difficulty == "QUIT":
            quit = True
            lives = 0
            break
        else:
            print("Please choose a number between 1 and 4")

    for character in word_to_guess:
        if character == " ":
            result += "  "
        else:
            result += "_ "

    print(result)

    while lives > 0:
        if (difficulty == "1" and lives != 7) or (difficulty == "2" and lives != 5) \
            or (difficulty == "3" and lives != 4) or (difficulty == "4" and lives != 3):
            if lives >= 4:
                print(Fore.GREEN + HANGMANPICS[-(lives-6)])
            else:
                print(Fore.YELLOW + HANGMANPICS[-(lives-6)])
        print(f"\nYou've got {lives} lives left")
        while True:
            typed_letter = input("Please choose a letter or type guessed word: ")
            typed_letter = typed_letter.upper()
            if typed_letter.isalpha() == True and len(typed_letter) == 1:
                if typed_letter in already_tried_letters:
                    print("You already typed this letter")
                else:
                    already_tried_letters.append(typed_letter)
                    break
            elif typed_letter == word_to_guess.upper():
                already_tried_letters = list(typed_letter)
                break
            elif len(typed_letter) == len(word_to_guess):
                print("Wrong word!")
                break
            elif typed_letter == "QUIT":
                quit = True
                break
            else:
                print("\nPlease type one letter")    
        if quit == True:
            break

        last_result = result
        result = ""
        for character in word_to_guess:
            if character in already_tried_letters or character.upper() in already_tried_letters or character == " ":
                result += f"{Fore.GREEN}{character}{Style.RESET_ALL}"+" "
            else:
                result += "_ "
        print(result)

        word_without_spaces = word_to_guess.replace(" ", "")
        
        win = all(item in already_tried_letters for item in word_without_spaces.upper())

        if win == True:
            print(f"\n{Fore.GREEN}You win!{Style.RESET_ALL} The password was {Fore.GREEN + word_to_guess}")
            while True:
                again = input("Do you want to play again? Y/N ")
                again = again.upper()
                if again == "Y":
                    start_again = True
                    break
                elif again == "N":
                    quit = True
                    break
                else:
                    print("\nPlease type \"Y\" or \"N\"")
        elif result == last_result:
            lives -= 1
            wrong_letters.append(typed_letter)
            print("\nWrong answer! Your wrong answers are:", Fore.RED + ", ".join(wrong_letters))
            if lives == 0:
                print(Fore.RED + HANGMANPICS[6])
                print(f"{Fore.RED}You lose!{Style.RESET_ALL} The password was {Fore.RED + word_to_guess}")
                while True:
                    again = input("Do you want to play again? Y/N ")
                    again = again.upper()
                    if again == "Y":
                        start_again = True
                        break
                    elif again == "N":
                        quit = True
                        break
                    else:
                        print("\nPlease type \"Y\" or \"N\"")
        if start_again == True or quit == True:
            break
    if quit == True:
        print("\nGoodbye!")
        break