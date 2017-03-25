import datetime

from django.shortcuts import get_object_or_404

from bravepeach.util import flavour_render
from ..models import Guide, GuideOffer, UserReview, UserRequest, GuideLike
from django.views.generic import View
from django.utils.dateparse import parse_date
from django.http import JsonResponse
from django.utils import formats


def profile(request, gid):
    guide = get_object_or_404(Guide.objects.select_related('user'), id=gid)
    recent_trip = (GuideOffer.objects.filter(paid=True, is_canceled=False, guide=guide,
                                             request__travel_end_at__lt=datetime.date.today())
                   .select_related('request').order_by('-request__travel_end_at')).all()[:5]
    review_list = UserReview.objects.filter(receiver=guide).order_by('-id')
    return flavour_render(request, "guide/profile.html", {"guide": guide, "recent_trip": recent_trip,
                                                          "reviews": review_list,
                                                          "review_ids": [x.offer_id for x in review_list]})


def guide_index(request):
    if request.user.is_authenticated:
        return flavour_render(request, "guide/index.html", {})
    else:
        return flavour_render(request, "guide/index_not_login.html", {})


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

        req_queryset = UserRequest.objects.all()
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
                                                         request_id=req.id).exists()
                    }
            result.append(temp)
        result += [guide_id]
        return JsonResponse(result, safe=False)
