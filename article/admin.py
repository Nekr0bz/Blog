# -*- coding: utf-8 -*-

from django.contrib import admin
from .models import Article, Comments


class CommentsInline (admin.TabularInline):
    """
    Интерфейс администратора позволяет редактировать
    связанные объекты на одной странице с родительским объектом.
    """
    model = Comments
    extra = 2
    readonly_fields = ['comments_likes', 'comments_dislikes']

class ArticleAdmin(admin.ModelAdmin):
    """
    Отображение модели в интерфейсе администратора
    """
    fieldsets = [
        (None,                          {'fields': ['article_user']}),
        (None,                          {'fields': ['article_title']}),
        (None,                          {'fields': ['article_text']}),
        (None,                          {'fields': ['article_datetime']}),
        ('Оценка пользователей',        {'fields': [('article_likes', 'article_dislikes')], 'classes':['collapse']})
    ]
    readonly_fields = ['article_likes', 'article_dislikes']
    inlines = [CommentsInline]

    list_display = ['__str__', 'article_datetime', 'article_likes', 'article_dislikes']
    list_filter = ['article_datetime']
    search_fields = ['article_title']
    list_per_page = 25


admin.site.register(Article, ArticleAdmin)