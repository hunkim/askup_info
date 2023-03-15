import requests
import datetime
import os
import time
from newspaper import Article
import sys

from chatgpt import summary

NEWS_API_KEY = os.environ["NEWS_API_KEY"]


def get_url_text(url):
    try:
        article = Article(url)
        article.download()
        article.parse()
    except Exception as e:
        sys.stderr.write(f'Error parsing article {e}')
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
            output += 'URL: {}\n\n'.format(article['url'])
            sys.stderr.write(f'Output: {output}')
        return output
    else:
        sys.stderr.write(f'Error {response.status_code}: {response.text}')


if __name__ == "__main__":
    # Define countries and categories
    countries = ['kr']
    categories = ["general"]
    # Get today's date as a string
    today = datetime.date.today().strftime('%Y-%m-%d')

    for country in countries:
        for category in categories:
            print(get_news(country, category))
