import random
from config import CHOICES

def get_bot_choice():
    return random.choice(list(CHOICES.keys()))

def determine_winner(user_choice: str, bot_choice: str)->str:
    if user_choice == bot_choice:
        return "draw"
    elif user_choice == "rock" and bot_choice == "scissors":
        return "win"
    elif user_choice == "paper" and bot_choice == "rock":
        return "win"
    elif user_choice == "scissors" and bot_choice == "paper":
        return "win"
    else:
        return "lose"
    
