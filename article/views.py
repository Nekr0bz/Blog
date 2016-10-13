from django.shortcuts import render

from .models import Article, Comments

def index(request):
    context = {'articles': Article.objects.order_by('-article_datetime')}
    return render(request, 'article/index.html', context)