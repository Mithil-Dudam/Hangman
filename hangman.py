# Hangman

import random

def continue_game():
    play_again = input("Do you want to play again ? (Enter 'yes' or 'no'): ").strip().lower()
    if play_again == "yes":
        return
    elif play_again == "no":
        print(f"\nGames Played: {count}")
        print(f"Games Won: {wins}")
        print(f"Games Lost: {losses}")
        print("\nThank you for playing HANGMAN!")
        quit()
    else:
        print("Invalid input! Please enter 'yes' or 'no' : ")
        return continue_game

print("Welcome to HANGMAN!\nThe rules are simple.\nYou have to guess letters to guess the full word. If you guess a letter wrong, you lose a life.\n6 lives and you are out. ALL THE BEST!")
count = 0
wins = 0
losses = 0

while True:
    count += 1
    words=["APPLE","TABLE","RIVER","GRASS","CLOUD","ORANGE","MARKET","TRAVEL","FOREST","BRIDGE"]
    word = random.choice(words)
    visual = ["_" for _ in word]
    guessed = []
    lives = 6
    print("".join(visual))
    while lives !=0:
        flag = 0
        guess = input("\nGuess a letter: ").upper().strip()
        if len(guess) != 1 or not 'A' <= guess <= 'Z':
            print("Invalid Input! Please guess a single letter between 'a' to 'z'!")
            continue
        else:
            if guess in guessed:
                print(f"You have already guessed {guess}! Try another letter!")
                continue
            guessed.append(guess)
            for i in range(len(word)):
                if guess == word[i]:
                    visual[i] = guess
                    flag = 1
            if flag != 1:
                print(f"\n{guess} is not in the word")
                lives -=1
            print("".join(visual))
            print(f"\nGuessed letters: {"".join(guessed)}")
            print(f"Lives: {lives}")
            if not "_" in visual:
                print("Correct! You have guessed the word.\n")
                wins += 1
                break

    if lives ==0:
        print(f"\nYou ran out of lives!\nThe word was {word}.\n")
        losses += 1

    continue_game()