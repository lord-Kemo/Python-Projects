import string
import secrets

def contains_uppercase(password: str) -> bool:
    for c in password:
        if c in string.ascii_uppercase:
            return True
    return False


def contains_symbols(password: str) -> bool:
    for c in password:
        if c in string.punctuation:
            return True
    return False


def generate_password(length: int, symbol: bool, uppercase: bool) -> str:
    combination: str = string.ascii_letters + string.digits
    
    if symbol:
        combination += string.punctuation
        
    if uppercase:
        combination += string.ascii_uppercase
        
    combination_length = len(combination)
    
    new_password = ' '
    
    for _ in range(length):
        new_password += combination[secrets.randbelow(combination_length)]
        
    return new_password





if __name__ == "__main__":
    for i in range(1, 6):
        new_pass: str = generate_password(length=25, symbol=True, uppercase=True)
        spec: str = f'U: {contains_uppercase(new_pass)} S: {contains_symbols(new_pass)}'
        print(f"{i}. {new_pass} ---> {spec}")
        
