import datetime
from dateutil.rrule import rrule, DAILY

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
                       Notice, Cost, GuideAdjust, GuideReview, Journal)
from ..forms import (WriteOfferForm, VolunteerForm, GuideAdjustForm, GuideReviewForm, JournalForm)
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
    return flavour_render(request, "guide/index.html", {"tab": "find"})


@login_required
def dashboard(request):
    notice_list = Notice.objects.order_by('-modified_at')
    stats = (("누적활동일수", "0일"), ("누적예약수", "0건"), ("누적여행자수", "0명"))
    return flavour_render(request, "guide/dashboard.html", {"tab": "dashboard", "notice_list": notice_list,
                                                            "stats": stats, "review_cnt": 0})


@user_passes_test(guide_required)
def schedule(request):
    page_type = request.GET.get("type", '')
    guide = Guide.objects.get(user=request.user)
    fixed_offer_set = GuideOffer.objects.filter(guide=guide, paid=True, request__travel_end_at__gte=datetime.date.today(), is_canceled=False)
    fixed_offer_price = [o.total_cost for o in fixed_offer_set]
    fixed_trip_set = UserRequest.objects.filter(id__in=[r.request_id for r in fixed_offer_set])
    ended_offer_set = GuideOffer.objects.filter(guide=guide, paid=True, request__travel_end_at__lt=datetime.date.today(), is_canceled=False)
    ended_offer_price = [o.total_cost for o in ended_offer_set]
    ended_trip_set = UserRequest.objects.filter(id__in=[r.request_id for r in ended_offer_set])
    canceled_offer_set = GuideOffer.objects.filter(guide=guide, is_canceled=True)
    canceled_trip_set = UserRequest.objects.filter(id__in=[r.request_id for r in canceled_offer_set])
    canceled_offer_price = [o.total_cost for o in canceled_offer_set]
    return flavour_render(request, "guide/schedule.html", {"tab": "schedule", "page_type": page_type,
                                                           "fixed_trip_set": fixed_trip_set,
                                                           "fixed_offer_price": fixed_offer_price,
                                                           "ended_trip_set": ended_trip_set,
                                                           "ended_offer_price": ended_offer_price,
                                                           "canceled_trip_set": canceled_trip_set,
                                                           "canceled_offer_price": canceled_offer_price,
                                                           })


@user_passes_test(guide_required)
def template(request):
    return


@user_passes_test(guide_required)
def request(request):
    page_type = request.GET.get("type", '')
    guide = request.user.guide.all()[0]

    request_list = UserRequest.objects.all()
    zzim_list = GuideLike.objects.filter(guide=guide.id).all()
    offer_list = GuideOffer.objects.filter(guide=guide.id).all()

    return flavour_render(request, "guide/request_offer.html", {"tab": "request", "page_type": page_type,
                                                                "request_list": request_list, "zzim_list": zzim_list,
                                                                "offer_list": offer_list})


@user_passes_test(guide_required)
def adjust(request):
    page_type = request.GET.get('type', '')
    prev_form = GuideAdjust.objects.filter(guide=request.user.guide.first()).first()
    if prev_form:
        form = GuideAdjustForm(instance=prev_form)
    else:
        form = GuideAdjustForm()

    revenue_list = GuideOffer.objects.filter(request__travel_end_at__lt=datetime.date.today(),
                                             adjust_done_at__isnull=False).order_by('-request__travel_end_at').all()
    expect_list = GuideOffer.objects.filter(request__travel_end_at__lt=datetime.date.today(),
                                            adjust_done_at__isnull=True).order_by('-request__travel_end_at').all()
    return flavour_render(request, "guide/adjust.html", {"tab": "adjust", "form": form, 'revenue_list': revenue_list,
                                                         'expect_list': expect_list, "page_type": page_type})


