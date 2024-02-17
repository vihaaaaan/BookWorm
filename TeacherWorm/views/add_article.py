from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template import loader


def add_article(request):
    context = {}
    if request.method == 'POST':
        article_url = request.POST.get('content', None)
        if article_url:
            print("Successfully posted:", article_url)
            #Call a function to get scraped data from URL
            #Call another function to load scraped data into database model

    return render(request, 'TeacherWorm/article _link_page.html', context)
