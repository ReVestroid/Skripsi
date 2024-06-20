import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

url = 'https://store.steampowered.com/search/results/?query&start=0&count=50&dynamic_data=&sort_by=_ASC&snr=1_7_7_7000_7&filter=topsellers&tags=19&infinite=1'

def total_results(url):
    r = requests.get(url)
    data = r.json()
    total_results = data['total_count']
    return int(total_results)

def get_data(url):
    r = requests.get(url)
    data = r.json()
    return data['results_html']

def get_review(url):
    r = requests.get(url)
    data = r.json()
    return data['results_html']

def parse(game):
    title_txt = game.find('span', {'class': 'title'}).text.strip().replace('¢', '').replace('®', '').replace(',', '')
    title = str(title_txt)
    
    price_txt = game.find('div', {'class': 'discount_original_price'})
    disc_price_txt = game.find('div', {'class': 'discount_final_price'})
    if price_txt is None:
        price_txt = "0"
    elif price_txt:
        price_txt = price_txt.text.strip().replace('Rp', '').replace(' ', '')
        
    if disc_price_txt is None:
        price_txt = "0"
    elif disc_price_txt:
        disc_price_txt = disc_price_txt.text.strip().replace('Rp', '').replace(' ', '')        
    
    if disc_price_txt == 'Free':
        disc_price_txt = price_txt
    elif price_txt == "0" :
        price_txt = disc_price_txt

    price = int(price_txt or 0)
    disc_price = int(disc_price_txt or 0)
    
    if disc_price > 0 :
        persen_disc = int(((price - disc_price) / price) * 100)
    else :
        persen_disc = 0
    
    return {
        'title': str(title),
        'price': price,
        'disc_price': disc_price,
        'persen_disc': round(persen_disc,1)
    }

def output(results):
    games_df = pd.concat(results, ignore_index=True)
    games_df.to_csv('games_price.csv', index=False)
    print('Finished. Saved to CSV')
    print(games_df.head())
    return

results = []
for x in range(0, 100, 50):
    data = get_data(f'https://store.steampowered.com/search/results/?query&start={x}&count=50&dynamic_data=&sort_by=_ASC&snr=1_7_7_7000_7&filter=topsellers&tags=19&infinite=1')
    soup = BeautifulSoup(data, 'html.parser')
    games = soup.find_all('a', {'class': 'search_result_row'})
    results.append(pd.DataFrame([parse(game) for game in games]))
    print('Results Scraped:', x)
    time.sleep(1.5)

output(results)

#totalresults(url)