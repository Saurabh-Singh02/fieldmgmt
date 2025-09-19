# field_mgmt/asgi.py
import os
import django
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.core.asgi import get_asgi_application
import chat.routing

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "field_mgmt.settings")
django.setup()

# Debug middleware to check authentication
class DebugMiddleware:
    def __init__(self, inner):
        self.inner = inner

    async def __call__(self, scope, receive, send):
        # Print debug info for WebSocket connections
        if scope['type'] == 'websocket':
            user = scope.get('user')
            print(f"WebSocket connection - User: {user}, Authenticated: {getattr(user, 'is_authenticated', False)}")
            
            # Check session
            session = scope.get('session')
            if session:
                print(f"Session key: {session.session_key}")
            else:
                print("No session found in WebSocket scope!")
        
        return await self.inner(scope, receive, send)

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": DebugMiddleware(
        AuthMiddlewareStack(
            URLRouter(
                chat.routing.websocket_urlpatterns
            )
        )
    ),
})