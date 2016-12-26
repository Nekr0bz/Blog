# -*- coding: utf-8 -*-

import ast

from django.shortcuts import redirect
from django.contrib import auth
from django.contrib.auth.models import User
from django.db.utils import IntegrityError
from django.http import HttpResponse, Http404


def login(request):
    """
    Авторизация пользователя

    :param request: запрос
    :type request: django.http.HttpRequest
    :return: если авторизация не произошла, возвращает сообщение об ошибке, иначе-'OK'
    :rtype: django.http.HttpResponse
    """
    if request.POST:
        authPOST = ast.literal_eval(request.POST['dataAuth'])

        if not validator(authPOST):
            return HttpResponse('error_valid')

        username = authPOST['username']
        password = authPOST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                auth.login(request, user)
                return HttpResponse('OK')
        else:
            return HttpResponse('error_login')

    else:
        raise Http404()


# TODO: КАРТИНАКУ В СТАТЬЮ
# TODO: ссs, js в одну строку
# TODO: ПЕРЕНОС СТРОК В СТАТЬЕ
# TODO: ТАЙМ ОУТ НА РЕГИСТРАЦИЮ И Т.Д.
def logout(request):
    """
    Пользователь вышел

    :param request: запрос
    :type request: django.http.HttpRequest
    :return: перенаправляет на ссылающую страницу
    :rtype: django.http.HttpResponseRedirect
    """
    auth.logout(request)
    return redirect("/")


def register(request):
    """
    Регистрация пользователя

    :param request: запрос
    :type request: django.http.HttpRequest
    :return: если регистрация не произошла, возвращает сообщение об ошибке, иначе-'OK'
    :rtype: django.http.HttpResponse
    :raise: django.db.utils.IntegrityError
    """
    if request.POST:
        authPOST = ast.literal_eval(request.POST['dataAuth'])

        if not validator(authPOST):
            return HttpResponse('error_valid')

        username = authPOST['username']
        mail = authPOST['mail']
        password1 = authPOST['password1']

        try:
            User.objects.create_user(username, mail, password1)
            user = auth.authenticate(username=username, password=password1)
            auth.login(request, user)
            ret_msg = 'OK'
        except IntegrityError:
            ret_msg = 'error_name'

        return HttpResponse(ret_msg)

    else:
        raise Http404()


def validator(authPOST):
    """
    Валидация формы для аутентификации

    :param authPOST: словарь POST данных
    :return: True или False взависимости валидны данные или нет
    """
    keysPOST = authPOST.keys()

    for key in keysPOST:
        if key != 'mail' and (not authPOST[key].isalnum() or len(authPOST[key]) < 4):
            return False

    if 'mail' in keysPOST:
        import re

        mail = authPOST['mail']
        p1 = authPOST['password1']
        p2 = authPOST['password2']
        reg = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"

        if not re.match(reg, mail) or p1 != p2:
            return False

    return True
