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
