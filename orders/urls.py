from django.urls import path
from .views import (
    place_order, my_orders, courier_dashboard, shop_orders,
    check_new_orders_courier, check_new_orders_shop,
    update_order_status, admin_statistics, latest_orders  # ✅ МІНЕ МЫНА ЖОЛ ҚОСЫЛДЫ
)

urlpatterns = [
    path('', place_order, name='place_order'),
    path('my-orders/', my_orders, name='my_orders'),
    path('courier/', courier_dashboard, name='courier_dashboard'),
    path('shop-orders/', shop_orders, name='shop_orders'),
    path('check-new-orders-courier/', check_new_orders_courier, name='check_new_orders_courier'),
    path('check-new-orders-shop/', check_new_orders_shop, name='check_new_orders_shop'),
    path('update-status/<int:order_id>/', update_order_status, name='update_order_status'),
    path('latest-orders/', latest_orders, name='latest_orders'),
    path('admin-statistics/', admin_statistics, name='admin_statistics'),
]
