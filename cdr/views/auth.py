from django.shortcuts import render
from django.contrib.auth import logout

def auth_login(request):
    return render(request, 'auth/login.html', {})

def auth_logout(request):
    logout(request)
    return render(request, 'auth/logout.html', {})
