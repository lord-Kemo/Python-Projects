import csv
import requests
from fake_useragent import UserAgent
from http import HTTPStatus



def get_website(csv_path: str) -> list[str]:
    
    websites: list[str] = []
    
    with open(csv_path, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if 'https://' not in row[1] or 'http://' in row[1]:
                websites.append(f'https://{row[1]}')
            else:
                websites.append(row[1])
                
        return websites
    
    
def get_user_agent() -> str:
    ua = UserAgent()
    return ua.chrome

def get_status_code(status_code: int) -> str:
    for value in HTTPStatus:
        if status_code == status_code:
            description: str = f'({value} {value.name})  {value.description}'
        return description
    
    return 'Unknown status code '

def check_website(website: str, user_agent):
    try:
        code: int = requests.get(website, headers={'User-Agent': user_agent}).status_code
        print(website, get_status_code(code))
    except Exception:
        print(website, 'Error')
        
        
def main():
    site: list[str] = get_website('Games\websites.csv')
    user_agent: str = get_user_agent()
    for website in site:
        check_website(website, user_agent)
        

if __name__ == '__main__':
    main()