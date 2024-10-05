import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

# Function to scrape articles from Reuters Finance section
def scrape_financial_news():
    url = 'https://www.reuters.com/business/economy/'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Container that holds the articles
    articles = soup.find_all('article')

    news_data = []

    for article in articles:
        # Get title, description, and link of the article
        title = article.find('h2').get_text(strip=True) if article.find('h2') else None
        description = article.find('p').get_text(strip=True) if article.find('p') else None
        link = article.find('a')['href'] if article.find('a') else None
        if link and not link.startswith('https'):
            link = f"https://www.reuters.com{link}"

        if title and description and link:
            news_data.append({
                'title': title,
                'description': description,
                'link': link,
                'scraped_at': datetime.now()
            })

    return news_data

# Function to save news data into a pandas DataFrame
def save_news_to_dataframe(news_data):
    # Create DataFrame
    df = pd.DataFrame(news_data)
    
    # Save to CSV for further analysis
    df.to_csv('financial_news.csv', index=False)

    return df

if __name__ == "__main__":
    # Scrape news
    news_data = scrape_financial_news()

    # Save to dataframe
    df = save_news_to_dataframe(news_data)

    # Display scraped data
    print(df.head())
