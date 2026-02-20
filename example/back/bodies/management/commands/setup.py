from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from bodies.models import Profile, PickupPoint, Product


class Command(BaseCommand):
    help = 'Инициализация системы с модерном пользователем и тестовыми данными'

    def handle(self, *args, **options):
        # Создание пунктов выдачи по умолчанию
        if not PickupPoint.objects.exists():
            pickup_points = [
                'Москва, ул. Красная площадь, д. 1',
                'СПБ, Невский пр-кт, д. 86',
                'Казань, ул. Баумана, д. 1',
            ]
            for address in pickup_points:
                PickupPoint.objects.create(address=address)
            self.stdout.write(self.style.SUCCESS('✓ Пункты выдачи созданы'))

        # Создание тестовых пользователей для всех ролей
        test_users = [
            {'username': 'admin', 'email': 'admin@shop.local', 'password': 'admin123', 'role': 'admin'},
            {'username': 'editor', 'email': 'editor@shop.local', 'password': 'editor123', 'role': 'editor'},
            {'username': 'authorized', 'email': 'user@shop.local', 'password': 'user123', 'role': 'authorized'},
        ]
        
        for user_data in test_users:
            username = user_data['username']
            
            # Создаем или получаем пользователя
            if user_data['role'] == 'admin':
                user, created = User.objects.get_or_create(
                    username=username,
                    defaults={
                        'email': user_data['email'],
                        'is_staff': True,
                        'is_superuser': True
                    }
                )
                if created:
                    user.set_password(user_data['password'])
                    user.save()
            else:
                user, created = User.objects.get_or_create(
                    username=username,
                    defaults={'email': user_data['email']}
                )
                if created:
                    user.set_password(user_data['password'])
                    user.save()
            
            # Создаем или обновляем профиль с правильной ролью
            profile, profile_created = Profile.objects.get_or_create(user=user)
            
            # Всегда устанавливаем правильную роль
            if profile.role != user_data['role']:
                profile.role = user_data['role']
                profile.save()
            
            self.stdout.write(self.style.SUCCESS(f'✓ {user_data["role"].upper()}: {username} / {user_data["password"]}'))

        # Создание тестовых товаров
        if not Product.objects.exists():
            products_data = [
                {'name': 'Ноутбук Dell', 'sku': 'DELL-001', 'price': 45000, 'description': 'Мощный ноутбук для работы и игр'},
                {'name': 'Смартфон Samsung', 'sku': 'SAM-001', 'price': 25000, 'description': 'Современный смартфон с отличной камерой'},
                {'name': 'Наушники Sony', 'sku': 'SONY-001', 'price': 8000, 'description': 'Беспроводные наушники с шумоподавлением'},
                {'name': 'Монитор LG', 'sku': 'LG-001', 'price': 15000, 'description': '27 дюймов, 4K разрешение'},
                {'name': 'Клавиатура Mechanical', 'sku': 'MECH-001', 'price': 5000, 'description': 'Механическая клавиатура для геймеров'},
            ]
            for product_data in products_data:
                Product.objects.create(**product_data)
            self.stdout.write(self.style.SUCCESS('✓ Тестовые товары созданы'))
        else:
            self.stdout.write('✓ Товары уже существуют')

        self.stdout.write(self.style.SUCCESS('\n✨ Инициализация завершена!'))
        self.stdout.write('Войдите в админ-панель: http://127.0.0.1:8000/admin/')
        self.stdout.write('Логин: admin, Пароль: admin123')
