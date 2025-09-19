from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from dashboard.views import home_view
from django.conf.urls import handler404
from dashboard import views as dashboard_views

handler404 = dashboard_views.custom_page_not_found

urlpatterns = [
    path('', home_view, name='home'),
    path('admin/', admin.site.urls),
    path('chat/', include(('chat.urls', 'chat'), namespace='chat')),

    # All accounts-related URLs (manual + Google login)
    path('accounts/', include(('accounts.urls', 'accounts'), namespace='accounts')),

    # Dashboard app
    path('dashboard/', include(('dashboard.urls', 'dashboard'), namespace='dashboard')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
