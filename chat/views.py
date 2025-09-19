from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Message

@login_required
def room(request, room_name):
    messages = Message.objects.filter(room=room_name)
    return render(request, "chat/room.html", {
        "room_name": room_name,
        "messages": messages
    })
