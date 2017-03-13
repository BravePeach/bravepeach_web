# from django.shortcuts import render

from bravepeach.util import flavour_render


def index(request):
    return flavour_render(request, "index.html")
