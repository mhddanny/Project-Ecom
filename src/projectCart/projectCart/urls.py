from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    # path('admin/', include('admin_honeypot.urls', namespace='admin_honeypot')),
    # path('securelogin/', admin.site.urls),

    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('testchat/', views.chat_bubble , name='testchat'),

    path('store/', include('store.urls')),
    path('cart/', include('carts.urls')),
    path('accounts/', include('accounts.urls')),
    #orders
    path('orders/', include('orders.urls')),
    #chat
    path('', include('chat.urls')),
    #admin
    path('app-admin/', include('appadmin.urls')),

    path('ckeditor/', include('ckeditor_uploader.urls')),

    path("__debug__/", include("debug_toolbar.urls")),
] 

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
