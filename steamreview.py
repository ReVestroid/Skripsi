import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import time

# Function to retrieve HTML content of search results page
def get_data(url):
    r = requests.get(url)
    data = r.json()
    return data['results_html']

# Function to parse individual game entries and extract review summary and tooltip data
def parse(game):
    # Extracting tooltip data
    tooltip_data_elem = game.find('span', {'data-tooltip-html': True})
    tooltip_data = tooltip_data_elem['data-tooltip-html'] if tooltip_data_elem else "No Data"
    
    # Check if the tooltip data contains the exclusion message
    if "This product has experienced one or more periods of off-topic review activity." in tooltip_data:
        # If it does, return None to indicate that this entry should be excluded
        return None
    
    # Extracting review data and total review from tooltip data
    review_match = re.search(r'(\w+\s?\w*)<br>(\d+)% of the ([\d,]+) user reviews for this game are positive', tooltip_data)
    review_data = review_match.group(1) if review_match else "No Data"
    percent_review = int(review_match.group(2)) if review_match else 0
    total_review = int(review_match.group(3).replace(',', '')) if review_match else 0
    
    # Determine data types
    data_types = {
        'review_data': type(review_data).__name__,
        'percent_review': type(percent_review).__name__,
        'total_review': type(total_review).__name__
    }
    
    return {
        'review_data': review_data,
        'percent_review': percent_review,
        'total_review': total_review,
        'data_types': data_types
    }


# Main function to execute the scraping process
def main():
    results = []
    # Looping through multiple pages of search results (50 games per page)
    for x in range(0, 100, 50):
        data = get_data(f'https://store.steampowered.com/search/results/?query&start={x}&count=50&dynamic_data=&sort_by=_ASC&snr=1_7_7_7000_7&filter=topsellers&tags=19&infinite=1')
        soup = BeautifulSoup(data, 'html.parser')
        games = soup.find_all('a', {'class': 'search_result_row'})
        # Parsing and filtering out None values
        parsed_results = [parse(game) for game in games if parse(game) is not None]
        results.append(pd.DataFrame(parsed_results))
        print('Results Scraped:', x)
        # Adding a delay between requests to avoid rate limiting
        time.sleep(1.5)

    # Combining and saving the results
    games_df = pd.concat(results, ignore_index=True)
    games_df.to_csv('games_review_tooltip.csv', index=False)
    print('Finished. Saved to CSV')
    print(games_df.head())


if __name__ == "__main__":
    main()

