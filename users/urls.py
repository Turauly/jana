from django.urls import path
from .views import (
    login_view, logout_view, register_view, role_redirect_view,
    send_reset_code, verify_code, set_new_password
)

urlpatterns = [
    # 🔐 Аутентификация
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', register_view, name='register'),
    path('redirect/', role_redirect_view, name='role_redirect'),

    # 🔄 Құпиясөзді қалпына келтіру
    path('send-reset-code/', send_reset_code, name='send_reset_code'),
    path('verify-code/', verify_code, name='verify_code'),
    path('set-new-password/', set_new_password, name='set_new_password'),
]
