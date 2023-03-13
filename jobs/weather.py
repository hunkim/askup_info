import requests
from bs4 import BeautifulSoup

def get_clean_text_from_url(url):
    # Make a request to the URL
    response = requests.get(url)

    # Parse the HTML using BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Extract the text from the HTML
    text = soup.get_text()

    # Remove extra characters from the text
    text = text.strip()

    # Replace multiple whitespace characters with a single space
    text = ' '.join(text.split())

    # Return the cleaned text
    return text

if __name__ == "__main__":
    # Get the text from the URL
    text = get_clean_text_from_url('https://weather.naver.com/')

    # Print the text
    print(text)