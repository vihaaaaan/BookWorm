from django.db import models


class Article(models.Model):
    created_on = models.DateField(auto_now_add=True)
    title = models.CharField(max_length=500)
    author = models.CharField(max_length=500)
    date_published = models.DateField()
    source = models.CharField(max_length=500)
    original_text_id = models.CharField(max_length=50, unique=True, blank=True, null=True)
    original_text = models.TextField()
    difficulty_level_easy_text = models.TextField()
    difficulty_level_medium_text = models.TextField()
    difficulty_level_hard_text = models.TextField()

