import random
import string
from django.db import models
from django.contrib.auth.models import User
# Create your models here.

def generate_receive_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название товара")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    description = models.TextField(blank=True, verbose_name="Описание товара")
    sku = models.CharField(max_length=50, unique=True, verbose_name="Артикул")


    def __str__(self):
        return f"{self.name} ({self.sku})"

class PickupPoint(models.Model):
    address = models.CharField(max_length=500, verbose_name="Адрес пункта выдачи")
    def __str__(self):
        return self.address



class Order(models.Model):
    STATUS_CHOICES = [
        ("new", "Новый"),
        ("delivered", "Завершен"),
    ]
    # Номер заказа	Артикул заказа	Дата заказа	Дата доставки	Адрес пункта выдачи	ФИО авторизированного клиента	Код для получения	Статус заказа

    user =  models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    products =  models.ManyToManyField(Product, verbose_name="Товары")  
    createdAt = models.DateTimeField(auto_now_add=True, verbose_name="Дата заказа")
    deliveryDate = models.DateTimeField(null=True, blank=True, verbose_name="Дата доставки")
    receiveCode = models.CharField(max_length=10, default=generate_receive_code(), verbose_name="Код получения")
    pickupPoint = models.ForeignKey(PickupPoint, on_delete=models.SET_NULL, null=True, verbose_name="Пункт выдачи")
    status =  models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')

    def __str__(self):
        return f"Заказ №{self.id} - {self.user.get_full_name() or self.user.username}"
    
    def get_skus(self):
        return ', '.join([p.sku for p in self.products.all()])
    
class Profile(models.Model):
    ROLE_CHOICES = [
        ('admin', 'админ'),
        ('manager', 'менеджер'),
        ('customer', 'покупатель'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='customer' )