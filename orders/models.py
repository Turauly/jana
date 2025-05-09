from django.db import models
from django.conf import settings  # settings.AUTH_USER_MODEL үшін
from shops.models import Product

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)  # тапсырыс беруші
    customer_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    address = models.TextField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    courier = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='deliveries'
    )


    status = models.CharField(max_length=20, choices=[
        ('new', 'Жаңа'),
        ('processing', 'Қабылданды'),
        ('delivering', 'Жолда'),
        ('delivered', 'Жеткізілді')
    ], default='new')

    def __str__(self):
        return f"{self.customer_name} - {self.product.name}"
