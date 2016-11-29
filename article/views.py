from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist


from .models import Article, Comments, Rate

#TODO: придумать что выводить когда ничего не найдено
def index(request):
    list_article = Article.objects.filter(article_datetime__lte=timezone.now()).order_by('-article_datetime')
    if request.GET:
        find = list_article.filter(article_title__icontains=request.GET['find'])
        if (find):
            list_article = find
    context = {
        'articles': list_article
    }

    return render(request, 'article/index.html', context)

def detail(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    comments = article.comments_set.all().\
        filter(comments_datetime__lte=timezone.now()).order_by('-comments_datetime')

    user_comments = user_articles = []
    if request.user.is_authenticated():
        user_comments = [i.id for i in request.user.comments_set.all()]
        user_articles = [i.id for i in request.user.article_set.all()]

    context = {
        'article': article,
        'comments': comments,
        'user_comments': user_comments,
        'user_articles': user_articles
    }
    return render(request, 'article/detail.html', context)

def rate_control(request):
    if request.GET:
        table_type = request.GET['table_type']
        table_id = request.GET['table_id']
        vote = request.GET['vote']
        num_vote = 1 if vote == 'like' else -1
        Obj = (Article if (table_type == 'article') else Comments).objects.get(id=table_id)
        other = 'like' if vote == 'dislike' else 'dislike'

        for k in Obj.__dict__.keys():
            if ('_'+vote in k):
                active_rate = k
            if ('_'+ other in k):
                other_rate = k

        try:
            rate_obj = request.user.rate_set.get(
                rate_table_type=table_type,
                rate_table_id=table_id
            )
            if (rate_obj.rate_vote == 0):
                # поставили оценку заного
                rate_obj.rate_vote = num_vote
                Obj.__dict__[active_rate] += 1
            elif (rate_obj.rate_vote == num_vote):
                # убрали оценку
                rate_obj.rate_vote = 0
                Obj.__dict__[active_rate] -= 1
            else:
                # поменяли оценку
                rate_obj.rate_vote = num_vote
                Obj.__dict__[active_rate] += 1
                Obj.__dict__[other_rate] -= 1

        except ObjectDoesNotExist:
            # ещё не оценивал
            rate_obj = request.user.rate_set.create(
                rate_table_type=table_type,
                rate_table_id=table_id,
                rate_vote=num_vote
            )
            Obj.__dict__[active_rate] += 1

        rate_obj.save()
        Obj.save()
        msg = str(Obj.__dict__[active_rate])+'/'+str(Obj.__dict__[other_rate])
        return HttpResponse(msg)
    else:
        raise Http404()

#TODO: валидация текста!
def add_article(request):
    if request.user.is_authenticated() == False:
        raise Http404()

    if request.POST:
        article_title = request.POST['article_title']
        article_text = request.POST['article_text']
        request.user.article_set.create(
            article_title=article_title,
            article_text=article_text,
            article_datetime=timezone.now()
        )
        return redirect('/')
    else:
        return render(request, 'article/addarticle.html')

def del_article(request, article_id):
    if request.user.is_authenticated():
        try:
            article = request.user.article_set.get(id=article_id)

            for rate_obj in Rate.objects.filter(
                    rate_table_type='article',
                    rate_table_id=article_id,
            ):
                rate_obj.delete()

            article.delete()
            return redirect('/')
        except ObjectDoesNotExist:
            raise Http404
    else:
        raise Http404

def upd_article(request, article_id):
    if request.user.is_authenticated():
        try:
            article = request.user.article_set.get(id=article_id)
            if request.POST:
                article.article_title = request.POST['article_title']
                article.article_text = request.POST['article_text']
                article.save()
                return redirect('/'+article_id+'/')
            else:
                context = {
                    'article': article
                }
                return render(request, 'article/updarticle.html', context)

        except ObjectDoesNotExist:
            raise Http404
    else:
        raise Http404

def add_comment(request, article_id):
    if request.POST and request.user.is_authenticated():
        comment_text = request.POST['comment_text']
        article = get_object_or_404(Article, id=article_id)
        article.comments_set.create(
            comments_user_id=request.user.id,
            comments_text=comment_text,
            comments_datetime=timezone.now()
        )
        path = request.META['HTTP_REFERER']
        return redirect(path)
    else:
        raise Http404()

def del_comment(request, comment_id):
    if request.user.is_authenticated():
        try:
            comment = request.user.comments_set.get(id=comment_id)

            for rate_obj in Rate.objects.filter(
                    rate_table_type='comment',
                    rate_table_id=comment_id,
            ):
                rate_obj.delete()

            comment.delete()
            path = request.META['HTTP_REFERER']
            return redirect(path)
        except ObjectDoesNotExist:
            raise Http404
    else:
        raise Http404

def upd_comment(request, comment_id):
    user = request.user
    if request.POST and user.is_authenticated():
        try:
            comment = user.comments_set.get(id=comment_id)
            article_id = comment.comments_article

            for rate_obj in Rate.objects.filter(
                rate_table_type='comment',
                rate_table_id=comment_id,
            ):
                rate_obj.delete()

            comment.delete()
            new_text = request.POST['comment_text']
            user.comments_set.create(
                comments_article=article_id,
                comments_text=new_text,
                comments_datetime=timezone.now()
            )
            path = request.META['HTTP_REFERER']
            return redirect(path)
        except ObjectDoesNotExist:
            raise Http404
    else:
        raise Http404

