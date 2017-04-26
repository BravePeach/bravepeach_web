import json
import datetime

import requests
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


@login_required
def chat_user(request, uid):
    rooms = Room.objects.filter(Q(user_1=request.user) | Q(user_2=request.user)).all()
    room_dict = {x.id: x for x in rooms}
    room_id_list = [x.id for x in rooms]
    scheme = request.is_secure() and "https:" or "http:"
    resp = requests.post("{}//api.bravepeach.com/get_last_chats".format(scheme),
                         data=json.dumps({"room_list": room_id_list})).json()
    last_chat_list = []
    for r in resp:
        room = r[0]
        d = r[1]
        d["timestamp"] = datetime.datetime.strptime(d["timestamp"], "%Y-%m-%d %H:%M:%S")
        if room_dict[room].user_1 == request.user:
            d["opponent"] = room_dict[room].user_2
        else:
            d["opponent"] = room_dict[room].user_1
        last_chat_list.append((room, d))
        del room_dict[room]
    for room_id, room in room_dict.items():
        if room.user_1 == request.user:
            last_chat_list.append({"opponent": room.user_2, "timestamp": datetime.datetime.now(),
                                   "content": "", "writer": request.user.id})
        else:
            last_chat_list.append({"opponent": room.user_1, "timestamp": datetime.datetime.now(),
                                   "content": "", "writer": request.user.id})
    scheme = request.is_secure() and "wss:" or "ws:"
    return render(request, "pc/chat.html", {"rooms": last_chat_list, "chat_host": scheme+CHAT_HOST, "active": int(uid)})


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
