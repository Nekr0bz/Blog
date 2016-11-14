from django.db import models
from django.contrib.auth.models import User

display_text = lambda text, l: text if len(text) <= l else text[:l]+'...'

class Article (models.Model):
    class Meta:
        db_table = 'article'

    article_user = models.ForeignKey(User)
    article_title = models.CharField('Заголовок', max_length=200)
    article_text = models.TextField('Текст')
    article_datetime = models.DateTimeField('Дата и время')
    article_likes = models.IntegerField('Количество лайков', default=0)
    article_dislikes = models.IntegerField('Количество дизлайков', default=0)

    def __str__(self):
        return display_text(self.article_title, 50)

    def view_article_text(self):
        return display_text(self.article_text, 300)

    #TODO: article_text не меньше 350 символов!


class Comments (models.Model):
    class Meta:
        db_table = 'comments'

    comments_article = models.ForeignKey(Article)
    comments_user = models.ForeignKey(User)
    comments_text = models.CharField('Текст', max_length=200)
    comments_likes = models.IntegerField('Количество лайков', default=0)
    comments_dislikes = models.IntegerField('Количество дизлайков', default=0)
    comments_datetime = models.DateTimeField('Дата и время')

    def __str__(self):
        text = self.comments_text
        return text if len(text) <= 50 else text[:50]+'...'

class Rate (models.Model):
    rate_user = models.ForeignKey(User)
    rate_vote = models.IntegerField(default=0)
    rate_table_id = models.IntegerField()
    rate_table_type = models.CharField(max_length=50)
