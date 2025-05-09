from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import CustomUserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import CustomUser, ResetCode
from django.core.mail import send_mail
from django.utils import timezone
from datetime import timedelta
import random

# 🔁 Рөлге байланысты бағыттау
@login_required
def role_redirect_view(request):
    if request.user.role == 'client':
        return redirect('place_order')
    elif request.user.role == 'courier':
        return redirect('courier_dashboard')
    elif request.user.role == 'shop_owner':
        return redirect('shop_orders')
    return redirect('admin:index')


# 📝 Тіркелу
def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('role_redirect')
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form})


# 🔐 Кіру
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('role_redirect')
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {'form': form})


# 🔓 Шығу
def logout_view(request):
    logout(request)
    return redirect('login')


# 🔐 1-қадам: Құпиясөзді қалпына келтіру — код жіберу
def send_reset_code(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = CustomUser.objects.get(email=email)

            # Ескі кодтарды өшіру
            ResetCode.objects.filter(user=user).delete()

            # Жаңа код жасау
            code = str(random.randint(100000, 999999))
            ResetCode.objects.create(user=user, code=code, created_at=timezone.now())

            # Email жіберу
            send_mail(
                'Құпиясөзді қалпына келтіру',
                f'Сіздің растау кодыңыз: {code}',
                'noreply@example.com',
                [email],
                fail_silently=False,
            )
            return render(request, 'users/verify_code.html', {'email': email})
        except CustomUser.DoesNotExist:
            return render(request, 'users/send_code.html', {'error': 'Бұл email табылмады'})
    return render(request, 'users/send_code.html')


# 🔐 2-қадам: Кодты тексеру
def verify_code(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        code = request.POST.get('code')
        try:
            user = CustomUser.objects.get(email=email)

            valid = ResetCode.objects.filter(
                user=user,
                code=code,
                created_at__gte=timezone.now() - timedelta(minutes=10)
            ).exists()

            if valid:
                # Код жарамды, келесі қадамға өтеміз
                return render(request, 'users/set_new_password.html', {'email': email})
            else:
                return render(request, 'users/verify_code.html', {
                    'email': email,
                    'error': 'Код дұрыс емес немесе мерзімі өтіп кеткен'
                })
        except CustomUser.DoesNotExist:
            return redirect('send_reset_code')
    return redirect('send_reset_code')


# 🔐 3-қадам: Жаңа құпиясөз орнату
def set_new_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user = CustomUser.objects.get(email=email)
            user.set_password(password)
            user.save()

            # Кодтарды жоямыз
            ResetCode.objects.filter(user=user).delete()

            return redirect('login')
        except CustomUser.DoesNotExist:
            return redirect('send_reset_code')
    return redirect('send_reset_code')
