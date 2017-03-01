from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm, UserRegistrationForm

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


def user_logout(request):
    logout(request)
    return HttpResponseRedirect(request.GET.get('next', '/'))


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(
                user_form.cleaned_data['password']
            )
            new_user.save()
            this_user = authenticate(username=user_form.cleaned_data['username'],
                                    password=user_form.cleaned_data['password'],
                                    )
            login(request, this_user)
            return render(request, 'views/register_done.html',{'new_user' : new_user})
    else :
        user_form = UserRegistrationForm()
    return render(request, 'views/register.html',{'user_form':user_form})
