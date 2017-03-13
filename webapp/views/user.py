from django.shortcuts import redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from ..forms import UserRegistrationForm, UserEditForm, ProfileEditForm
from ..models import Profile
from bravepeach.util import flavour_render


def user_login(request):
    logout(request)
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        remember = request.POST.get('remember_me', None)
        user = authenticate(username=username, password=password)
        if user is not None and user.is_active:
            login(request, user)
            if not remember:
                request.session.set_expiry(0)
            return redirect("index")
        else:
            return flavour_render(request, "user/login.html", {"login": "fail"})
    else:
        return flavour_render(request, "user/login.html", {"login": None})


def user_logout(request):
    logout(request)
    return HttpResponseRedirect(request.GET.get('next', '/'))


def register(request):
    return flavour_render(request, 'user/register.html',)


def register_bravepeach(request):
    if request.method == "POST":
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.username = user_form.cleaned_data['email']
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            profile_instance = get_object_or_404(Profile, user_id=new_user.id)
            profile_form = ProfileEditForm(request.POST, instance=profile_instance)
            if profile_form.is_valid():
                profile_form.save()
                this_user = authenticate(username=user_form.cleaned_data['email'],
                                         password=user_form.cleaned_data["password"])
                if this_user:
                    login(request, this_user)
                    return flavour_render(request, "user/greeting.html", {"user": new_user})
                else:
                    print("no auth user")
                return redirect("register_bp")
            else:
                print(profile_form.errors)
                return redirect("register_bp")
        else:
            print(user_form.errors)
            return redirect("register_bp")

    else:
        user_form = UserRegistrationForm()
        profile_form = ProfileEditForm()
        return flavour_render(request, 'user/register_bp.html', {'user_form': user_form, 'profile_form': profile_form})


def password_reset_complete(request):
    messages.add_message(request, messages.INFO, "reset_pw")
    return redirect("login", reset_pw="true")


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
