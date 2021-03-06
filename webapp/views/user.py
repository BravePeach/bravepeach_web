import datetime
from io import BytesIO
from uuid import uuid4

import boto3
from PIL import Image
import requests
from django.core.files.base import ContentFile
from django.shortcuts import redirect, get_object_or_404
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from bravepeach import settings
from ..forms import UserRegistrationForm, UserEditForm, ProfileEditForm, UnsubscribeForm, UserReviewForm
from ..models import Profile, GuideOffer, UserReview, GuideReview
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
            return HttpResponseRedirect(request.GET.get('next', '/'))
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
            # profile_instance = get_object_or_404(Profile, user_id=new_user.id)
            # profile_form = ProfileEditForm(request.POST, instance=profile_instance)
            profile_form = ProfileEditForm(request.POST)
            if profile_form.is_valid():
                new_profile = profile_form.save(commit=False)
                new_profile.user = new_user
                new_profile.save()
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
                      "cert": "본인 인증하기", "unsub": "회원 탈퇴", "profile": "계정 관리"}
    if page_type not in page_type_dict:
        return redirect("index")

    param_dict = {"page_type": page_type, "type_dict": page_type_dict}

    if page_type == "alarm":
        # TODO: get alarm list
        # param_dict["alarn_list"] = alarm_list
        pass
    elif page_type == "account":
        pass
    elif page_type == "profile":
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
        param_dict["user_form"] = user_form
        param_dict["profile_form"] = profile_form
    elif page_type == "payment":
        payment_list = (GuideOffer.objects.filter(request__user_id=request.user.id,
                                                  request__travel_begin_at__gte=datetime.date.today())
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
        my_review_list = UserReview.objects.filter(writer=request.user).order_by('-id')
        param_dict['my_reviews'] = my_review_list
        guide_review_list = GuideReview.objects.filter(receiver=request.user).order_by('-id')
        param_dict['guide_reviews'] = guide_review_list
    elif page_type == "cert":
        pass
    elif page_type == 'unsub':
        unsub_form = UnsubscribeForm()
        param_dict["unsub_form"] = unsub_form

    return flavour_render(request, "user/mypage/"+page_type+".html", param_dict)


@login_required
def cert_mail(request):
    # TODO: send mail
    print(request.POST)
    return JsonResponse({"ok": True})


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
            pass
    return redirect("mypage", page_type="profile")


def upload_original(request):
    if request.method == "POST":
        files = request.FILES
        s3 = boto3.resource("s3", aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)
        file_ext = files['original'].name.split(".")[-1]
        tmp_name = datetime.datetime.now().strftime("%Y_%m_%d/%H_%M_%S_%f")+"."+file_ext
        img = Image.open(files['original'])
        img.thumbnail((600, 600), Image.ANTIALIAS)
        tmp_file = "/tmp/{}.jpg".format(uuid4())
        img.save(tmp_file, format="jpeg")
        s3.meta.client.upload_file(tmp_file, settings.AWS_STORAGE_BUCKET_NAME,
                                      "original/{}".format(tmp_name))
        url = "http://" + "/".join([settings.AWS_S3_CUSTOM_DOMAIN, "original", tmp_name])
        return JsonResponse({"ok": True, "url": url})
    return JsonResponse({"ok": False})


@login_required
def upload_profile(request):
    if request.method == "POST":
        res = requests.get(request.POST.get('img'))
        img = Image.open(BytesIO(res.content))
        crop_img = img.crop([int(x) for x in request.POST.getlist('coord[]')])
        resize_img = crop_img.resize((200, 200), Image.ANTIALIAS)
        byte_img = BytesIO()
        resize_img.save(byte_img, format="jpeg")
        filename = str(request.user.id)+"__"+datetime.datetime.now().strftime("%H_%M_%S_%f")+".jpg"
        request.user.profile.photo.save(filename, ContentFile(byte_img.getvalue()))
        url = "http://"+settings.AWS_S3_CUSTOM_DOMAIN+"/"+str(request.user.profile.photo)
        return JsonResponse({"ok": True, "url": url})
    return JsonResponse({"ok": False})


@login_required
def unsub_bp(request):
    if request.method != "POST":
        return redirect('mypage', page_type="unsub")

    request.user.profile.deleted_at = datetime.datetime.now()
    request.user.is_active = False
    unsub_form = UnsubscribeForm(request.POST, instance=request.user.profile)

    if unsub_form.is_valid():
        unsub_form.save()
        request.user.save()
        return redirect('logout')
    else:
        return redirect('mypage', page_type="unsub")


@login_required
def write_review(request, offer_id):
    prev_review = UserReview.objects.filter(offer_id=offer_id)
    offer = GuideOffer.objects.get(id=offer_id)

    if request.method == "GET":
        if prev_review:
            form = UserReviewForm(instance=prev_review)
        else:
            form = UserReviewForm()
        return flavour_render(request, "user/write_review.html", {"offer": offer, "review_form": form})
    else:
        if prev_review:
            form = UserReviewForm(request.POST, instance=prev_review)
        else:
            form = UserReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.offer_id = offer_id
            review.writer = request.user
            review.receiver = offer.guide
            review.save()
        return redirect('my_trip')
