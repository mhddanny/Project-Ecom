from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse 
from django.utils.safestring import mark_safe
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST

from accounts.models import Account
from . models import Room
import json

# Create your views here.

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
        'users': users,
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

@login_required
def deleteAdminRoom(request, uuid):
    if request.user.has_perm('room.delete_room'):
        room = Room.objects.get(uuid=uuid)
        room.delete()

        messages.success(request, 'You have delete room succesfully')
        return redirect('/chat-admin/')
    else:
        messages.error(request, 'You don\t have access to delete room!')
        return redirect('/chat-admin/')