import datetime
from io import BytesIO
from uuid import uuid4
from urllib.request import urlopen
from hashlib import sha256

import boto3
from PIL import Image
import requests
from django.core.mail import send_mail
from django.core.files.base import ContentFile
from django.shortcuts import redirect, reverse
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from bravepeach import settings
from ..forms import UserRegistrationForm, UserEditForm, ProfileEditForm, UnsubscribeForm, UserReviewForm
from ..models import Profile, GuideOffer, UserReview, GuideReview, UserAlarm
from bravepeach.util import flavour_render, AESCipher


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
                res = requests.get(request.POST.get('profile-url'))
                filename = str(request.user.id)+"__"+datetime.datetime.now().strftime("%H_%M_%S_%f")+".jpg"
                new_profile.photo.save(filename, ContentFile(BytesIO(res.content).getvalue()))
                this_user = authenticate(username=user_form.cleaned_data['email'],
                                         password=user_form.cleaned_data["password"])
                if this_user:
                    login(request, this_user)
                    new_alarm = UserAlarm(receiver=this_user, is_new=False,
                                          contents="{} 님의 가입을 환영합니다!".format(this_user.profile.full_name),)
                    new_alarm.save()
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


def login_fb(request):
    access_token = request.POST.get('access_token')
    params = {"access_token": access_token, "format": "json",
              "fields": "id,email,first_name,last_name,gender,picture"}
    resp = requests.get('https://graph.facebook.com/me', params=params)
    print(resp.text)
    if not resp.status_code != '200':
        return JsonResponse({"ok": False, "msg": "FB Fail: {}".format(resp.status_code)})
    data = resp.json()
    uid = data['id']
    prev_profile = Profile.objects.filter(fb_id=uid).first()
    if not prev_profile:
        try:
            new_user = User(username=data['email'], first_name=data['first_name'], last_name=data['last_name'],
                            email=data['email'])
            new_user.save()
            profile = Profile(user=new_user, gender=1 if data['gender'] == 'male' else 2, fb_id=data['id'])
            if not data['picture']['data']['is_silhouette']:
                url = "https://graph.facebook.com/{}/picture?type=large".format(data['id'])
                photo = urlopen(url)
                profile.photo.save("fb_{}.jpg".format(data['id']), ContentFile(photo.read()))
            profile.save()
            new_alarm = UserAlarm(receiver=new_user, is_new=False,
                                  contents="{} 님의 가입을 환영합니다!".format(new_user.profile.full_name),)
            new_alarm.save()
            login(request, new_user)
        except Exception as e:
            msg = ""
            if e.args[0] == 1062:
                msg = "{} 는 이미 가입되어있는 메일입니다.".format(data['email'])
            return JsonResponse({"ok": False, "msg": msg})
    else:
        login(request, prev_profile.user)
    return JsonResponse({'ok': True})


def login_google(request):
    access_token = request.POST.get('access_token', "")
    params = {"key": settings.SOCIAL_AUTH_GOOGLE_API_KEY}
    headers = {'Authorization': "Bearer "+access_token, 'referer': request.get_host()}
    resp = requests.get('https://content.googleapis.com/plus/v1/people/me', params=params, headers=headers)
    if resp.status_code != 200:
        print(resp.text)
        return JsonResponse({"ok": False, "msg": resp.status_code})
    data = resp.json()
    primary_mail = None
    for email in data['emails']:
        if email['type'] == "account":
            primary_mail = email['value']
            break
    if not primary_mail:
        primary_mail = data['emails'][0]['value']
    uid = data['id']
    prev_profile = Profile.objects.filter(ggl_id=uid).first()
    if not prev_profile:
        try:
            new_user = User(username=primary_mail, email=primary_mail,
                            first_name=data['name']['givenName'], last_name=data['name']['familyName'])
            new_user.save()
        except Exception as e:
            print(e)
            msg = ""
            if e.args[0] == 1062:
                msg = "{} 는 이미 가입되어있는 메일입니다.".format(primary_mail)
            return JsonResponse({"ok": False, "msg": msg})

        profile = Profile(user=new_user, gender=1 if data['gender'] == 'male' else 2, ggl_id=data['id'])
        if data['image']['url']:
            url = data['image']['url'].split('?')[0] + '?sz=200'
            photo = urlopen(url)
            profile.photo.save('ggl_{}.jpg'.format(data['id']), ContentFile(photo.read()))
        profile.save()
        new_alarm = UserAlarm(receiver=new_user, is_new=False,
                              contents="{} 님의 가입을 환영합니다!".format(new_user.profile.full_name),)
        new_alarm.save()
        login(request, new_user)
    else:
        login(request, prev_profile.user)
    return JsonResponse({"ok": True})


