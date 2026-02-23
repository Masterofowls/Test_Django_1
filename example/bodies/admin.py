from django.contrib import admin
from .models import Product, PickupPoint, Order, Profile


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'sku', 'price', 'has_image')
    search_fields = ('name', 'sku')
    list_filter = ('price',)
    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'sku', 'price')
        }),
        ('Описание и изображение', {
            'fields': ('description', 'image')
        }),
    )
    
    def has_image(self, obj):
        """Показать галочку если есть изображение"""
        return bool(obj.image)
    has_image.boolean = True
    has_image.short_description = '📸 Есть изображение'


@admin.register(PickupPoint)
class PickupPointAdmin(admin.ModelAdmin):
    list_display = ('address',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'status', 'createdAt', 'receiveCode')
    list_filter = ('status', 'createdAt')
    search_fields = ('user__username', 'receiveCode')
    readonly_fields = ('createdAt', 'receiveCode')


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role')
    list_filter = ('role',)
