from datetime import datetime

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template import Template
import re
from bs4 import BeautifulSoup
import requests

from TeacherWorm.models.articles import Article

headers = {
    'accept': '*/*',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en-US,en;q=0.9',
    'referer': 'https://www.google.com',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36 Edg/85.0.564.44'
}


def load_to_models(article):
    article = article[0]
    # Create the Article instance
    article_instance = Article(
        title=article['headline'],
        author=article['author'],
        date_published=article['posted'],
        source=article['source'],
        original_text=article['description'].replace('\n', '</p><br></br><p>'),
        # Assuming these fields are not provided in the dictionary and will be populated later
        difficulty_level_easy_text='',
        difficulty_level_medium_text='',
        difficulty_level_hard_text='',
    )

    # Save the instance to the database
    article_instance.save()


def add_article(request):
    context = {}
    if request.method == 'POST':
        article_url = request.POST.get('content', None)
        if article_url:
            print("Successfully posted:", article_url)
            dict = get_the_news(article_url)
            load_to_models(dict)
            #Call a function to get scraped data from URL
            #Call another function to load scraped data into database model

    return render(request, 'TeacherWorm/article _link_page.html', context)


def get_article(card,url):
    """Extract article information from the raw html"""
    try:
        headline = card.find('h1').text
    except AttributeError:
        headline = ""
    try:
        #source = card.find("span class = \"caas-author").text
        source = "Yahoo"
    except AttributeError:
        source = ""
    try:
        posted = card.find('time').text.replace('·', '').strip()
    except AttributeError:
        posted = ""
    description = ""
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

def get_the_news(url):
    """Scrape a specific article from the provided URL"""
    articles = []
    '''


    i = 1
    while i < 2:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            cards = soup.find_all('div', 'NewsArticle')
            i += 1
            # extract articles from page
            for card in cards:
                article = get_article(card)
                link = article['link']
                if not link in links:
                    links.add(link)
                    articles.append(article)
        else:
            print(f"Error: Unable to fetch the URL. Status Code: {response.status_code}")
            break
    '''
    response = requests.get(url, headers=headers)
    if(response.status_code == 200):
      #print(response.text)
      soup = BeautifulSoup(response.text, 'html.parser')
      #cards = soup.find_all('div')
      #print(cards)
      article = get_article(soup,url)
      articles.append(article)

      #for card in cards:
      #      article = get_article(card)
      #      articles.append(article)

    else:
      print(f"Error: Unable to fetch the URL. Status Code: {response.status_code}")

    return articles
