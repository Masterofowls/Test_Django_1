import random
import string
from django.db import models
from django.contrib.auth.models import User


def generate_receive_code():
    """Генерирует 6-значный код для получения заказа"""
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))


class Product(models.Model):
    """Модель товара в магазине"""
    name        = models.CharField(max_length=255, verbose_name="Название товара")
    price       = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена (руб.)")
    description = models.TextField(blank=True, verbose_name="Описание товара")
    sku         = models.CharField(max_length=50, unique=True, verbose_name="Артикул")
    image       = models.ImageField(upload_to='products/', blank=True, null=True, verbose_name="Изображение товара")

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
        ordering = ['-id']

    def __str__(self):
        return f"{self.name} ({self.sku})"


class PickupPoint(models.Model):
    """Пункт выдачи заказов"""
    address = models.CharField(max_length=500, verbose_name="Адрес пункта выдачи")

    class Meta:
        verbose_name = "Пункт выдачи"
        verbose_name_plural = "Пункты выдачи"

    def __str__(self):
        return self.address


class Order(models.Model):
    """Заказ пользователя"""
    STATUS_CHOICES = [
        ('new', 'Новый'),
        ('delivered', 'Завершен'),
    ]
    
    user         = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders", verbose_name="Пользователь")
    products     = models.ManyToManyField(Product, verbose_name="Товары в заказе")
    createdAt    = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания заказа")
    deliveryDate = models.DateTimeField(null=True, blank=True, verbose_name="Дата доставки")
    receiveCode  = models.CharField(max_length=10, default=generate_receive_code, verbose_name="Код для получения")
    pickupPoint  = models.ForeignKey(PickupPoint, on_delete=models.SET_NULL, null=True, verbose_name="Пункт выдачи")
    status       = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new', verbose_name="Статус заказа")

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
        ordering = ['-createdAt']

    def __str__(self):
        user_name = self.user.get_full_name() or self.user.username
        return f"Заказ #{self.id} - {user_name}"
    
    def get_skus(self):
        """Получить артикулы всех товаров в заказе"""
        return ', '.join([p.sku for p in self.products.all()])


class Profile(models.Model):
    """Профиль пользователя с ролью"""
    ROLE_CHOICES = [
        ('unauthorized', 'Неавторизированный'),
        ('authorized', 'Авторизированный'),
        ('editor', 'Редактор'),
        ('admin', 'Администратор'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='authorized', verbose_name="Роль")

    class Meta:
        verbose_name = "Профиль"
        verbose_name_plural = "Профили"

    def __str__(self):
        return f"{self.user.username} ({self.get_role_display()})"
    
    def is_admin(self):
        return self.role == 'admin'
    
    def is_editor(self):
        return self.role in ['editor', 'admin']
    
    def is_authorized(self):
        return self.role in ['authorized', 'editor', 'admin']
