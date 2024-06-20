import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import time
import html

# Function to retrieve HTML content of search results page
def get_data(url):
    r = requests.get(url)
    data = r.json()
    return data['results_html']

# Function to parse individual game entries and extract price information
def parse(game):
    title_txt = game.find('span', {'class': 'title'}).text.strip().replace('¢', '').replace('®', '').replace(',', '').replace('™', '')
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

def parse_review(game):
    # Extracting review data from tooltip data
    review_summary = game.find('span', {'class': 'search_review_summary'})
    if review_summary:
        tooltip_html = review_summary['data-tooltip-html']
        review_match = re.search(r'(\w+\s?\w*)<br>(\d+)% of the ([\d,]+) user reviews for this game are positive', tooltip_html)
        if review_match:
            review_data = review_match.group(1)
            percent_review = int(review_match.group(2))
            total_review = int(review_match.group(3).replace(',', ''))
            return {
                'review_data': review_data,
                'percent_review': percent_review,
                'total_review': total_review
            }
    return {
        'review_data': 'No Data',
        'percent_review': 0,
        'total_review': 0
    }


# Main function to execute the scraping process
def main():
    results = []
    rank = 1
    # Looping through multiple pages of search results (50 games per page)
    for x in range(0, 200, 50):
        data = get_data(f'https://store.steampowered.com/search/results/?query&start={x}&count=50&dynamic_data=&sort_by=_ASC&snr=1_7_7_7000_7&filter=topsellers&tags=19&infinite=1')
        soup = BeautifulSoup(data, 'html.parser')
        games = soup.find_all('a', {'class': 'search_result_row'})
        
        # Parsing and filtering out None values for price data
        parsed_results_price = [parse(game) for game in games]
        games_df_price = pd.DataFrame(parsed_results_price)
        
        # Parsing and filtering out None values for review data
        parsed_results_review = [parse_review(game) for game in games if parse_review(game) is not None]
        games_df_review = pd.DataFrame(parsed_results_review)
        
        # Combine price and review data
        games_df_combined = pd.concat([games_df_price, games_df_review], axis=1)
        
        # Add 'Rank' column
        games_df_combined['rank'] = range(rank, rank + len(games_df_combined))
        rank += len(games_df_combined)  # Increment rank counter
        
        # Move 'Rank' column to the left side
        games_df_combined = games_df_combined[['rank'] + [col for col in games_df_combined.columns if col != 'rank']]
        
        # Append the combined DataFrame to the results list
        results.append(games_df_combined)
        
        print('Results Scraped:', x)
        # Adding a delay between requests to avoid rate limiting
        time.sleep(1.5)

    # Combining and saving the results
    games_df = pd.concat(results, ignore_index=True)
    games_df.to_csv('games_data.csv', index=False)
    
    print('Finished. Saved to CSV')
    print(games_df.head())


if __name__ == "__main__":
    main()