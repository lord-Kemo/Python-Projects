import random

def roll_dice(amount: int = 2) -> list[int]:
    if amount <= 0:
        raise ValueError("The number of dice must be greater than 0.")
    
    rolls: list[int] = []
    for i in range(amount):
        random_roll: int = random.randint(1, 6)
        rolls.append(random_roll)
    return rolls
    
def main():
    while True:
        try:
            dice_amount: str = input("Enter the number of dice to roll: ")
            
            if dice_amount.lower() == "exit":
                print("Goodbye!")
                break
            
            dice_amount_int: int = int(dice_amount)
            rolls = roll_dice(dice_amount_int)
            print(*rolls, sep=", ")
            print(f'Total: {sum(rolls)}')
            
            
        except ValueError as e:
            print("Invalid input. Please enter a number.")
            continue
        
        
if __name__ == "__main__":  
    main()