def set_adjust_method(request):
    if request.method == "POST":
        prev_form = GuideAdjust.objects.filter(guide=request.user.guide.first()).first()
        if prev_form:
            form = GuideAdjustForm(request.POST, instance=prev_form)
        else:
            form = GuideAdjustForm(request.POST)

        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.guide = request.user.guide.first()
            new_form.save()
        else:
            print(form.errors)
    return redirect(adjust)


def request_adjust(request, oid):
    offer = GuideOffer.objects.filter(id=oid).first()
    offer.adjust_requested_at = datetime.date.today()
    offer.save()
    return redirect(adjust)


@user_passes_test(guide_required)
def review(request):
    guide = Guide.objects.filter(user_id=request.user.id).all()[0]
    review_list = UserReview.objects.filter(receiver=guide).order_by('-id').all()
    write_list = GuideOffer.objects.filter(guide_review__isnull=True).order_by('id').all()
    send_list = GuideReview.objects.filter(writer=guide).order_by('-id').all()
    journal_write_list = GuideOffer.objects.filter(journal__isnull=True).order_by('id').all()
    journal_list = Journal.objects.filter(writer=guide).order_by('-id').all()
    return flavour_render(request, "guide/review.html", {"tab": "review", 'review_list': review_list,
                                                         "write_list": write_list, "send_list": send_list,
                                                         "journal_write_list": journal_write_list,
                                                         "journal_list": journal_list})


def write_review(request, oid):
    offer = get_object_or_404(GuideOffer, id=oid)

    if request.method == "POST":
        form = GuideReviewForm(request.POST)
        if form.is_valid():
            new_review = form.save(commit=False)
            new_review.write_date = datetime.date.today()
            new_review.writer = request.user.guide.all()[0]
            new_review.offer_id = oid
            new_review.receiver = offer.request.user
            new_review.save()
        return redirect(review)
    else:
        form = GuideReviewForm()
        return flavour_render(request, "guide/write_review.html", {"offer": offer, "form": form})


def view_review(request, rid):
    review = GuideReview.objects.filter(id=rid).first()
    return flavour_render(request, "guide/view_review.html", {"review": review})


def write_journal(request, oid):
    offer = get_object_or_404(GuideOffer, id=oid)

    if request.method == "POST":
        print(request.FILES)
        print(request.POST)
        form = JournalForm(request.POST, request.FILES)
        if form.is_valid():
            new_journal = form.save(commit=False)
            new_journal.write_date = datetime.date.today()
            new_journal.writer = request.user.guide.first()
            new_journal.offer = offer
            new_journal.save()
        else:
            print(form.errors)
        return redirect(review)
    else:
        form = JournalForm()
        return flavour_render(request, "guide/write_journal.html", {"offer": offer, "form": form})


def view_journal(request, jid):
    journal = Journal.objects.filter(id=jid).first()
    return flavour_render(request, "guide/view_journal.html", {"journal": journal})


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


@user_passes_test(guide_required)
def write_offer(request, req_id):
    guide_id = Guide.objects.prefetch_related('accom_templates').prefetch_related('guide_templates').get(user_id=request.user.id).id
    req = get_object_or_404(UserRequest.objects.select_related('user'), id=req_id)
    # offer = GuideOffer.objects.create(guide_id=guide_id, request_id=req_id)
    is_liked = GuideLike.objects.filter(guide_id=guide_id, request_id=req.id)

    date_list = [i.strftime("%Y/%m/%d") for i in rrule(DAILY, dtstart=req.travel_begin_at, until=req.travel_end_at)]

    return flavour_render(request, 'guide/write_offer.html', {'req': req,
                                                              'is_liked': is_liked,
                                                              'guide_id': guide_id,
                                                              'date_list': date_list})


@user_passes_test(guide_required)
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


@user_passes_test(guide_required)
def search_guide(request, req_id):
    if request.is_ajax():
        guide_id = request.GET.get('guide_id')
        title = request.GET.get('title')
        s_id = 'guide_search' + str(request.GET.get('s_id'))
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

        html = render_to_string('pc/guide/guide_result.html', {'guide_template_set': guide_template_set, 'id': s_id, 'title': title})
        return HttpResponse(html)
    return JsonResponse({"ok": False})


