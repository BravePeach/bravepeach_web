import datetime

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404

from bravepeach.util import flavour_render
from ..models import Guide, GuideOffer, UserReview, UserRequest, GuideLike, AccomTemplate, GuideTemplate
from ..forms import WriteOfferForm
from django.views.generic import View
from django.utils.dateparse import parse_date
from django.http import JsonResponse
from django.utils import formats
from django.shortcuts import redirect


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
    guide_id = Guide.objects.get(user_id=request.user.id).id
    req = get_object_or_404(UserRequest.objects.select_related('user'), id=req_id)
    is_liked = GuideLike.objects.filter(guide_id=guide_id, request_id=req.id)

    if AccomTemplate.objects.filter(guide_id=guide_id).exists():
        accom_template_set = AccomTemplate.objects.get(guide_id=guide_id)

    else:
        accom_template_set = ''

    if GuideTemplate.objects.filter(guide_id=guide_id).exists():
        guide_template_set = GuideTemplate.objects.get(guide_id=guide_id)

    else:
        guide_template_set = ''

    if request.method == 'POST':
        # form 채우기
        form = WriteOfferForm()

        if form.is_valid():
            form.save()
            # 자기가 쓴 제안서 관리하는 페이지로 리다이렉트
            return redirect('index')
        else:
            print(form.errors)
            # 폼이 invalid 할때는 어떻게?
            return redirect("enroll_trip")
    else:
        form = WriteOfferForm()
        return flavour_render(request, 'guide/write_offer.html', {'form': form,
                                                                  'req': req,
                                                                  'accom_template_set': accom_template_set,
                                                                  'guide_template_set': guide_template_set,
                                                                  'is_liked': is_liked
                                                                  })
