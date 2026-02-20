#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Управление команда для создания тестовых пользователей
Использование: python manage.py create_test_users
"""

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from bodies.models import Profile


class Command(BaseCommand):
    help = 'Создаёт тестовые пользователи с разными ролями для демонстрации'

    def handle(self, *args, **options):
        """Создание тестовых пользователей"""
        
        test_users = [
            {'username': 'admin', 'password': 'admin', 'role': 'admin'},
            {'username': 'editor', 'password': 'editor', 'role': 'editor'},
            {'username': 'user', 'password': 'user', 'role': 'authorized'},
            {'username': 'guest', 'password': 'guest', 'role': 'unauthorized'},
        ]
        
        self.stdout.write("=" * 60)
        self.stdout.write("📝 Создание тестовых пользователей")
        self.stdout.write("=" * 60)
        
        for user_data in test_users:
            username = user_data['username']
            password = user_data['password']
            role = user_data['role']
            
            # Проверяем, существует ли уже пользователь
            if User.objects.filter(username=username).exists():
                user = User.objects.get(username=username)
                self.stdout.write(
                    self.style.WARNING(f"⚠️  Пользователь '{username}' уже существует")
                )
                
                # Используем get_or_create для профиля
                profile, created = Profile.objects.get_or_create(
                    user=user,
                    defaults={'role': role}
                )
                
                # Обновляем роль если она отличается
                if profile.role != role:
                    profile.role = role
                    profile.save()
                    self.stdout.write(
                        self.style.SUCCESS(f"✅ Роль пользователя '{username}' обновлена на '{role}'")
                    )
                elif created:
                    self.stdout.write(
                        self.style.SUCCESS(f"✅ Профиль для '{username}' создан с ролью '{role}'")
                    )
            else:
                # Создаём нового пользователя
                user = User.objects.create_user(
                    username=username,
                    password=password,
                    first_name=username.capitalize()
                )
                
                # Создаём профиль с ролью (используем get_or_create на случай параллельных операций)
                profile, created = Profile.objects.get_or_create(
                    user=user,
                    defaults={'role': role}
                )
                
                self.stdout.write(
                    self.style.SUCCESS(
                        f"✅ Пользователь '{username}' создан\n"
                        f"   Пароль: {password}\n"
                        f"   Роль: {role}"
                    )
                )
        
        self.stdout.write("=" * 60)
        self.stdout.write(self.style.SUCCESS("✅ Все тестовые пользователи созданы!"))
        self.stdout.write("=" * 60)
        self.stdout.write("\n📋 Учетные данные для входа:\n")
        
        for user_data in test_users:
            self.stdout.write(
                f"  👤 {user_data['username']:12} | 🔐 {user_data['password']:12} | 👑 {user_data['role']}"
            )
        
        self.stdout.write("\n")
