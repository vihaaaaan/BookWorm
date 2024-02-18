from datetime import datetime

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template import Template
import re
from bs4 import BeautifulSoup
import requests

from TeacherWorm.models.articles import Article
from datetime import datetime

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template import Template
import re
from bs4 import BeautifulSoup
import requests
from TeacherWorm.models.articles import Article

import openai
from openai import OpenAI

import os

OPENAI_API_KEY = "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"
#openai.api_key = OPENAI_API_KEY
client = openai.OpenAI(api_key = OPENAI_API_KEY)

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
        original_text=article['description'].replace('\n', '\n\n'),
        # Assuming these fields are not provided in the dictionary and will be populated laters
    )

    # Save the instance to the database
    article_instance.save()


def add_article(request):
    context = {}
    if request.method == 'POST':
        article_url = request.POST.get('article_url', None)
        if article_url:
            print("Successfully posted:", article_url)
            dict = get_the_news(article_url)
            load_to_models(dict)
            #Call a function to get scraped data from URL
            #Call another function to load scraped data into database model
            newText = remake(dict[0], 3)
            questMCQ = []
            questMCQ = questionM(newText,5)
            questFRQ = questionF(newText,2)
            questTF = questionTF(newText,5)
            print(questMCQ)
            print(questFRQ)
            print(questTF)
            #print(quest)
            #print(newText)

    return render(request, 'TeacherWorm/teacher_view.html', context)


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


def questionM(prompt, numQ):
    print("handling regular")

    directions = f"Create a list with {numQ} dictionaries in it like [(),(),(),(),()] to hold multiple questions for the following prompt {prompt}. Each dictionary will have five strings. The first string in each dictionary will be the multiple choice question. The second dictionary will the correct answer to the multiple choice question. The next three strings will be the remaining wrong answers to the multiple choice question. "
    print(directions)
    messages = [{"role": "system", "content": "You are to making multiple choice test questions based on an article."}]
    messages.append({"role": "user",
                     "content": directions})

    answers = client.chat.completions.create(model="gpt-3.5-turbo",
                                             messages=messages, )
    print("recieved from gpt")

    output = answers.choices[0].message.content

    return output



def questionF(prompt, numQ):
    print("handling regular")

    directions = f"Create a list with {numQ} frq’s based on the following text: {prompt}"
    print(directions)
    messages = [{"role": "system", "content": "You are to frq test questions based on an article."}]
    messages.append({"role": "user",
                     "content": directions})

    answers = client.chat.completions.create(model="gpt-3.5-turbo",
                                             messages=messages, )
    print("recieved from gpt")

    output = answers.choices[0].message.content

    return output

def questionTF(prompt, numQ):
    print("handling regular")
    print(prompt)
    directions = f"Create a list with {numQ} dictionaries in it like [(),(),(),(),()] to hold multiple true or false questions for the following prompt {prompt}. Each dictionary will have three strings. The first string in each dictionary will be the true or false question. The second dictionary will the correct answer. The thrid string will be the wrong answer."
    print(directions)
    messages = [{"role": "system", "content": "You are to true or false test questions based on an article."}]
    messages.append({"role": "user",
                     "content": directions})

    answers = client.chat.completions.create(model="gpt-3.5-turbo",
                                             messages=messages, )
    print("recieved from gpt")

    output = answers.choices[0].message.content

    return output


def remake(orgArticle, difficulty):
    print("handling regular")
    mid = orgArticle["description"]
    # print(type(mid))
    
    if (difficulty == 1):
        messages = [{"role": "system", "content": "You are to rewrite an article to adjust the reading level."}]
        messages.append({"role": "user",
                         "content": f"Rewrite the following article for a reading level between kindergarten and 4th grade.: {mid}"})
        answers = client.chat.completions.create(model="gpt-3.5-turbo",
                                                 messages=messages, )
    elif (difficulty == 2):
        messages = [{"role": "system", "content": "You are to rewrite an article to adjust the reading level."}]
        messages.append({"role": "user",
                         "content": f"Rewrite the following article for a reading level between 5th grade and 7th grade.: {mid}"})
        answers = client.chat.completions.create(model="gpt-3.5-turbo",
                                                 messages=messages, )
    else:
        messages = [{"role": "system", "content": "You are to rewrite an article to adjust the reading level."}]
        messages.append({"role": "user",
                         "content": f"Rewrite the following article for a reading level between 8th grade and 12th grade.: {mid}"})
        answers = client.chat.completions.create(model="gpt-3.5-turbo",
                                                 messages=messages, )

        answers = client.chat.completions.create(model="gpt-3.5-turbo",
                                                 messages=messages, )
    print("recieved from gpt")

    output = answers.choices[0].message.content

    return output