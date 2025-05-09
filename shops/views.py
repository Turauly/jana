from django.shortcuts import render, redirect
from .models import Product, Shop
from .forms import ProductForm
from django.contrib.auth.decorators import login_required

@login_required
def add_product(request):
    if request.user.role != 'shop_owner':
        return redirect('home')

    shop = Shop.objects.get(owner=request.user)

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.shop = shop
            product.save()
            return redirect('shop_orders')
    else:
        form = ProductForm()

    return render(request, 'shops/add_product.html', {'form': form})
