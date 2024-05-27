from dotenv import load_dotenv
import os
import requests
from bs4 import BeautifulSoup
import re
import pandas as pd

load_dotenv()
API_KEY = os.getenv('API_KEY')
SEARCH_ENGINE_ID = os.getenv('SEARCH_ENGINE_ID')
NUM_REQUESTS = 60

def get_homepage(name:str) -> str:
    
    query = f'{name} contactos'
    url = 'https://www.googleapis.com/customsearch/v1'
    params = {
        'q': query,
        'key': API_KEY,
        'cx': SEARCH_ENGINE_ID
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

def populate_email() -> list:
    
    df = pd.read_excel('entities.xlsx')
    df_filtered = df[df['emails'] != ''] if df['emails'] else df['emails'] == ''    
    
    for i in range(NUM_REQUESTS):
        
        entity_name = list(df_filtered['NOMBRE ORGANIZACIÓN'])[i]
        url = get_homepage(name = entity_name)
        emails = ', '.join(get_emails(url=url))
        df_filtered['emails'][i] = emails
        
    df.join(df_filtered[['NOMBRE ORGANIZACIÓN', 'emails']], on='NOMBRE ORGANIZACIÓN')
    df.to_csv('output.csv')
        

if __name__ == '__main__':
    
    populate_email()