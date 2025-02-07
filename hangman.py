# Hangman

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import random

app=FastAPI()

origins = ['http://localhost:5173']
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Guess(BaseModel):
    guess:str

count = 0
wins = 0
losses = 0
words = [
    "Algorithm", "JavaScript", "Framework", "Encryption", "Data", "Programming", "Debugging", "Database", "Server", "Code","Elephant", "Kangaroo", "Giraffe", "Hippopotamus", "Lion", "Ostrich", "Dolphin", "Parrot", "Turtle", "Panda","Chair", "Television", "Lamp", "Smartphone", "Radio", "Book", "Shoes""Keyboard", "Clock", "Towel","Mountain", "Ocean", "River", "Desert", "Volcano", "Forest", "Waterfall", "Sunset", "Glacier", "Cloud","Pizza", "Sandwich", "Burger", "Pasta", "Cake", "Chocolate", "Soup", "Apple", "Salad", "Sandwich","Mountain", "Country", "Island", "Continent", "Ocean", "River", "Capital", "Desert", "Volcano", "City","Happiness", "Adventure", "Mystery", "Universe", "Science","Knowledge", "Discovery", "Hero", "Journey", "Freedom"
]
guessed = []
lives = 6
word = random.choice(words).upper()
visual = ["_" for _ in word]

@app.post("/check-letter",status_code=status.HTTP_200_OK)
async def check_letter(user:Guess):
    global count,wins,losses,lives,guessed,visual
    user.guess=user.guess.upper().strip()
    if not 'A' <= user.guess <= 'Z':
        raise HTTPException(status_code=422,detail="Invalid Input! Please guess a letter between 'A' to 'Z'!")
    if user.guess in guessed:
        raise HTTPException(status.HTTP_302_FOUND,detail=user.guess+" already guessed! Try another letter!")
    guessed.append(user.guess)
    if user.guess in word:
        for i in range(len(word)):
            if user.guess == word[i]:
                visual[i] = user.guess
        if "_" in visual:
            return{"Message":user.guess+" is present", "Guessed":guessed ,"Display":visual, "Lives":lives,"Game_Over":False}
        else:
            return{"Message":user.guess+" is present", "Additional_Message":"You Guessed the Word!", "Guessed":guessed ,"Display":visual,"Game_Over":True, "Lives":lives}
    else:
        lives-=1
        if lives == 0:
            visual = []
            for i in word:
                visual.append(i)
            return{"Message":"Game Over", "Guessed":guessed ,"Display":visual, "Lives":lives,"Game_Over":True}
        return{"Message":user.guess+" is not present", "Guessed":guessed, "Display":visual, "Lives":lives,"Game_Over":False}
    
@app.get("/word-length",status_code=status.HTTP_200_OK)
async def word_length():    
    return {"Length":len(word)}

@app.post("/reset",status_code=status.HTTP_200_OK)
async def reset():
    global count,wins,losses,lives,guessed,visual,word
    count=0
    wins=0
    losses=0
    lives=6
    guessed=[]
    word = random.choice(words).upper()
    visual = ["_" for _ in word]
    return {"Message":"Reset Success"}

# def continue_game():
#     play_again = input("Do you want to play again ? (Enter 'yes' or 'no'): ").strip().lower()
#     if play_again == "yes":
#         return
#     elif play_again == "no":
#         print(f"\nGames Played: {count}")
#         print(f"Games Won: {wins}")
#         print(f"Games Lost: {losses}")
#         print("\nThank you for playing HANGMAN!")
#         quit()
#     else:
#         print("Invalid input! Please enter 'yes' or 'no' : ")
#         return continue_game

# print("Welcome to HANGMAN!\nThe rules are simple.\nYou have to guess letters to guess the full word. If you guess a letter wrong, you lose a life.\n6 lives and you are out. ALL THE BEST!")
# count = 0
# wins = 0
# losses = 0

# while True:
#     count += 1
#     words=["APPLE","TABLE","RIVER","GRASS","CLOUD","ORANGE","MARKET","TRAVEL","FOREST","BRIDGE"]
#     word = random.choice(words)
#     visual = ["_" for _ in word]
#     guessed = []
#     lives = 6
#     print("".join(visual))
#     while lives !=0:
#         flag = 0
#         guess = input("\nGuess a letter: ").upper().strip()
#         if len(guess) != 1 or not 'A' <= guess <= 'Z':
#             print("Invalid Input! Please guess a single letter between 'a' to 'z'!")
#             continue
#         else:
#             if guess in guessed:
#                 print(f"You have already guessed {guess}! Try another letter!")
#                 continue
#             guessed.append(guess)
#             for i in range(len(word)):
#                 if guess == word[i]:
#                     visual[i] = guess
#                     flag = 1
#             if flag != 1:
#                 print(f"\n{guess} is not in the word")
#                 lives -=1
#             print("".join(visual))
#             print(f"\nGuessed letters: {"".join(guessed)}")
#             print(f"Lives: {lives}")
#             if not "_" in visual:
#                 print("Correct! You have guessed the word.\n")
#                 wins += 1
#                 break

#     if lives ==0:
#         print(f"\nYou ran out of lives!\nThe word was {word}.\n")
#         losses += 1

#     continue_game()