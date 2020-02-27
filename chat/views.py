# chat/views.py
from django.shortcuts import render
from django.utils.safestring import mark_safe
import json
from django.core.cache import cache
from django.http import HttpResponse

def index(request):
    return render(request, 'chat/index.html', {})

# def room(request, room_name):
#     return render(request, 'chat/room.html', {
#         'room_name_json': mark_safe(json.dumps(room_name))
#     })

def webrtc(request, room_name):
    if cache.has_key(room_name):
        room_data = cache.get(room_name)
        if room_data['numClient'] >=2:
            return HttpResponse(room_name + ' is full!')
    return render(request, 'chat/webrtc.html', {
        'room_name_json': room_name
    })