@user_passes_test(guide_required)
def new_accom_form(request, req_id):
    if request.is_ajax():
        form_id = 'accom_form' + str(request.GET.get('id'))
        search_id = 'accom_search' + str(request.GET.get('id'))
        accom_form = render_to_string('pc/guide/accom_template_form.html', {'id': form_id}) + '<!--!>'
        accom_search = render_to_string('pc/guide/accom_result.html', {'id': search_id})
        return HttpResponse(accom_form + accom_search)
    return JsonResponse({"ok": False})


@user_passes_test(guide_required)
def new_cost_form(request, req_id):
    if request.is_ajax():
        form_id = 'cost_form' + str(request.GET.get('id'))
        cost_form = render_to_string('pc/guide/cost_form.html', {'id': form_id})
        return HttpResponse(cost_form)
    return JsonResponse({"ok": False})


@user_passes_test(guide_required)
def new_guide_form(request, req_id):
    if request.is_ajax():
        form_id = 'guide_form' + str(request.GET.get('id'))
        search_id = 'guide_search' + str(request.GET.get('id'))
        date = request.GET.get('date')
        guide_form = render_to_string('pc/guide/guide_template_form.html', {'id': form_id, 'date': date}) + '<!--!>'
        guide_search = render_to_string('pc/guide/guide_result.html', {'id': search_id, 'date': date})
        return HttpResponse(guide_form + guide_search)
    return JsonResponse({"ok": False})


@user_passes_test(guide_required)
def load_accom(request, req_id):
    if request.is_ajax():
        accom_id = request.GET.get('accom_id')
        form_id = 'accom_form' + str(request.GET.get('id'))

        accom_template = AccomTemplate.objects.get(id=accom_id)
        html = render_to_string('pc/guide/accom_template_form.html', {'id': form_id, 'accom_template': accom_template})
        return HttpResponse(html)
    return JsonResponse({"ok": False})


@user_passes_test(guide_required)
def load_guide(request, req_id):
    if request.is_ajax():
        guide_template_id = request.GET.get('guide_id')
        form_id = 'guide_form' + str(request.GET.get('id'))
        date = request.GET.get('date')
        guide_template = GuideTemplate.objects.get(id=guide_template_id)
        html = render_to_string('pc/guide/guide_template_form.html', {'id': form_id, 'guide_template': guide_template, 'date':date})
        return HttpResponse(html)
    return JsonResponse({"ok": False})


@user_passes_test(guide_required)
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


@user_passes_test(guide_required)
def upload_guide_photo(request):
    if request.method == "POST":
        files = request.FILES
        s3 = boto3.resource("s3", aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)
        file_ext = files['guide_photo'].name.split(".")[-1]
        tmp_name = datetime.datetime.now().strftime("%Y_%m_%d/%H_%M_%S_%f")+"."+file_ext
        img = Image.open(files['guide_photo'])
        tmp_file = "/tmp/{}.jpg".format(uuid4())
        img.save(tmp_file, format="jpeg")
        s3.meta.client.upload_file(tmp_file, settings.AWS_STORAGE_BUCKET_NAME,
                                      "guide_photo/{}".format(tmp_name))
        url = "http://" + "/".join([settings.AWS_S3_CUSTOM_DOMAIN, "guide_photo", tmp_name])
        return JsonResponse({"ok": True, "url": url})
    return JsonResponse({"ok": False})


@user_passes_test(guide_required)
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


