from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from .forms import LoginForm

def index(request):
    return render(request, "views/index.html", {})


# def user_login(request):
#     if request.method =="POST":
#         form = LoginForm(request.POST)
#         if form.is_valid():
#             cd = form.cleaned_data
#             user = authenticate(email = cd['email'],
#                                 password = cd['password'])
#             if user is not None:
#                 if user.is_active:
#                     login(request, user)
#                     return HttpResponse('Authenticated successfully')
#                 else:
#                     return HttpResponse('Disabled account')
#         else:
#             return HttpResponse('invalid login')
#     else:
#         form = LoginForm()
#     return render(request, 'views/login.html',{'form':form})
