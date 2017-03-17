import json
import datetime
from collections import OrderedDict

from django.shortcuts import redirect
from django.http import JsonResponse
from django.db.models import Count, Case, When
from django.views.generic import View
from django.contrib.auth.decorators import login_required

from bravepeach.util import flavour_render
from ..forms import RequestForm
from ..models import Guide, Review, UserRequest, GuideOffer, Like


def guide_search(request):
    return flavour_render(request, 'trip/guide_search.html', {})


class FilterGuide(View):
    def get(self, request):
        result = []
        location = request.GET.get('location')
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        traveler_cnt = request.GET.get('traveler_cnt')
        sort = request.GET.get('sort')

        guide_queryset = Guide.objects.all()
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
            guide_id_list = Review.objects.values('receiver').annotate(
                receiver_cnt=Count(
                    Case(
                        When(
                            receiver__startswith='G', then=1
                        )
                    )
                )
            ).order_by('-receiver_cnt').values_list('receiver', flat=True)

            guide_id_list = [int(i[1:]) for i in guide_id_list]
            guide_queryset = [Guide.objects.get(id=i) for i in guide_id_list]

        for guide in guide_queryset:
            print(Like.objects.filter(from_id=request.user.id, to_id=guide.id).exists())
            temp = {'id': guide.id,
                    'rating': guide.rating,
                    'pay_cnt': guide.pay_cnt,
                    'guide_location': guide.guide_location,
                    'first_name': guide.user.first_name,
                    'last_name': guide.user.last_name,
                    'review_num': Review.objects.filter(receiver=guide.id).count(),
                    'is_liked': Like.objects.filter(from_id=request.user.id, to_id=guide.id).exists()}
            result.append(temp)
        result += [request.user.id]
        return JsonResponse(result, safe=False)


@login_required
def enroll_trip(request):
    if request.method == 'POST':
        cities = request.POST["city"].replace(' ', '').split(',')
        age_group = [int(x) for x in request.POST["age_group"].split(',')]
        data = request.POST.copy()
        data['city'] = json.dumps(cities)
        data['age_group'] = json.dumps(age_group)
        data['user'] = request.user.id

        for key in ['trans_via', 'trans_type', 'accom_location', 'accom_type', 'theme', 'guide_type', 'importance']:
            if data.__contains__(key):
                new_value = sum([int(i) for i in data.getlist(key)])
                data.update({key: new_value})

        form = RequestForm(data)

        if form.is_valid():
            form.save()
            return redirect('index')
        else:
            print(form.errors)
            return redirect("enroll_trip")
    else:
        form = RequestForm()
        return flavour_render(request, 'trip/enroll_trip.html', {'form': form})


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
    guide_id_list = [i.guide_id for i in Like.objects.filter(user_id=request.user.id).order_by('-id')]
    guide_list = Guide.objects.filter(id__in=guide_id_list).extra(
        select={'manual': 'FIELD(id,%s)' % ','.join(map(str, guide_id_list))},
        order_by=['manual']
    )

    return flavour_render(request, 'trip/like.html', {"guide_list": guide_list})


class AddLike(View):
    def get(self, request):
        user_id = request.GET.get('user_id')
        guide_id = request.GET.get('guide_id')
        Like.objects.create(user_id=user_id, guide_id=guide_id)
        return JsonResponse({"ok": True})


class DeleteLike(View):
    def get(self, request):
        user_id = request.GET.get('user_id')
        guide_id = request.GET.get('guide_id')
        Like.objects.filter(user_id=user_id, guide_id=guide_id).delete()
        return JsonResponse({"ok": True})
