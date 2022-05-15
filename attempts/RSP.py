# rock-paper-scissors game
import random

while True:
    possible_actions = ["rock", "paper", "scissors"]
    your_card = input("What's your move? Enter either rock, paper, or scissors: ")
    com_card = random.choice(possible_actions)
    print(f"\nYou chose {your_card}, computer chose {com_card}.\n")

    if your_card.lower() == com_card:
        print(f"Both players selected {your_card}. It's a tie!")
    elif your_card.lower() == "rock":
        if com_card == "scissors":
            print("Rock smashes scissors! You win!")
        else:
            print("Paper covers rock! You lose.")
    elif your_card.lower() == "scissors":
        if com_card == "paper":
            print("Scissors cut paper! You win!")
        else:
            print("Rock smashes scissors! You lose.")
    elif your_card.lower() == "paper":
        if com_card == "rock":
            print("Paper covers rock! You win!")
        else:
            print("Scissors cut paper! You lose.")

    play_again = input("Play again? Enter y/n: ")
    if play_again.lower() == "n" or "no":
        False
    elif play_again.lower() == "y" or "yes":
        True