def greeting(request):
    """
    NOTE: This is just for test.
    """
    return flavour_render(request, "user/greeting.html")


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
    return redirect("login")    # , reset_pw="true")


@login_required
def mypage(request, page_type="account"):
    page_type_dict = {"alarm": "알림", "account": "계정 관리", "payment": "결제 내역", "review": "후기 관리",
                      "cert": "본인 인증하기", "unsub": "회원 탈퇴", "profile": "계정 관리"}
    if page_type not in page_type_dict:
        return redirect("index")

    param_dict = {"page_type": page_type, "type_dict": page_type_dict}

    if page_type == "alarm":
        alarm_list = UserAlarm.objects.order_by("-id").all()
        param_dict["alarm_list"] = alarm_list
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
    uid = AESCipher(settings.ENCRYPT_KEY).encrypt(request.user.email)
    token = sha256(request.user.email.encode()).hexdigest()
    send_mail("Email Certification request from Bravepeach",
              """This is Email from Bravepeach to Validate Email.\n
              Please connect to following link to validate:\n
              {}://{}/cert-mail/{}_{}
              """.format(request.is_secure() and "https" or "http", request.get_host(), uid, token),
              settings.DEFAULT_FROM_EMAIL, [request.user.email]
              )
    return JsonResponse({"ok": True})


def cert_mail_check(request, uid, token):
    decrypt = AESCipher(settings.ENCRYPT_KEY).decrypt(uid)
    user = User.objects.filter(username=decrypt).first()
    print(user.profile.full_name)
    if not user:
        return JsonResponse({'ok': False, "msg": "No Such Mail"})
    if token != sha256(user.email.encode()).hexdigest():
        return JsonResponse({'ok': False, "msg": "Token Contaminated"})
    user.profile.mail_certified = True
    user.profile.save()
    return redirect(reverse('index'))


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


def upload_profile(request):
    if request.method == "POST":
        res = requests.get(request.POST.get('img'))
        img = Image.open(BytesIO(res.content))
        coord = [int(x) for x in request.POST.getlist('coord[]')]
        if request.user_agent.is_mobile:
            coord = [x*2 for x in coord]
        crop_img = img.crop(coord)
        resize_img = crop_img.resize((200, 200), Image.ANTIALIAS)
        if request.user.is_authenticated:
            byte_img = BytesIO()
            resize_img.save(byte_img, format="jpeg")
            filename = str(request.user.id)+"__"+datetime.datetime.now().strftime("%H_%M_%S_%f")+".jpg"
            request.user.profile.photo.save(filename, ContentFile(byte_img.getvalue()))
            url = "http://"+settings.AWS_S3_CUSTOM_DOMAIN+"/"+str(request.user.profile.photo)
        else:
            tmp_file = "/tmp/{}.jpg".format(uuid4())
            resize_img.save(tmp_file, format="jpeg")
            tmp_name = datetime.datetime.now().strftime("%Y_%m_%d/%H_%M_%S_%f")+".jpg"
            s3 = boto3.resource("s3", aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)
            s3.meta.client.upload_file(tmp_file, settings.AWS_STORAGE_BUCKET_NAME, 'profile/{}'.format(tmp_name))
            url = "http://" + "/".join([settings.AWS_S3_CUSTOM_DOMAIN, "profile", tmp_name])
        return JsonResponse({"ok": True, "url": url})
    return JsonResponse({"ok": False})


@login_required
def unsub_bp(request):
    if request.method != "POST":
        return redirect('mypage', page_type="unsub")

    request.user.profile.deleted_at = datetime.datetime.now()
    request.user.is_active = False
    request.user.username += '__'
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
