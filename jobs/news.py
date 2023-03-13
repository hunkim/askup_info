import requests
import datetime
import os
import time
from newspaper import Article

from chatgpt import summary

NEWS_API_KEY = os.environ["NEWS_API_KEY"]

def get_url_text(url):
    try:
        article = Article(url)
        article.download()
        article.parse()
    except Exception as e:
        print("Error parsing article", e)
        return None

    return article.text


def get_news(country, category):
    # Make request to News API to get top headlines
    response = requests.get('https://newsapi.org/v2/top-headlines', params={
        'country': country,
        'apiKey': NEWS_API_KEY,
    })

    # Check if the response is successful (status code 200)
    if response.status_code == 200:
        data = response.json()
        articles = data['articles']
        output = ''
        for article in articles:
            output += '제목: {}\n'.format(article['title'])
            if article.get('description'):
                desc = article.get('description')
            else:
                desc = get_url_text(article['url'])
                if desc:
                    desc = summary(desc)
            
            if desc:
                output += f"요약: {desc[:300]}\n\n"
            #output += 'URL: {}\n\n'.format(article['url'])
        return output
    elif response.status_code >= 400 and response.status_code < 500:
        # If rate limit is exceeded, sleep for 1 second and try again
        print(f'Error {response.status_code}: {response.text}, retrying in 2 second...')
        time.sleep(2)
        return get_news(country, category)
    else:
        # If any other error occurs, print error message
        print(f'Error {response.status_code}: Could not retrieve {category} news for {country}.')


if __name__ == "__main__":
    # Define countries and categories
    countries = ['kr', 'us']
    categories = ["general"]
    # Get today's date as a string
    today = datetime.date.today().strftime('%Y-%m-%d')
    
    for country in countries:
        for category in categories:
            print(get_news(country, category))

