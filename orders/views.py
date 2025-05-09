from django.shortcuts import render, redirect, get_object_or_404
from .forms import OrderForm
from .models import Order
from users.models import CustomUser
from shops.models import Product, Shop
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.http import JsonResponse
from django.db.models import Count
from django.core.serializers import serialize

# 🛒 Клиент тапсырыс береді (дүкен таңдалады + өнім JSON-мен)
@login_required
def place_order(request):
    selected_shop_id = request.GET.get('shop')
    shops = Shop.objects.all()
    products_json = "[]"

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.save()
            return render(request, 'orders/success.html')
    else:
        if selected_shop_id:
            form = OrderForm()
            products = Product.objects.filter(shop_id=selected_shop_id)
            form.fields['product'].queryset = products
            products_json = serialize("json", products)
        else:
            form = None

    return render(request, 'orders/place_order.html', {
        'form': form,
        'shops': shops,
        'selected_shop_id': selected_shop_id,
        'products_json': products_json
    })


# 📋 Клиент өз тапсырыстарын көреді
@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'orders/my_orders.html', {'orders': orders})


# 🚚 Курьер панелі
@login_required
def courier_dashboard(request):
    if request.user.role != 'courier':
        return redirect('place_order')

    if request.method == 'POST':
        if 'go_online' in request.POST:
            order = Order.objects.filter(status='new', courier__isnull=True).first()
            if order:
                order.courier = request.user
                order.status = 'delivering'
                order.save()
        elif 'mark_delivered' in request.POST:
            order_id = request.POST.get('order_id')
            order = Order.objects.filter(id=order_id, courier=request.user).first()
            if order:
                order.status = 'delivered'
                order.save()

    my_order = Order.objects.filter(courier=request.user).exclude(status='delivered').first()
    return render(request, 'orders/courier_dashboard.html', {'order': my_order})


# 🛍 Дүкен иесінің тапсырыстары
@login_required
def shop_orders(request):
    if request.user.role != 'shop_owner':
        return redirect('place_order')

    products = Product.objects.filter(shop__owner=request.user)
    orders = Order.objects.filter(product__in=products).order_by('-created_at')
    return render(request, 'orders/shop_orders.html', {'orders': orders})


# 🔊 Курьерге арналған жаңа тапсырысты тексеру API
@login_required
def check_new_orders_courier(request):
    new_order_exists = Order.objects.filter(status='new', courier__isnull=True).exists()
    return JsonResponse({'new_order': new_order_exists})


# 🔊 Дүкен иесіне арналған жаңа тапсырысты тексеру API
@login_required
def check_new_orders_shop(request):
    if request.user.role != 'shop_owner':
        return JsonResponse({'new_order': False})

    products = Product.objects.filter(shop__owner=request.user)
    new_order_exists = Order.objects.filter(product__in=products, status='new').exists()
    return JsonResponse({'new_order': new_order_exists})


# ✏️ Дүкен иесі тапсырыс статусын өңдейді
@login_required
def update_order_status(request, order_id):
    if request.user.role != 'shop_owner':
        return redirect('place_order')

    order = get_object_or_404(Order, id=order_id)
    products = Product.objects.filter(shop__owner=request.user)

    if order.product in products:
        if request.method == 'POST':
            new_status = request.POST.get('status')
            if new_status in ['new', 'processing', 'delivering', 'delivered']:
                order.status = new_status
                order.save()

    return redirect('shop_orders')


# 📊 Админге арналған жалпы статистика
@staff_member_required
def admin_statistics(request):
    total_orders = Order.objects.count()
    delivered_orders = Order.objects.filter(status='delivered').count()

    top_courier = Order.objects.filter(status='delivered', courier__isnull=False) \
        .values('courier__username') \
        .annotate(total=Count('id')) \
        .order_by('-total').first()

    top_shop = Order.objects.values('product__shop__name') \
        .annotate(total=Count('id')) \
        .order_by('-total').first()

    return render(request, 'orders/admin_statistics.html', {
        'total_orders': total_orders,
        'delivered_orders': delivered_orders,
        'top_courier': top_courier,
        'top_shop': top_shop
    })


# 🕒 Соңғы тапсырыстар тізімі
@staff_member_required
def latest_orders(request):
    orders = Order.objects.order_by('-created_at')[:20]
    return render(request, 'orders/latest_orders.html', {'orders': orders})