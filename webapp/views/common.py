# from django.shortcuts import render

from bravepeach.util import flavour_render
from ..forms import GuideSearchFrom
from django.shortcuts import redirect


def index(request):
    form = GuideSearchFrom()
    return flavour_render(request, "index.html", {'form': form})
