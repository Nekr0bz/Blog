from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist

from .models import Article, Comments

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
    context = {
        'article': get_object_or_404(Article, id=article_id)
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



