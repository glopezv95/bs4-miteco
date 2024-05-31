import requests
from bs4 import BeautifulSoup
import re

def get_homepage(name:str, key:str, cx: str) -> dict:
    
    query = f'{name} contactos'
    url = 'https://www.googleapis.com/customsearch/v1'
    params = {
        'q': query,
        'key': key,
        'cx': cx
    }
    
    response = requests.get(url = url, params = params)
    data = dict(response.json())
        
    title = data['items'][0]['title']
    link = data['items'][0]['link']
    output = {'title': title, 'link': link}

    return output

def get_emails(url:str) -> str:
    
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    print(soup)
    
    emails = []
    
    for link in soup.findAll("a", attrs = {"href": re.compile("^mailto:")}):
        
        email = link.get('href').replace('mailto:', '')
        emails.append(email)
        
    return emails