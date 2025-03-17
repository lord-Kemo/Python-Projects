import random

def run_game() -> None:
    print("Welcome please choose: rock, paper or scissors as your choice in text.")
    print("You will play against the computer.")
    
    try:
        choice = input("Enter your choice >>  ")
        choice = choice.lower()
    except ValueError:
        print("Please enter a valid choice.")
        return
    
    map_choice = {0 : "rock", 1 : "paper", 2 : "scissors"}
    ai_choice = random.randint(0, 2)
    
    flag = True
    
    
    while flag:
        if choice == "rock":
            if map_choice[ai_choice] == "rock":
                print("It's a draw!")
            elif map_choice[ai_choice] == "paper":
                print("You lose!")
            else:
                print("You win!")
            flag = False
            print(f"You : {choice}")
            print(f"Computer : {map_choice[ai_choice]}")
        elif choice == "paper":
            if map_choice[ai_choice] == "rock":
                print("You win!")
            elif map_choice[ai_choice] == "paper":
                print("It's a draw!")
            else:
                print("You lose!")
            print(f"You : {choice}")
            print(f"Computer : {map_choice[ai_choice]}")
            flag = False
        elif choice == "scissors":
            if map_choice[ai_choice] == "rock":
                print("You lose!")
            elif map_choice[ai_choice] == "paper":
                print("You win!")
            else:
                print("It's a draw!")
            print(f"You : {choice}")
            print(f"Computer : {map_choice[ai_choice]}")
            flag = False
        else:
            print("Please enter a valid choice.")
            return
        


resume = True

while resume:
    run_game()
    print("Do you want to play again? (yes/no)")
    print("------")
    choice = input(">> ")
    if choice.lower() == "no":
        resume = False
    elif choice.lower() == "yes":
        resume = True
    else:
        print("Please enter a valid choice.")
        break

