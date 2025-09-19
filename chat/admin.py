from django.contrib import admin
from .models import Message

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("user", "room", "content", "timestamp")
    list_filter = ("room", "timestamp", "user")
    search_fields = ("content", "user__username")