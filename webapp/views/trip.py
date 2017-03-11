from ..models import Guide, Review
from django.http import JsonResponse
from django.db.models import Count, Case, When
from django.views.generic import View
from bravepeach.util import flavour_render


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
            temp = {'rating': guide.rating, 'pay_cnt': guide.pay_cnt, 'guide_location': guide.guide_location,
                    'first_name': guide.user.first_name, 'last_name': guide.user.last_name,
                    'review_num': Review.objects.filter(receiver='G' + str(guide.id)).count()}
            result.append(temp)

        return JsonResponse(result, safe=False)


def enroll_trip(request):
    return flavour_render(request, 'trip/enroll_trip.html', {})
