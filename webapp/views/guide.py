import datetime
import json
from uuid import uuid4

import boto3
from PIL import Image
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404

from django.views.generic import View
from django.utils.dateparse import parse_date
from django.http import JsonResponse, HttpResponse
from django.utils import formats
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import user_passes_test
from bravepeach import settings

from bravepeach.util import flavour_render
from ..models import (Guide, GuideOffer, UserReview, UserRequest, GuideLike, AccomTemplate, GuideTemplate,
                       Notice)
from ..forms import WriteOfferForm, VolunteerForm
from bravepeach.const import GUIDE_TYPE, GUIDE_THEME


def guide_required(user):
    return user.profile.is_guide


def profile(request, gid):
    guide = get_object_or_404(Guide.objects.select_related('user'), id=gid)
    recent_trip = (GuideOffer.objects.filter(paid=True, is_canceled=False, guide=guide,
                                             request__travel_end_at__lt=datetime.date.today())
                   .select_related('request').order_by('-request__travel_end_at')).all()[:5]
    review_list = UserReview.objects.filter(receiver=guide).order_by('-id')
    return flavour_render(request, "guide/profile.html", {"guide": guide, "recent_trip": recent_trip,
                                                          "reviews": review_list,
                                                          "review_ids": [x.offer_id for x in review_list]})


def index(request):
    if request.user.is_authenticated:
        if request.user.profile.is_guide:
            return redirect(find)
        else:
            return redirect(dashboard)
    else:
        return flavour_render(request, "guide/index_not_login.html", {})


@login_required
def volunteer(request):
    prev_vol = Guide.objects.filter(user=request.user).all()

    if request.method == "POST":
        cert_link_list = []
        exp_link_list = []
        s3 = boto3.resource("s3", aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)
        for f in request.FILES.getlist('certificate'):
            ext = f.name.split('.')[-1]
            key = "volunteer/{}/cert/{}.{}".format(request.user.id,
                                                   datetime.datetime.now().strftime("%Y_%m_%d/%H_%M_%S_%f"), ext)
            s3.meta.client.upload_fileobj(f, settings.AWS_STORAGE_BUCKET_NAME, key)
            cert_link_list.append("http://"+settings.AWS_S3_CUSTOM_DOMAIN+'/'+key)

        for f in request.FILES.getlist('experience'):
            ext = f.name.split('.')[-1]
            key = "volunteer/{}/exp/{}.{}".format(request.user.id,
                                                  datetime.datetime.now().strftime("%Y_%m_%d/%H_%M_%S_%f"), ext)
            s3.meta.client.upload_fileobj(f, settings.AWS_STORAGE_BUCKET_NAME, key)
            exp_link_list.append("http://"+settings.AWS_S3_CUSTOM_DOMAIN+'/'+key)

        exp_data = list(zip(exp_link_list, json.loads(request.POST['exp'])))

        if len(prev_vol) == 0:
            vol = VolunteerForm(request.POST)
        else:
            vol = VolunteerForm(request.POST, instance=prev_vol[0])

        if vol.is_valid():
            new_vol = vol.save(commit=False)
            new_vol.user = request.user
            new_vol.certificate = cert_link_list
            new_vol.experience = exp_data
            new_vol.save()
            return JsonResponse({"ok": True, "vid": new_vol.id})
            # return redirect('view_volunteer', gid=new_vol.id)
        else:
            print(vol.errors)
            return JsonResponse({"ok": False})

    else:
        if prev_vol:
            form = VolunteerForm(instance=prev_vol[0])
        else:
            form = VolunteerForm()
        return flavour_render(request, "guide/volunteer.html", {"form": form, "type_list": GUIDE_TYPE,
                                                                'theme_list': GUIDE_THEME})


def view_volunteer(request, gid):
    guide = Guide.objects.get(id=gid)
    return flavour_render(request, "guide/view_volunteer.html", {'guide': guide})


def enroll_volunteer(request, gid):
    volunteer = Guide.objects.get(id=gid)
    volunteer.is_volunteer = True
    volunteer.save()
    return redirect(dashboard)


@user_passes_test(guide_required)
def find(request):
    return flavour_render(request, "guide/find.html", {"tab": "find"})


def dashboard(request):
    notice_list = Notice.objects.order_by('-modified_at')
    stats = (("누적활동일수", "0일"), ("누적예약수", "0건"), ("누적여행자수", "0명"))
    return flavour_render(request, "guide/dashboard.html", {"tab": "dashboard", "notice_list": notice_list,
                                                            "stats": stats, "review_cnt": 0})


