from urllib.parse import urlparse

from django.conf import settings

from bs4 import BeautifulSoup
import openai
from openai import OpenAI
import requests

headers = {
    'accept': '*/*',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en-US,en;q=0.9',
    'referer': settings.REFERER,
    'user-agent': settings.USER_AGENT,
}


# Webscraping functions


def get_article_data(url):
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return True
      # soup = BeautifulSoup(response.text, 'html.parser')
      # article_data = parse_article_html(soup, url)
    else:
        return False
        # Need to implement something here that goes to the front end and posts a message saying that the url is invalid

def parse_article_html(card,url):
    """Extract article information from the raw html"""

    # Get domain name from url
    parsed_url = urlparse(url)
    domain_name = parsed_url.netloc

    # Check if domain name is valid
    match domain_name:
      case 'news.yahoo.com':
        source = "Yahoo News"
      case 'cnn.com':
        source = "CNN"
      case 'bbc.com':
        source = "BBC"
      case 'nbcnews.com':
        source = "NBC News"
      case 'cbsnews.com':
        source = "CBS News"
      case 'apnews.com':
        source = "Associated Press"
      case _:
        source = ""

    # Capture title
    try:
        headline = card.find('h1').text.strip()
    except AttributeError:
        headline = ""

    # Capture date
    try:
        posted = card.find('time').text.replace('·', '').strip()
    except AttributeError:
        posted = ""
    description = ""

    # Capture text
    p_tags = card.find_all('p')
    for p_tag in p_tags:
        description += p_tag.text.strip() + '\n'


    try:
        author = card.find('span', 'caas-author-byline-collapse').text

    except AttributeError:
        author = ""

    article = {
        'headline': headline,
        'author' : author,
        'posted': posted,
        'source': source,
        'description': description.strip(),
        'link':url
    }
    return article
