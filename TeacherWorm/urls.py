# from django.conf.urls import url
from django.urls import path

app_name = "teacher-worm"

urlpatterns = [
    path("", add_article, name="add_article"),
]
