from dotenv import load_dotenv
import os
import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
from tqdm import tqdm

load_dotenv()
API_KEY = os.getenv('API_KEY')
SEARCH_ENGINE_ID = os.getenv('SEARCH_ENGINE_ID')
NUM_REQUESTS = 6

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

def get_emails(url:str):
    
    emails = []
    
    try:
    
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        for link in soup.findAll("a", attrs = {"href": re.compile("^mailto:")}):
            
            email = str(link.get('href').replace('mailto:', ''))
            emails.append(email)
    
    except:
        pass
    
    return emails

def populate_email() -> None:
    
    df = pd.read_excel('entities.xlsx')
    df_filtered = df[df['homepage'] != '']
    
    for index, row in tqdm(df_filtered.iterrows()):
        
        entity_name = row['NOMBRE ORGANIZACIÓN']
        homepage = get_homepage(name=entity_name)['link']
        df_filtered.loc[index, 'homepage'] = homepage
    
    merged_df = df.merge(
        df_filtered[['NOMBRE ORGANIZACIÓN', 'emails']],
        on='NOMBRE ORGANIZACIÓN',
        how='left')
    
    merged_df.to_csv('output.csv', index=False)
        

if __name__ == '__main__':
    
    populate_email()