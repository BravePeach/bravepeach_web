from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from webapp.models import Room


@login_required
def chat_index(request):
    rooms = Room.objects.all()
    return render(request, "pc/chat.html", {"rooms": rooms})


@login_required
def make_room(request):
    if request.method == "POST":
        opponent = int(request.POST.get('opponent'))
        opponent_user = User.objects.filter(id=opponent).first()
        uid_list = [request.user.id, opponent]
        uid_list.sort()
        room_name = "{} 와 {} 의 대화".format(request.user.profile.full_name, opponent_user.profile.full_name)
        new_room = Room(title=room_name)
        new_room.save()
        return JsonResponse({"ok": True, "room_id": new_room.id, "room_title": room_name})
