from django.contrib import admin
from django.urls import path, include
from users.views import role_redirect_view
from . import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),  # 🔵 Басты бет — home.html
    path('admin/', admin.site.urls),
    path('order/', include('orders.urls')),
    path('accounts/', include('users.urls')),
    path('redirect/', role_redirect_view, name='role_redirect'),  # 🔄 Рөлге қарай бағыттау
]

# 📁 Суреттер (media) көрсету үшін қажет
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
