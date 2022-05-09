def RPS ():
    import random

    user_choice = input("Enter a choice (rock, paper, scissors)")
    possible_choice = ["rock", "paper", "scissors", "nothing"]
    computer_choice = random.choice(possible_choice)
    print(f"\nYou chose {user_choice}, computer chose {computer_choice}.\n")

    if user_choice == computer_choice:
        print(f"Both players selected {user_choice}. Drawing with a robot is losing unlucky!")
    elif user_choice == "rock":
        if computer_choice == "scissors":
            print("Rock beats scissors! WINNER!")
        else:
            print("Paper beats rock! LOSER!")
    elif user_choice == "paper":
        if computer_choice == "rock":
            print("Paper beats rock! WINNER!!")       
        else:
            print("Scissors beats paper! LOSER!")
    elif user_choice == "scissors":
        if computer_choice == "paper":
            print("Scissors beats paper! LOSER!")
        else:
            print("Rock beats scissors! LOSER!")
    elif user_choice or computer_choice == "nothing":
            print("Nothing chosen by one of the players game is void")
RPS()
