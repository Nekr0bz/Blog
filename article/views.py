from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.utils import timezone

from .models import Article, Comments

def index(request):
    list_article = Article.objects.filter(article_datetime__lte=timezone.now()).order_by('-article_datetime')
    context = {'articles': list_article}
    return render(request, 'article/index.html', context)

def detail(request, article_id):
    context = {
        'article': get_object_or_404(Article, id=article_id)
    }
    return render(request, 'article/detail.html', context)

#TODO: сделать так тчобы страница не прокручивалась вверх
#TODO: убирать лайк/дизлайк при повторном нажатии
def article_add_like(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    article.article_likes +=1
    article.save()
    path = request.META['HTTP_REFERER']
    return redirect(path)

def article_add_dislike(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    article.article_dislikes +=1
    article.save()
    path = request.META['HTTP_REFERER']
    return redirect(path)

def comment_add_like(request, comment_id):
    comment = get_object_or_404(Comments, id=comment_id)
    comment.comments_likes +=1
    comment.save()
    path = request.META['HTTP_REFERER']
    return redirect(path)

def comment_add_dislike(request, comment_id):
    comment = get_object_or_404(Comments, id=comment_id)
    comment.comments_dislikes +=1
    comment.save()
    path = request.META['HTTP_REFERER']
    return redirect(path)