@user_passes_test(guide_required)
def schedule(request):
    return flavour_render(request, "guide/find.html", {"tab": "schedule"})


@user_passes_test(guide_required)
def request(request):
    return flavour_render(request, "guide/request_offer.html", {"tab": "request"})


@user_passes_test(guide_required)
def adjust(request):
    return flavour_render(request, "guide/find.html", {"tab": "adjust"})


@user_passes_test(guide_required)
def review(request):
    return flavour_render(request, "guide/find.html", {"tab": "review"})


@user_passes_test(guide_required)
def message(request):
    return flavour_render(request, "guide/find.html", {"tab": "message"})


def inactivate(request):
    guide = request.user.guide.all()[0]
    guide.activated = False
    guide.save()
    return redirect(dashboard)


def activate(request):
    guide = request.user.guide.all()[0]
    guide.activated = True
    guide.save()
    return redirect(dashboard)


class FilterTrip(View):
    def get(self, request):
        guide_id = Guide.objects.get(user_id=request.user.id).id

        result = []
        location = request.GET.getlist('location[]')
        print(location)
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        traveler_cnt = request.GET.get('traveler_cnt')
        sort = request.GET.get('sort')

        req_queryset = UserRequest.objects.select_related('user').all()
        if traveler_cnt:
            req_queryset = req_queryset.filter(total_traveler__lte=int(traveler_cnt.split()[1][:-1]))

        if bool(start_date) & bool(end_date):
            start_date = parse_date(start_date.replace('.', '-'))
            end_date = parse_date(end_date.replace('.', '-'))
            req_queryset = req_queryset.filter(travel_begin_at__gte=start_date, travel_end_at__lte=end_date)

        # if sort == "popularity":
        #     guide_queryset = guide_queryset.order_by('-pay_cnt')
        #
        # elif sort == "reviewNum":
        #     guide_queryset = guide_queryset.annotate(num_reviews=Count('userreview')).order_by('num_reviews')

        for req in req_queryset:
            temp = {'id': req.id,
                    'name': req.user.profile.full_name,
                    'profile_pic': req.user.profile.photo.url,
                    'travel_begin_at': formats.date_format(req.travel_begin_at, "Y/m/d"),
                    'travel_end_at': formats.date_format(req.travel_end_at, "Y/m/d"),
                    'city': req.city,
                    'adult_traveler': req.adult_traveler,
                    'child_traveler': req.child_traveler,
                    'cost': req.cost,
                    'is_liked': GuideLike.objects.filter(guide_id=guide_id,
                                                         request_id=req.id).exists(),
                    'trans_guided': req.trans_guided,
                    'accom_guided': req.accom_guided,
                    'guide_guided': req.guide_guided
                    }
            result.append(temp)
        result += [guide_id]
        return JsonResponse(result, safe=False)


@login_required
def write_offer(request, req_id):
    guide_id = Guide.objects.prefetch_related('accom_templates').prefetch_related('guide_templates').get(user_id=request.user.id).id
    req = get_object_or_404(UserRequest.objects.select_related('user'), id=req_id)
    # offer = GuideOffer.objects.create(guide_id=guide_id, request_id=req_id)
    is_liked = GuideLike.objects.filter(guide_id=guide_id, request_id=req.id)

    return flavour_render(request, 'guide/write_offer.html', {'req': req,
                                                              'is_liked': is_liked,
                                                              'guide_id': guide_id})


# 숙소 템플릿 검색
def search_accom(request, req_id):
    if request.is_ajax():
        guide_id = request.GET.get('guide_id')
        title = request.GET.get('title')
        s_id = 'accom_search' + str(request.GET.get('s_id'))
        accom_template_result = AccomTemplate.objects.filter(title__icontains=title, guide_id=guide_id, overwritten=False).order_by('title')
        paginator = Paginator(accom_template_result, 5)
        if accom_template_result:
            page = request.GET.get('page')
            try:
                accom_template_set = paginator.page(page)
            except PageNotAnInteger:
                # If page is not an integer, deliver first page.
                accom_template_set = paginator.page(1)
            except EmptyPage:
                # If page is out of range (e.g. 9999), deliver last page of results.
                accom_template_set = paginator.page(paginator.num_pages)

        else:
            accom_template_set = ''

        html = render_to_string('pc/guide/accom_result.html', {'accom_template_set': accom_template_set, 'id': s_id, 'title': title})
        return HttpResponse(html)


