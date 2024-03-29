from django.shortcuts import render, get_object_or_404
from TeacherWorm.models.articles import Article  # Ensure this is the correct import path for your Article model
from TeacherWorm.models.questions import Question


def read_article(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    questions = Question.objects.filter(article_id=article)
    print(article.original_text)

    context = {
        'article': article,
        'questions': questions,

    }
    return render(request, 'StudentWorm/article_view.html', context)
