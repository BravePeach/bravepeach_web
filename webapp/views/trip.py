import json
import datetime
from collections import OrderedDict, defaultdict

from django.shortcuts import redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.db.models import Count, Case, When, Sum
from django.views.generic import View
from django.contrib.auth.decorators import login_required
from django.utils import formats
from django.template.loader import render_to_string

from bravepeach.util import flavour_render
from ..forms import RequestForm, GuideSearchFrom
from ..models import (Guide, UserReview, GuideReview, UserRequest, GuideOffer, UserLike, GuideLike, GuideTemplate,
                      AccomTemplate, Comment, Cost)
from django.utils import timezone


def guide_search(request):
    if request.GET:
        form = GuideSearchFrom(request.GET)
        city = request.GET.get('city')
        travel_begin_at = request.GET.get('travel_begin_at')
        travel_end_at = request.GET.get('travel_end_at')
        age_group = request.GET.get('age_group')
        if form.is_valid():
            return flavour_render(request, "trip/guide_search.html", {'city': city,
                                                                      'travel_begin_at': travel_begin_at,
                                                                      'travel_end_at': travel_end_at,
                                                                      'age_group': age_group,
                                                                      })
    else:
        return flavour_render(request, "trip/guide_search.html")


class FilterGuide(View):
    def get(self, request):
        country = request.GET.getlist('country[]')
        city = request.GET.getlist('city[]')
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        traveler_cnt = request.GET.get('traveler_cnt')
        sort = request.GET.get('sort')

        guide_queryset = Guide.objects.all()

        if country:
            guide_queryset = guide_queryset.filter(guide_country__has_any_keys=country)

        if city:
            guide_queryset = guide_queryset.filter(guide_city__has_any_keys=city)

        if traveler_cnt:
            guide_queryset = guide_queryset.filter(max_traveler_cnt__gte=int(traveler_cnt.split()[1][:-1]))

        if bool(start_date) & bool(end_date):
            travel_date = []
            for i in range(int(start_date.replace('.', '')), int(end_date.replace('.', '')) + 1):
                travel_date.append(str(i))
            guide_queryset = guide_queryset.exclude(off_day__has_any_keys=travel_date)

        if sort == "popularity":
            guide_queryset = guide_queryset.order_by('-pay_cnt')

        elif sort == "reviewNum":
            guide_queryset = guide_queryset.annotate(num_reviews=Count('userreview')).order_by('num_reviews')

        html = render_to_string('pc/trip/guide_search_result.html', {'guide_queryset': guide_queryset})
        return HttpResponse(html)


@login_required
def enroll_trip(request):
    if request.method == 'POST':
        cities = request.POST["city"].replace(' ', '').split(',')
        age_group = [int(x) for x in request.POST["age_group"].split(',')]
        data = request.POST.copy()
        data['city'] = json.dumps(cities)
        data['age_group'] = json.dumps(age_group)
        data['user'] = request.user.id

        for key in ['trans_via', 'trans_class', 'accom_location', 'accom_type', 'theme', 'local_trans', 'guide_type', 'importance']:
            if key in data:
                new_value = sum([int(i) for i in data.getlist(key)])
                data.update({key: new_value})

        form = RequestForm(data)

        if form.is_valid():
            form.save()
            user_request = UserRequest.objects.last()
            return flavour_render(request, 'trip/enroll_trip_detail.html', {'req': user_request})
        else:
            print(form.errors)
            return redirect("enroll_trip")
    else:
        form = RequestForm()
        return flavour_render(request, 'trip/enroll_trip.html', {'form': form})


@login_required
def my_trip_detail(request):
    return


@login_required
def my_trip(request):
    enroll_dict = OrderedDict()
    enroll_offer_dict = OrderedDict()
    enroll_paid_list = []

    enroll_list = UserRequest.objects.filter(user_id=request.user.id).order_by('-id')
    offer_list = (GuideOffer.objects.filter(request_id__in=[x.id for x in enroll_list])
                  .filter(request__travel_end_at__gte=datetime.date.today())).order_by('-id', '-paid', 'is_canceled')
    past_list = (GuideOffer.objects.filter(request_id__in=[x.id for x in enroll_list])
                 .filter(paid=True, is_canceled=False, request__travel_end_at__lt=datetime.date.today()))

    for enroll in enroll_list:
        enroll_dict[enroll.id] = enroll

    for offer in offer_list:
        if offer.paid:
            enroll_paid_list.append(offer)
        elif offer.request_id not in [x.request_id for x in enroll_paid_list]:
            if offer.request_id not in enroll_offer_dict:
                enroll_offer_dict[offer.request_id] = [enroll_dict[offer.request_id], 0]
            enroll_offer_dict[offer.request_id][1] += 1
        if offer.request_id in enroll_dict:
            del enroll_dict[offer.request_id]

    for enroll in enroll_dict.values():
        enroll_offer_dict[enroll.id] = [enroll, 0]

    enroll_offer_list = list(enroll_offer_dict.values())
    enroll_offer_list.sort(key=lambda x: (x[0].published, x[1], x[0].id), reverse=True)

    return flavour_render(request, "trip/my_trip.html", {"enroll_list": enroll_offer_list,
                                                         "offer_list": enroll_paid_list,
                                                         "past_list": past_list})


