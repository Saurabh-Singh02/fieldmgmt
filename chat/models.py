# chat/models.py
from django.db import models
from django.conf import settings   # ✅ to support custom user models

class Message(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,   # ✅ always use this, never auth.User
        on_delete=models.CASCADE,
        related_name="messages"
    )
    room = models.CharField(max_length=255)   # ✅ which chatroom this message belongs to
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['timestamp']   # ✅ oldest → newest

    def __str__(self):
        return f"[{self.room}] {self.user}: {self.content[:20]}"