# 가이드 템플릿 검색
def search_guide(request, req_id):
    if request.is_ajax():
        guide_id = request.GET.get('guide_id')
        title = request.GET.get('title')
        guide_template_result = GuideTemplate.objects.filter(title__icontains=title, guide_id=guide_id, overwritten=False).order_by('title')
        paginator = Paginator(guide_template_result, 5)
        if guide_template_result:
            page = request.GET.get('page')
            try:
                guide_template_set = paginator.page(page)
            except PageNotAnInteger:
                # If page is not an integer, deliver first page.
                guide_template_set = paginator.page(1)
            except EmptyPage:
                # If page is out of range (e.g. 9999), deliver last page of results.
                guide_template_set = paginator.page(paginator.num_pages)

        else:
            guide_template_set = ''

        html = render_to_string('pc/guide/guide_result.html', {'guide_template_set': guide_template_set})
        return HttpResponse(html)
    return JsonResponse({"ok": False})


# 이동수단 폼 저장
def save_trans(request, req_id):
    if request.is_ajax():
        guide_id = request.GET.get('guide_id')
        trans_info = request.GET.get('trans_info')
        offer = GuideOffer.objects.filter(guide_id=guide_id, request_id=req_id).last()
        offer.trans_info = trans_info
        offer.save()
        return HttpResponse()
    return JsonResponse({"ok": False})


def new_accom_form(request, req_id):
    if request.is_ajax():
        form_id = 'accom_form' + str(request.GET.get('id'))
        search_id = 'accom_search' + str(request.GET.get('id'))
        accom_form = render_to_string('pc/guide/accom_template_form.html', {'id': form_id}) + '<!--!>'
        accom_search = render_to_string('pc/guide/accom_result.html', {'id': search_id})
        return HttpResponse(accom_form + accom_search)
    return JsonResponse({"ok": False})


def new_cost_form(request, req_id):
    if request.is_ajax():
        form_id = 'cost_form' + str(request.GET.get('id'))
        cost_form = render_to_string('pc/guide/cost_form.html', {'id': form_id})
        return HttpResponse(cost_form)
    return JsonResponse({"ok": False})


def load_accom(request, req_id):
    if request.is_ajax():
        accom_id = request.GET.get('accom_id')
        form_id = 'accom_form' + str(request.GET.get('id'))

        accom_template = AccomTemplate.objects.get(id=accom_id)
        html = render_to_string('pc/guide/accom_template_form.html', {'id': form_id, 'accom_template': accom_template})
        return HttpResponse(html)
    return JsonResponse({"ok": False})


def upload_accom_photo(request):
    if request.method == "POST":
        files = request.FILES
        s3 = boto3.resource("s3", aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)
        file_ext = files['accom_photo'].name.split(".")[-1]
        tmp_name = datetime.datetime.now().strftime("%Y_%m_%d/%H_%M_%S_%f")+"."+file_ext
        img = Image.open(files['accom_photo'])
        tmp_file = "/tmp/{}.jpg".format(uuid4())
        img.save(tmp_file, format="jpeg")
        s3.meta.client.upload_file(tmp_file, settings.AWS_STORAGE_BUCKET_NAME,
                                      "accom_photo/{}".format(tmp_name))
        url = "http://" + "/".join([settings.AWS_S3_CUSTOM_DOMAIN, "accom_photo", tmp_name])
        return JsonResponse({"ok": True, "url": url})
    return JsonResponse({"ok": False})


def save_accom_template(request):
    if request.method == "POST":
        guide_id = request.POST.get('guide_id')
        accom_template_id = request.POST.get('accom_template_id')
        title = request.POST.get('title')
        content = request.POST.get('content')
        address = [request.POST.get('country'), request.POST.get('city'), request.POST.get('small_city')]
        lat = request.POST.get('lat')
        lng = request.POST.get('lng')
        type_id = int(request.POST.get('type_id'))

        # 이전 내용 덮어쓰기
        if accom_template_id:
            a = AccomTemplate.objects.get(id=accom_template_id, guide_id=guide_id)
            a.overwritten = True
            a.save()
        # 새로 저장
        a = AccomTemplate.objects.create(guide_id=guide_id, title=title, content=content, address=address, lat=lat, lng=lng, type_id=type_id)
        return JsonResponse({"ok": True, "new_id": a.id})
    return JsonResponse({"ok": False})
