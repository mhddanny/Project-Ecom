from django.contrib.auth.decorators import login_required
from django.http import JsonResponse 
from django.utils.safestring import mark_safe
from django.shortcuts import render
from django.views.decorators.http import require_POST

from accounts.models import Account
from . models import Room
import json

# Create your views here.
def index(request):
    context = {
        
    }

    return render(request, 'chat/index.html', context)

@login_required
def room(request, room_name):
    context = {
        # content a
        "room_name": room_name,
        "username": request.user.username,

        # content b
        # "room_name_json": mark_safe(json.dumps(room_name)),
        # "username": mark_safe(json.dumps(request.user.username)),
    }
    return render(request, 'chat/room.html', context)

@require_POST
def create_room(request, uuid):
    name = request.POST.get('name', '')
    url = request.POST.get('url', '')

    Room.objects.create(uuid=uuid, client=name, url=url)

    return JsonResponse({'message': 'room created'})

@login_required
def chatAdmin(request):
    rooms = Room.objects.all()
    users = Account.object.filter(is_staff=True)

    context = {
        'rooms': rooms,
        'users': users
    }

    return render(request, 'chat/admin/chat_admin.html', context)

@login_required
def chatAdminRoom(request, uuid):
    room = Room.objects.get(uuid=uuid)

    if room.status == Room.WAITING:
        room.status = Room.ACTIVE
        room.agent = request.user
        room.save()

    context = {
        'room': room
    }
    return render(request, 'chat/admin/admin_chat_room.html', context)