@login_required
def cancel_offer(request):
    offer_id = request.POST['offer_id']
    offer = GuideOffer.objects.filter(request__user_id=request.user.id, id=offer_id)
    if not offer:
        return JsonResponse({"ok": False})
    #offer.is_canceled = True
    # offer.save()
    return JsonResponse({"ok": True})


@login_required
def like(request):
    guide_id_list = [i.guide_id for i in UserLike.objects.filter(user_id=request.user.id).order_by('-id')]
    guide_list = Guide.objects.filter(id__in=guide_id_list).extra(
        select={'manual': 'FIELD(id,%s)' % ','.join(map(str, guide_id_list))},
        order_by=['manual']
    )
    return flavour_render(request, 'trip/like.html', {"guide_list": guide_list})


class AddLike(View):
    def get(self, request):
        user_id = request.GET.get('user_id')
        guide_id = request.GET.get('guide_id')
        UserLike.objects.create(user_id=user_id, guide_id=guide_id)
        return JsonResponse({"ok": True})


class DeleteLike(View):
    def get(self, request):
        user_id = request.GET.get('user_id')
        guide_id = request.GET.get('guide_id')
        UserLike.objects.filter(user_id=user_id, guide_id=guide_id).delete()
        return JsonResponse({"ok": True})


@login_required
def volunteer_list(request, user_request_id):
    user_request = get_object_or_404(UserRequest.objects.all(), id=user_request_id, user_id=request.user.id)
    guide_offer = GuideOffer.objects.select_related('guide').filter(request_id=user_request_id).order_by('-id')
    # guide_list = Guide.objects.filter(id__in=guide_offer.values('guide_id'))
    return flavour_render(request, 'trip/volunteer_list.html',
                          {"user_request": user_request, "guide_offers": guide_offer})


@login_required
def offer_detail(request, offer_id):
    guide_offer = get_object_or_404(GuideOffer.objects.select_related('guide').filter(pk=offer_id, request__user__id=request.user.id))

    g_template_qlist = []
    if guide_offer.guide_template:
        for id_list in guide_offer.guide_template:
            g_template_qlist += [GuideTemplate.objects.filter(id__in=id_list, guide_id=guide_offer.guide_id)
                                                      .extra(select={'manual': 'FIELD(id,%s)' % ','.join(map(str, id_list))},
                                                             order_by=['manual'])]

    a_template_list = guide_offer.accom_template
    for i in a_template_list:
        i[1] = AccomTemplate.objects.get(id=i[1])

    comment_q = Comment.objects.select_related('offer').filter(offer_id=offer_id).order_by('created_at')
    cost_qlist = []
    type_cost = []
    guide_commission = 0
    for type_id in range(7):
        cost_q = Cost.objects.select_related('offer').filter(offer_id=offer_id, type_id=type_id).order_by('id')
        if cost_q:
            cost_qlist += [cost_q]
            type_cost += [cost_q.aggregate(Sum('price'))['price__sum']]
            if type_id == 2:
                guide_commission = int(float(type_cost[-1]) * 0.12)

    total_cost = sum(type_cost) + guide_commission

    return flavour_render(request, 'trip/offer_detail.html', {"guide": guide_offer.guide,
                                                              "guide_offer": guide_offer,
                                                              "g_template_qlist": g_template_qlist,
                                                              "a_template_list": a_template_list,
                                                              "comment_q": comment_q,
                                                              "cost_qlist": cost_qlist,
                                                              "type_cost": type_cost,
                                                              "total_cost": total_cost,
                                                              "guide_commission": guide_commission,
                                                              })


@login_required
def payment(request, offer_id):
    param_dict = defaultdict(list)
    offer = GuideOffer.objects.select_related("request").get(id=offer_id)
    param_dict["offer"] = offer
    costs = Cost.objects.filter(offer=offer).all()
    for cost in costs:
        if cost.type == "trans":
            param_dict["trans_cost"].append(cost)
        elif cost.type == "accom":
            param_dict["accom_cost"].append(cost)
        elif cost.type == "guide":
            param_dict["guide_cost"].append(cost)
        else:
            pass
    param_dict["trans_total_cost"] = sum([x.cost for x in param_dict['trans_cost']])
    param_dict["accom_total_cost"] = sum([x.cost for x in param_dict['accom_cost']])
    param_dict["guide_total_cost"] = sum([x.cost for x in param_dict['guide_cost']])
    param_dict["guide_commission"] = param_dict["guide_total_cost"] * 0.12
    param_dict["total_cost"] = (param_dict["trans_total_cost"] + param_dict["accom_total_cost"] +
                                param_dict["guide_total_cost"] + param_dict["guide_commission"])
    param_dict["payment_deadline"] = datetime.date.today()+datetime.timedelta(days=2)
    return flavour_render(request, "trip/payment.html", param_dict)


class AddComment(View):
    def post(self, request):
        offer_id = request.POST.get('offer_id')
        writer = request.POST.get('user_id')
        content = request.POST.get('content')
        Comment.objects.create(writer=writer, content=content, offer_id=offer_id)
        c = Comment.objects.all().last()
        result = {'content': c.__dict__['content'], 'created_at': formats.date_format(timezone.localtime(c.__dict__['created_at']), "Y.m.d H:i")}
        return JsonResponse(result)
