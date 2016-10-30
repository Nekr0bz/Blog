from django.shortcuts import render, redirect

MODAL_LOGIN = 1       # модальное окно Login
MODAL_REGISTER = 2    # модальное окно Register

def login(request):
    path = request.META['HTTP_REFERER']
    ret = redirect(path)
    ret.set_cookie('MODAL', MODAL_LOGIN)
    return ret



def logout(request):
    path = request.META['HTTP_REFERER']
    return redirect(path)


def register(request):
    path = request.META['HTTP_REFERER']
    ret = redirect(path)
    ret.set_cookie('MODAL', MODAL_REGISTER)
    return ret

