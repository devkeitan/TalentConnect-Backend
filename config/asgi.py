import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# ✅ This must be called BEFORE importing routing/consumers
from django.core.asgi import get_asgi_application
django_asgi_app = get_asgi_application()

# ✅ Only import these AFTER get_asgi_application()
from channels.routing import ProtocolTypeRouter, URLRouter
from config.middleware import JWTAuthMiddleware
import messaging.routing

application = ProtocolTypeRouter({
    'http': django_asgi_app,
    'websocket': JWTAuthMiddleware(
        URLRouter(
            messaging.routing.websocket_urlpatterns
        )
    ),
})
