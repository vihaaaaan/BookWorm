from django.db import models
from articles import Article


class Article(models.Model):
    created_on = models.DateField(auto_now_add=True)
    question = models.TextField()
    QUESTION_TYPE_CHOICES = [
        ("MCQ", "Multiple Choice"),
        ("TF", "True or False"),
        ("FRQ", "Free Response"),
    ]
    question_type = models.CharField(max_length=50, choices=QUESTION_TYPE_CHOICES)
    mcq_incorrect_choice_1 = models.TextField(null=True)
    mcq_incorrect_choice_2 = models.TextField(null=True)
    mcq_incorrect_choice_3 = models.TextField(null=True)
    mcq_correct_choice = models.TextField(null=True)
    article_id = models.ForeignKey(Article, on_delete=models.CASCADE)
    DIFFICULTLY_CHOICES = [
        ("EASY", "Easy"),
        ("MEDIUM", "Medium"),
        ("HARD", "Hard"),
        ("ORIGINAL", "Original"),
    ]
    difficulty_level = models.CharField(max_length=50, choices=DIFFICULTLY_CHOICES)

