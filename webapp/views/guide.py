import datetime

from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from bravepeach.util import flavour_render
from ..models import Guide, GuideOffer, Review


def profile(request, gid):
    guide = get_object_or_404(Guide.objects.select_related('user'), id=gid)
    recent_trip = (GuideOffer.objects.filter(paid=True, is_canceled=False, guide=guide,
                                             request__travel_end_at__lt=datetime.date.today())
                   .select_related('request').order_by('-request__travel_end_at')).all()[:5]
    review_list = Review.objects.filter(guide_id=guide.id).order_by('-id')
    return flavour_render(request, "guide/profile.html", {"guide": guide, "recent_trip": recent_trip,
                                                          "rating": range(guide.clean_rating[0]),
                                                          "norating": range(4-guide.clean_rating[0]),
                                                          "reviews": review_list,
                                                          "review_ids": [x.offer_id for x in review_list]})
