# from django.conf.urls import url
from django.urls import path
from .views import add_article

urlpatterns = [
    path('add_article/', add_article, name='add_article'),
]
