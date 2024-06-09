from django.contrib import admin
from .models.articles import Article
from .models.questions import Question

# Register your models here.
admin.site.register(Article)
admin.site.register(Question)