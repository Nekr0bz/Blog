import ast

from django.shortcuts import redirect
from django.contrib import auth
from django.contrib.auth.models import User
from django.db.utils import IntegrityError
from django.http import HttpResponse, Http404


def login(request):
    if request.POST:
        authPOST = ast.literal_eval(request.POST['dataAuth'])

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


def logout(request):
    path = request.META['HTTP_REFERER']
    auth.logout(request)
    return redirect(path)


def register(request):
    if request.POST:
        authPOST = ast.literal_eval(request.POST['dataAuth'])

        username = authPOST['username']
        mail = authPOST['mail']
        password1 = authPOST['password1']
        ret_msg = ''

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

