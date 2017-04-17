from django.db.models import Q
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from webapp.models import Room
from bravepeach.settings import CHAT_HOST


@login_required
def chat_index(request):
    return redirect(chat_user, uid=0)
    # rooms = Room.objects.filter(Q(user_1=request.user) | Q(user_2=request.user)).all()
    # return render(request, "pc/chat.html", {"rooms": rooms, "chat_host": CHAT_HOST})


@login_required
def chat_user(request, uid):
    rooms = Room.objects.filter(Q(user_1=request.user) | Q(user_2=request.user)).all()
    return render(request, "pc/chat.html", {"rooms": rooms, "chat_host": CHAT_HOST, "active": int(uid)})


@login_required
def make_room(request):
    if request.method == "POST":
        opponent = int(request.POST.get('opponent'))
    else:
        opponent = int(request.GET.get('opponent'))
    opponent_user = User.objects.filter(id=opponent).first()
    uid_list = [request.user.id, opponent]
    uid_list.sort()
    room_name = "{} 님과 {} 님의 대화".format(request.user.profile.full_name, opponent_user.profile.full_name)
    room = Room.objects.filter(Q(user_1_id=uid_list[0]) | Q(user_2_id=uid_list[1])).first()
    if not room:
        room = Room(title=room_name, user_1_id=uid_list[0], user_2_id=uid_list[1])
        room.save()
    if request.POST.get('redirect', False):
        return redirect(chat_index)
    return JsonResponse({"ok": True, "room_id": room.id, "room_title": room_name})
