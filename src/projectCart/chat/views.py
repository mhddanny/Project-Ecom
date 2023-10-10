from django.contrib.auth.decorators import login_required
from django.utils.safestring import mark_safe
from django.shortcuts import render
from accounts.models import Account

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