# -*- coding: utf-8 -*-

from django import template
from django.core.exceptions import ObjectDoesNotExist

register = template.Library()

@register.simple_tag
def rate_active(user, table_type, table_id, vote):
    """
    Тег для определия оцениал пользователь
    данную статью или комментарий

    :param user: Объект user
    :type user: django.contrib.auth.models.User
    :param table_type: тип оцениваемого объекта:
    комментарий или статья

    :param table_id: ID оцениваемого объекта
    :param vote: оценка
    :return: строка 'active' если пользователь
    оценивал данный объект

    :raise: django.core.exceptions.ObjectDoesNotExist
    """
    if (user.is_authenticated()):
        try:
            user.rate_set.get(
                rate_table_type=table_type,
                rate_table_id=table_id,
                rate_vote=int(vote)
            )
            return 'active'
        except ObjectDoesNotExist:
            return None