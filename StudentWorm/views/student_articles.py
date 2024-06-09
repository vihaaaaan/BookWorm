from django.shortcuts import render
from TeacherWorm.models.articles import Article

def student_articles(request):
    articles = Article.objects.all()
    context = {'articles': articles}
    return render(request, 'StudentWorm/student_view.html', context)