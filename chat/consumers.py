# chat/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from .models import Message

User = get_user_model()

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"
        
        # Check if user is authenticated
        if self.scope["user"].is_anonymous:
            await self.close()
        else:
            # Join room group
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )
            await self.accept()
            
            # Send chat history to the newly connected user
            await self.send_chat_history()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
            message = data["message"].strip()
            
            if not message:
                return
                
            user = self.scope["user"]
            
            # Save message to database
            saved_message = await self.save_message(user, message)
            
            # Broadcast to everyone in the room
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "chat_message",
                    "message": message,
                    "username": user.username,
                    "timestamp": saved_message.timestamp.isoformat()
                }
            )
        except json.JSONDecodeError:
            # Handle invalid JSON
            pass
        except KeyError:
            # Handle missing message key
            pass

    async def chat_message(self, event):
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            "message": event["message"],
            "username": event["username"],
            "timestamp": event["timestamp"]
        }))

    @database_sync_to_async
    def save_message(self, user, message):
        return Message.objects.create(
            user=user,
            room=self.room_name,
            content=message
        )
    
    @database_sync_to_async
    def get_chat_history(self):
        return list(Message.objects.filter(room=self.room_name)
                          .select_related('user')
                          .order_by('timestamp')[:50])
    
    async def send_chat_history(self):
        messages = await self.get_chat_history()
        for message in messages:
            await self.send(text_data=json.dumps({
                "message": message.content,
                "username": message.user.username,
                "timestamp": message.timestamp.isoformat(),
                "history": True  # Flag to identify historical messages
            }))