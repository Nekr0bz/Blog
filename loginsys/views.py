from django.shortcuts import render, redirect

def login(request):
    return render(request, 'loginsys/login.html')

def logout(request):
    path = request.META['HTTP_REFERER']
    return redirect(path)

def register(request):
    return render(request, 'loginsys/register.html')

