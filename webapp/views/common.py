# from django.shortcuts import render

from bravepeach.util import flavour_render
from ..forms import GuideSearchFrom
from django.shortcuts import redirect


def index(request):
    if request.method == 'GET':
        form = GuideSearchFrom(request.GET)
        if request.GET.__contains__('city'):
            city = request.GET.__getitem__('city')
        if request.GET.__contains__('travel_begin_at'):
            travel_begin_at = request.GET.__getitem__('travel_begin_at')
        if request.GET.__contains__('travel_end_at'):
            travel_end_at = request.GET.__getitem__('travel_end_at')
        if request.GET.__contains__('age_group'):
            age_group = request.GET.__getitem__('age_group')
        if form.is_valid():
            return flavour_render(request, "trip/guide_search.html", {'city': city,
                                                                      'travel_begin_at': travel_begin_at,
                                                                      'travel_end_at':travel_end_at,
                                                                      'age_group': age_group,
                                                                      })
    else:
        form = GuideSearchFrom()

    return flavour_render(request, "index.html", {'form': form})
