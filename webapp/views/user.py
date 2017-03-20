import datetime

from django.shortcuts import redirect, get_object_or_404
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from ..forms import UserRegistrationForm, UserEditForm, ProfileEditForm
from ..models import Profile, GuideOffer, Review
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
                print("profile error: ", profile_form.errors)
                return redirect("register_bp")
        else:
            print("user_error: ", user_form.errors)
            return redirect("register_bp")

    else:
        user_form = UserRegistrationForm()
        profile_form = ProfileEditForm()
        return flavour_render(request, 'user/register_bp.html', {'user_form': user_form, 'profile_form': profile_form})


def greeting(reauest):
    """
    NOTE: This is just for test.
    """
    return flavour_render(reauest, "user/greeting.html")


def check_email(request):
    if request.method != "POST":
        return JsonResponse({"ok": False})

    email = request.POST.get("email", None)
    user = User.objects.filter(email=email)
    if len(user) > 0:
        return JsonResponse({"ok": True, "usable": False})
    else:
        return JsonResponse({"ok": True, "usable": True})


def password_reset_complete(request):
    messages.add_message(request, messages.INFO, "reset_pw")
    return redirect("login", reset_pw="true")


@login_required
def mypage(request, page_type="account"):
    page_type_dict = {"alarm": "알림", "account": "계정 관리", "payment": "결제 내역", "review": "후기 관리",
                      "cert": "본인 인증하기", "unsub": "회원 탈퇴"}
    if page_type not in page_type_dict:
        return redirect("index")

    param_dict = {"page_type": page_type, "type_dict": page_type_dict}

    if page_type == "alarm":
        # TODO: get alarm list
        # param_dict["alarn_list"] = alarm_list
        pass
    elif page_type == "account":
        pass
    elif page_type == "payment":
        payment_list = (GuideOffer.objects.filter(request__user_id=request.user.id,
                                                  request__travel_end_at__lt=datetime.date.today())
                        .prefetch_related('request').prefetch_related('cancel').order_by('-id'))
        wait_list = []
        paid_list = []
        cancel_list = []
        for payment in payment_list:
            if payment.is_canceled:
                cancel_list.append(payment)
            elif payment.paid:
                paid_list.append(payment)
            else:
                wait_list.append(payment)
        param_dict.update(**{"wait_list": wait_list, "paid_list": paid_list, "cancel_list": cancel_list})

    elif page_type == "review":
        # TODO: model change?
        review_list = Review.objects.filter(writer=request.user).order_by('-id')
        param_dict['review_list'] = review_list
    elif page_type == "cert":
        pass
    elif page_type == 'unsub':
        pass

    return flavour_render(request, "user/mypage/"+page_type+".html", param_dict)


@login_required
def profile(request):
    return flavour_render(request, "user/profile.html")


@login_required
def edit_profile(request):
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
    return flavour_render(request, 'user/edit_profile.html', {'user_form': user_form, 'profile_form': profile_form})

