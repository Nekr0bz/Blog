from django.shortcuts import render, get_object_or_404
from django.utils import timezone

from .models import Article

def index(request):
    list_article = Article.objects.filter(article_datetime__lte=timezone.now()).order_by('-article_datetime')
    context = {'articles': list_article}
    return render(request, 'article/index.html', context)

def detail(request, article_id):
    context = {
        'article': get_object_or_404(Article, id=article_id)
    }
    return render(request, 'article/detail.html', context)