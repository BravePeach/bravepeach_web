from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from bravepeach.util import flavour_render
from ..forms import GuideSearchFrom
from ..models import GuideAlarm, UserAlarm


def index(request):
    form = GuideSearchFrom()
    return flavour_render(request, "index.html", {'form': form})


@login_required
def get_alarm(request):
    req_type = request.GET.get('type', "")
    if req_type == "user":
        alarm_list = UserAlarm.objects.filter(receiver=request.user, immediate=True, is_new=True).all()
        alarm_cnt = len(alarm_list)
    elif req_type == "guide" and request.user.profile.is_guide:
        alarm_list = GuideAlarm.objects.filter(receiver=request.user.guide.first(), immediate=True, is_new=True).all()
        alarm_cnt = len(alarm_list)
    else:
        return JsonResponse({"ok": False})
    alarm_list.update(is_new=False)
    return JsonResponse({"ok": True, "alarm_cnt": alarm_cnt})