@user_passes_test(guide_required)
def save_guide_template(request):
    if request.method == "POST":
        guide_id = request.POST.get('guide_id')
        guide_template_id = request.POST.get('guide_template_id')
        title = request.POST.get('title')
        content = request.POST.get('content')

        # 이전 내용 덮어쓰기
        if guide_template_id:
            a = GuideTemplate.objects.get(id=guide_template_id, guide_id=guide_id)
            a.overwritten = True
            a.save()
        # 새로 저장
        a = GuideTemplate.objects.create(guide_id=guide_id, title=title, content=content, photo="")
        return JsonResponse({"ok": True, "new_id": a.id})
    return JsonResponse({"ok": False})


@user_passes_test(guide_required)
def save_trans_offer(request, req_id):
    if request.method == "POST":
        guide_id = request.POST.get('guide_id')
        trans_info = request.POST.get('trans_info')

        if not GuideOffer.objects.filter(guide_id=guide_id, request_id=req_id).exists():
            req = UserRequest.objects.get(id=req_id)
            travel_period = [i for i in rrule(DAILY, dtstart=req.travel_begin_at, until=req.travel_end_at)]
            GuideOffer.objects.create(guide_id=guide_id, request_id=req_id, trans_info=trans_info, travel_period=travel_period)

        else:
            g = GuideOffer.objects.get(guide_id=guide_id, request_id=req_id)
            g.trans_info = trans_info
            g.save()

        return JsonResponse({"ok": True})
    return JsonResponse({"ok": False})


def get_weekday(i):
    weekday = ('월', '화', '수', '목', '금', '토', '일')
    return weekday[i]


@user_passes_test(guide_required)
def save_accom_offer(request, req_id):
    if request.method == "POST":
        guide_id = request.POST.get('guide_id')
        accom_id = request.POST.get('accom_id').split(',')
        accom_date = request.POST.get('accom_date').split(',')
        accom_template = list(zip(accom_date, accom_id))

        if not GuideOffer.objects.filter(guide_id=guide_id, request_id=req_id).exists():
            req = UserRequest.objects.get(id=req_id)
            travel_period = [i for i in rrule(DAILY, dtstart=req.travel_begin_at, until=req.travel_end_at)]
            GuideOffer.objects.create(guide_id=guide_id, request_id=req_id, accom_template=accom_template, travel_period=travel_period)

        else:
            g = GuideOffer.objects.get(guide_id=guide_id, request_id=req_id)
            g.accom_template = accom_template
            g.save()

        return JsonResponse({"ok": True})
    return JsonResponse({"ok": False})


@user_passes_test(guide_required)
def save_guide_offer(request, req_id):
    if request.method == "POST":
        guide_id = request.POST.get('guide_id')
        guide_template = request.POST.get('guide_template').split('dumpstring')[:-1]

        for i, j in enumerate(guide_template):
            guide_template[i] = j.split(',')

        if not GuideOffer.objects.filter(guide_id=guide_id, request_id=req_id).exists():
            req = UserRequest.objects.get(id=req_id)
            travel_period = [i for i in rrule(DAILY, dtstart=req.travel_begin_at, until=req.travel_end_at)]
            GuideOffer.objects.create(guide_id=guide_id, request_id=req_id, guide_template=guide_template, travel_period=travel_period)

        else:
            g = GuideOffer.objects.get(guide_id=guide_id, request_id=req_id)
            g.guide_template = guide_template
            g.save()

        return JsonResponse({"ok": True})
    return JsonResponse({"ok": False})


@user_passes_test(guide_required)
def save_cost_offer(request, req_id):
    if request.method == "POST":
        guide_id = request.POST.get('guide_id')
        type_id_list = request.POST.get('type_id_list').split(',')
        price_list = request.POST.get('price_list').split(',')
        info_list = request.POST.get('info_list').split(',')
        offer_id = GuideOffer.objects.get(guide_id=guide_id, request_id=req_id).id
        print(type_id_list)
        for i in range(len(type_id_list)):
            Cost.objects.get_or_create(offer_id=offer_id, type_id=type_id_list[i], price=price_list[i], info=info_list[i])

        return JsonResponse({"ok": True})
    return JsonResponse({"ok": False})
