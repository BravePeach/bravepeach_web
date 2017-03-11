from dateutil import parser

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from ..forms import UserRegistrationForm, UserEditForm, ProfileEditForm
from bravepeach.util import flavour_render


def user_logout(request):
    logout(request)
    return HttpResponseRedirect(request.GET.get('next', '/'))


def register_user(request):
    user_form = UserRegistrationForm(request.POST)
    profile_form = ProfileEditForm(request.POST)
    if user_form.is_valid() and profile_form.is_valid():
        profile_form.save()
        new_user = user_form.save(commit=False)
        new_user.set_password(user_form.cleaned_data['password'])
        new_user.save()
        this_user = authenticate(username=user_form.cleaned_data['username'],
                                 password=user_form.cleaned_data['password'],)
        login(request, this_user)
        return request, this_user


def register(request):
    return flavour_render(request, 'user/register.html',
                          {"register_type": [('Facebook으로 가입하기', '#4990e2'), ("Naver로 가입하기", "#6ac601"),
                                             ("Google로 가입하기", '#ff9600'), ("Bravepeach로 가입하기", "#e64c47")]})


def register_bravepeach(request):
    if request.method == "POST":
        request, user = register_user(request)
        return flavour_render(request, "user/greeting.html", {"user": user})
    else:
        user_form = UserRegistrationForm()
        profile_form = ProfileEditForm()
        return flavour_render(request, 'user/register_bravepeach.html',
                              {'user_form': user_form, 'profile_form': profile_form})


@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user,
                                 data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile,
                                       data=request.POST,
                                       files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            request.user.profile.birthday = profile_form.cleaned_data['birthday']
            user_form.save()
            profile_form.save()
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return flavour_render(request, 'views/edit_profile.html', {'user_form': user_form, 'profile_form': profile_form})
