from django.shortcuts import render, get_object_or_404
from TeacherWorm.models.articles import Article  # Ensure this is the correct import path for your Article model
from TeacherWorm.models.questions import Question
from TeacherWorm.models.choices import Choice


def read_article(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    questions = Question.objects.filter(article_id=article)
    choices = Choice.objects.filter(question_id__in=questions.values_list('id', flat=True))
    print(article.original_text)

    context = {
        'article': article,
        'questions': questions,
        'choices': choices,
    }
    return render(request, 'StudentWorm/article_view.html', context)
