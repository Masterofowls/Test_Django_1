#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Установка пароля администратора и создание профиля"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User
from bodies.models import Profile

# Получаем администратора
admin_user = User.objects.get(username='admin')

# Устанавливаем пароль
admin_user.set_password('admin')
admin_user.save()

print("✅ Пароль установлен для пользователя 'admin'")

# Создаём профиль с ролью администратора
profile, created = Profile.objects.get_or_create(
    user=admin_user,
    defaults={'role': 'admin'}
)

if created:
    print("✅ Профиль администратора создан")
else:
    profile.role = 'admin'
    profile.save()
    print("✅ Профиль обновлён на роль 'admin'")

print("\n" + "="*50)
print("🎉 Готово к работе!")
print("="*50)
print("\nДанные для входа:")
print("  📧 Логин: admin")
print("  🔑 Пароль: admin")
print("\nАдрес админ-панели:")
print("  🌐 http://localhost:8000/admin/")
print("\n" + "="*50)
