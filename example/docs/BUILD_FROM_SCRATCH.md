# 🏗️ Сборка проекта с нуля — Полное руководство

Полная пошаговая инструкция по созданию Django интернет-магазина с нуля: от установки Python и PostgreSQL до полностью рабочего приложения с четырёхуровневой системой ролей, каталогом товаров, заказами и админ-панелью.

---

## 📋 Содержание

1. [Предварительные требования](#1-предварительные-требования)
2. [Установка инструментов](#2-установка-инструментов)
3. [Создание виртуального окружения](#3-создание-виртуального-окружения)
4. [Инициализация Django-проекта](#4-инициализация-django-проекта)
5. [Создание приложения bodies](#5-создание-приложения-bodies)
6. [Настройка config/settings.py](#6-настройка-configsettingspy)
7. [Создание моделей (bodies/models.py)](#7-создание-моделей-bodiesmodelspy)
8. [Создание форм (bodies/forms.py)](#8-создание-форм-bodiesformspy)
9. [Создание представлений (bodies/views.py)](#9-создание-представлений-bodiesviewspy)
10. [Настройка URL-маршрутов](#10-настройка-url-маршрутов)
11. [Регистрация в админ-панели (bodies/admin.py)](#11-регистрация-в-админ-панели-bodiesadminpy)
12. [Сигналы Django (bodies/signals.py)](#12-сигналы-django-bodiessignalspy)
13. [Конфигурация приложения (bodies/apps.py)](#13-конфигурация-приложения-bodiesappspy)
14. [Создание HTML-шаблонов](#14-создание-html-шаблонов)
15. [Создание management-команд](#15-создание-management-команд)
16. [Создание базы данных PostgreSQL](#16-создание-базы-данных-postgresql)
17. [Миграции и запуск](#17-миграции-и-запуск)
18. [Проверка работоспособности](#18-проверка-работоспособности)

---

## 1. Предварительные требования

Перед началом работы убедитесь, что у вас установлены:

| Инструмент | Версия | Назначение |
|------------|--------|------------|
| **Python** | 3.12+ | Язык программирования |
| **PostgreSQL** | 12+ | База данных |
| **pip** | Последняя | Менеджер пакетов Python |

---

## 2. Установка инструментов

### Windows

1. **Python** — скачайте с [python.org](https://www.python.org/downloads/). При установке поставьте галочку **"Add Python to PATH"**.
2. **PostgreSQL** — скачайте с [postgresql.org](https://www.postgresql.org/download/windows/). Запомните пароль пользователя `postgres`.

### Проверка установки

```bash
python --version
# Python 3.12.x

psql --version
# psql (PostgreSQL) 16.x
```

---

## 3. Создание виртуального окружения

Откройте терминал (PowerShell на Windows или Terminal на macOS/Linux).

```bash
# Создать корневую папку проекта
mkdir example
cd example

# Создать виртуальное окружение
python -m venv venv

# Активировать виртуальное окружение
# Windows (PowerShell):
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

После активации вы увидите `(venv)` перед строкой терминала.

### Установить зависимости

Создайте файл **`requirements.txt`** в корне папки `example/`:

```
Django==6.0.1
psycopg==3.1.18
openpyxl==3.1.5
```

Установите зависимости:

```bash
pip install -r requirements.txt
```

| Пакет | Назначение |
|-------|-----------|
| `Django==6.0.1` | Веб-фреймворк |
| `psycopg==3.1.18` | Драйвер PostgreSQL для Python |
| `openpyxl==3.1.5` | Работа с Excel-файлами |

---

## 4. Инициализация Django-проекта

Находясь внутри папки `example/`, выполните:

```bash
django-admin startproject config .
```

> **Важно:** Точка (`.`) в конце означает, что проект создаётся в текущей папке, а не в подпапке.

После выполнения этой команды появятся:

```
example/
├── manage.py        # CLI-утилита Django
└── config/          # Пакет конфигурации
    ├── __init__.py  # Пустой файл — указывает, что это пакет Python
    ├── settings.py  # Настройки проекта
    ├── urls.py      # Главные URL-маршруты
    ├── asgi.py      # ASGI точка входа
    └── wsgi.py      # WSGI точка входа
```

### Что делает каждый файл

- **`manage.py`** — Точка входа для всех команд Django (`runserver`, `migrate`, `createsuperuser` и др.)
- **`config/__init__.py`** — Пустой файл, помечающий `config/` как Python-пакет
- **`config/settings.py`** — Все настройки приложения (база данных, приложения, шаблоны и т.д.)
- **`config/urls.py`** — Маршрутизация URL-адресов к представлениям
- **`config/wsgi.py`** — Точка входа для WSGI-серверов (Gunicorn, uWSGI)
- **`config/asgi.py`** — Точка входа для ASGI-серверов (Daphne, Uvicorn)

---

## 5. Создание приложения bodies

Django-проект состоит из приложений. Создайте основное приложение `bodies`:

```bash
python manage.py startapp bodies
```

Появится папка `bodies/`:

```
bodies/
├── __init__.py
├── admin.py        # Регистрация моделей в админ-панели
├── apps.py         # Конфигурация приложения
├── migrations/     # Миграции базы данных
│   └── __init__.py
├── models.py       # Модели базы данных
├── tests.py        # Тесты
└── views.py        # Представления (контроллеры)
```

### Дополнительно создайте:

```bash
# Папка для HTML-шаблонов
mkdir bodies/templates

# Папка для management-команд
mkdir -p bodies/management/commands

# Пустые __init__.py файлы для пакетов Python
# (bodies/management/__init__.py уже должен быть создан mkdir -p, но на всякий случай)
touch bodies/management/__init__.py
touch bodies/management/commands/__init__.py
```

> **Windows:** Вместо `touch` создайте пустые файлы вручную (правой кнопкой → Создать → Текстовый документ, переименовать в `__init__.py`), или используйте:
> ```powershell
> echo. > bodies\management\__init__.py
> echo. > bodies\management\commands\__init__.py
> ```

Также создайте файлы, которые Django не создаёт автоматически:

- **`bodies/forms.py`** — Пользовательские формы
- **`bodies/signals.py`** — Обработчики сигналов Django
- **`bodies/urls.py`** — URL-маршруты приложения

---

## 6. Настройка config/settings.py

Откройте `config/settings.py` и замените его содержимое на:

```python
"""
Django settings for back project.

Generated by 'django-admin startproject' using Django 6.0.1.

For more information on this file, see
https://docs.djangoproject.com/en/6.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/6.0/ref/settings/
"""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/6.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-%p0t$hgp_wnb#nbu*-*odc$+t48i0!)9)pz3z*&vdmmqb$&*1k'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    'bodies',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/6.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'shop',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}


# Password validation
# https://docs.djangoproject.com/en/6.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/6.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/6.0/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/6.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
```

### Что мы настроили

| Настройка | Значение | Описание |
|-----------|----------|----------|
| `INSTALLED_APPS` | `+ 'bodies'` | Зарегистрировали наше приложение |
| `DATABASES` | PostgreSQL | База данных `shop`, пользователь `postgres` |
| `ROOT_URLCONF` | `'config.urls'` | Главный файл маршрутов |
| `APP_DIRS` | `True` | Django ищет шаблоны в `templates/` внутри приложений |
| `DEBUG` | `True` | Режим разработки (показывает ошибки) |

> **⚠️ Для продакшена:** замените `SECRET_KEY` на уникальное значение, установите `DEBUG = False`, настройте `ALLOWED_HOSTS`.

---

## 7. Создание моделей (bodies/models.py)

Модели определяют структуру таблиц в базе данных. Откройте `bodies/models.py` и запишите:

```python
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
```

### Описание моделей

| Модель | Назначение | Ключевые поля |
|--------|-----------|---------------|
| **Product** | Товар в каталоге | `name`, `price`, `description`, `sku` (уникальный) |
| **PickupPoint** | Пункт выдачи заказов | `address` |
| **Order** | Заказ пользователя | `user` (FK→User), `products` (M2M→Product), `status`, `receiveCode` |
| **Profile** | Профиль с ролью | `user` (1-к-1→User), `role` (4 уровня) |

### Связи между моделями

```
User ←→ Profile     (1:1 — у каждого пользователя один профиль)
User → Order         (1:N — пользователь может иметь много заказов)
Order ↔ Product      (M:N — заказ содержит много товаров, товар в нескольких заказах)
Order → PickupPoint  (N:1 — много заказов на один пункт выдачи)
```

### Система ролей (4 уровня)

| Роль | Права |
|------|-------|
| `unauthorized` | Просмотр каталога без фильтров |
| `authorized` | + Фильтрация товаров, создание заказов |
| `editor` | + Редактирование товаров |
| `admin` | + Добавление/удаление товаров, управление пользователями |

---

## 8. Создание форм (bodies/forms.py)

Создайте файл `bodies/forms.py`:

```python
# -*- coding: utf-8 -*-
"""
Пользовательские формы для приложения bodies
"""

from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class SimplifiedUserCreationForm(forms.ModelForm):
    """
    Упрощённая форма регистрации с более мягкими требованиями к паролю
    """
    password1 = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Введите пароль'}),
        min_length=4,
        help_text="Минимум 4 символа"
    )
    password2 = forms.CharField(
        label="Подтверждение пароля",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Подтвердите пароль'}),
        min_length=4,
        help_text="Введите пароль ещё раз"
    )
    
    username = forms.CharField(
        label="Имя пользователя",
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Выберите имя пользователя'}),
        help_text="Только буквы, цифры и @/./+/-/_"
    )
    
    class Meta:
        model = User
        fields = ('username',)
    
    def clean_username(self):
        """Проверка уникальности имени пользователя"""
        username = self.cleaned_data.get('username')
        
        if not username:
            raise ValidationError("Имя пользователя не может быть пустым")
        
        if User.objects.filter(username=username).exists():
            raise ValidationError(f"Пользователь с именем '{username}' уже существует")
        
        return username
    
    def clean(self):
        """Проверка паролей и совпадение"""
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        
        if password1 and password2:
            if password1 != password2:
                raise ValidationError("Пароли не совпадают!")
        
        return cleaned_data
    
    def save(self, commit=True):
        """Сохранение пользователя с паролем"""
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user
```

### Зачем нужна эта форма

Стандартная форма Django (`UserCreationForm`) требует пароль минимум 8 символов, с цифрами и буквами. Наша форма позволяет создавать тестовых пользователей с простыми паролями (например, `admin`/`admin`).

---

## 9. Создание представлений (bodies/views.py)

Представления (views) обрабатывают HTTP-запросы и возвращают ответы. Откройте `bodies/views.py` и замените содержимое:

```python
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.views.decorators.http import require_http_methods
from .models import Product, PickupPoint, Order, Profile
from .forms import SimplifiedUserCreationForm


def get_user_role(user):
    """Получить роль пользователя"""
    if not user.is_authenticated:
        return 'unauthorized'
    try:
        return user.profile.role
    except Profile.DoesNotExist:
        # Если профиль не существует, создаем его
        profile = Profile.objects.create(user=user, role='authorized')
        return profile.role


def require_role(allowed_roles):
    """Декоратор для проверки роли пользователя"""
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            user_role = get_user_role(request.user)
            if user_role not in allowed_roles:
                return HttpResponseForbidden("У вас нет прав доступа к этой странице")
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator


def product_list(request):
    """Показать список товаров в зависимости от роли пользователя"""
    user_role = get_user_role(request.user)
    
    # Неавторизированный пользователь видит все товары без фильтрации
    products = Product.objects.all()
    
    # Авторизированный/Редактор/Админ могут видеть с фильтрацией
    if user_role in ['authorized', 'editor', 'admin']:
        search = request.GET.get('search', '')
        price_min = request.GET.get('price_min', '')
        price_max = request.GET.get('price_max', '')
        
        if search:
            products = products.filter(name__icontains=search) | products.filter(description__icontains=search)
        if price_min:
            try:
                products = products.filter(price__gte=float(price_min))
            except ValueError:
                pass
        if price_max:
            try:
                products = products.filter(price__lte=float(price_max))
            except ValueError:
                pass
    
    context = {
        'products': products,
        'user_role': user_role,
        'show_edit': user_role in ['editor', 'admin'],
        'show_delete': user_role == 'admin',
        'show_add_product': user_role == 'admin',
    }
    return render(request, 'products.html', context)


def register_view(request):
    """Регистрация нового пользователя"""
    if request.method == 'POST':
        form = SimplifiedUserCreationForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                # Создаем профиль с ролью авторизированного пользователя
                # Проверяем, не существует ли уже профиль
                profile, created = Profile.objects.get_or_create(
                    user=user,
                    defaults={'role': 'authorized'}
                )
                if created:
                    print(f"✅ Профиль создан для пользователя {user.username}")
                else:
                    print(f"✅ Профиль уже существует для пользователя {user.username}")
                
                login(request, user)
                print(f"✅ Пользователь {user.username} успешно зарегистрирован и вошел в систему")
                return redirect('product_list')
            except Exception as e:
                print(f"❌ Ошибка при создании профиля: {e}")
                form.add_error(None, f"Ошибка при создании профиля: {str(e)}")
        else:
            print(f"❌ Ошибки валидации формы: {form.errors}")
    else:
        form = SimplifiedUserCreationForm()
    
    return render(request, 'register.html', {'form': form})


def login_view(request):
    """Вход в систему"""
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
        
        print(f"🔐 Попытка входа: пользователь '{username}'")
        
        if not username or not password:
            error = 'Введите имя пользователя и пароль'
            print(f"❌ {error}")
            return render(request, 'login.html', {'error': error})
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            print(f"✅ Пользователь {username} успешно вошел в систему")
            return redirect('product_list')
        else:
            error = 'Неверный логин или пароль'
            print(f"❌ {error} для пользователя '{username}'")
            return render(request, 'login.html', {'error': error})
    return render(request, 'login.html')


def logout_view(request):
    """Выход из системы"""
    logout(request)
    return redirect('product_list')


@login_required(login_url='login')
@require_role(['authorized', 'editor', 'admin'])
def order_list(request):
    """Показать заказы пользователя"""
    orders = Order.objects.filter(user=request.user)
    return render(request, 'order_list.html', {'orders': orders})


@login_required(login_url='login')
@require_role(['authorized', 'editor', 'admin'])
def create_order(request, product_id, pickup_point_id):
    """Создать новый заказ"""
    product      = get_object_or_404(Product, id=product_id)
    pickup_point = get_object_or_404(PickupPoint, id=pickup_point_id)
    
    order = Order.objects.create(user=request.user, pickupPoint=pickup_point)
    order.products.add(product)
    
    return redirect('order_list')


@login_required(login_url='login')
@require_role(['editor', 'admin'])
def edit_product(request, product_id):
    """Редактировать товар"""
    product = get_object_or_404(Product, id=product_id)
    
    if request.method == 'POST':
        product.name = request.POST.get('name', product.name)
        product.price = request.POST.get('price', product.price)
        product.description = request.POST.get('description', product.description)
        product.sku = request.POST.get('sku', product.sku)
        product.save()
        return redirect('product_list')
    
    return render(request, 'edit_product.html', {'product': product})


@login_required(login_url='login')
@require_role(['admin'])
def delete_product(request, product_id):
    """Удалить товар"""
    product = get_object_or_404(Product, id=product_id)
    
    if request.method == 'POST':
        product.delete()
        return redirect('product_list')
    
    return render(request, 'confirm_delete.html', {'object': product, 'object_type': 'товара'})


@login_required(login_url='login')
@require_role(['admin'])
def add_product(request):
    """Добавить новый товар"""
    if request.method == 'POST':
        product = Product.objects.create(
            name=request.POST.get('name', ''),
            price=request.POST.get('price', 0),
            description=request.POST.get('description', ''),
            sku=request.POST.get('sku', '')
        )
        return redirect('product_list')
    
    return render(request, 'add_product.html')


@login_required(login_url='login')
@require_role(['admin'])
def manage_users(request):
    """Управление пользователями (показ списка)"""
    from django.contrib.auth.models import User
    users = User.objects.all()
    return render(request, 'manage_users.html', {'users': users})


@login_required(login_url='login')
@require_role(['admin'])
def edit_user_role(request, user_id):
    """Изменить роль пользователя"""
    from django.contrib.auth.models import User
    user = get_object_or_404(User, id=user_id)
    profile = user.profile
    
    if request.method == 'POST':
        new_role = request.POST.get('role')
        profile.role = new_role
        profile.save()
        return redirect('manage_users')
    
    return render(request, 'edit_user_role.html', {'user': user, 'profile': profile})


@login_required(login_url='login')
@require_role(['admin'])
def delete_user(request, user_id):
    """Удалить пользователя"""
    from django.contrib.auth.models import User
    user = get_object_or_404(User, id=user_id)
    
    if request.user.id == user_id:
        return HttpResponseForbidden("Вы не можете удалить свой аккаунт")
    
    if request.method == 'POST':
        user.delete()
        return redirect('manage_users')
    
    return render(request, 'confirm_delete.html', {'object': user, 'object_type': 'пользователя'})
```

### Обзор представлений

| Представление | URL | Доступ | Описание |
|-------------|-----|--------|----------|
| `product_list` | `/` | Все | Каталог товаров (фильтрация — только для авторизированных) |
| `register_view` | `/register/` | Все | Регистрация нового пользователя |
| `login_view` | `/login/` | Все | Вход в систему |
| `logout_view` | `/logout/` | Все | Выход из системы |
| `order_list` | `/orders/` | authorized+ | Список заказов текущего пользователя |
| `create_order` | `/buy/<id>/<point>/` | authorized+ | Создание заказа |
| `edit_product` | `/product/<id>/edit/` | editor+ | Редактирование товара |
| `add_product` | `/product/add/` | admin | Добавление нового товара |
| `delete_product` | `/product/<id>/delete/` | admin | Удаление товара |
| `manage_users` | `/users/` | admin | Список всех пользователей |
| `edit_user_role` | `/user/<id>/edit-role/` | admin | Изменение роли пользователя |
| `delete_user` | `/user/<id>/delete/` | admin | Удаление пользователя |

### Вспомогательные функции

- **`get_user_role(user)`** — Возвращает роль пользователя (`'unauthorized'` для неавторизированных)
- **`require_role(roles)`** — Декоратор, проверяющий, что роль пользователя входит в список допустимых

---

## 10. Настройка URL-маршрутов

### 10.1. Главные маршруты — config/urls.py

Откройте `config/urls.py` и замените содержимое:

```python
"""
URL configuration for back project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('bodies.urls')),
]
```

### 10.2. Маршруты приложения — bodies/urls.py

Создайте файл `bodies/urls.py`:

```python
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('',                          views.product_list,  name='product_list'),
    path('register/',                 views.register_view, name='register'),
    path('login/',                    views.login_view,    name='login'),
    path('logout/',                   views.logout_view,   name='logout'),
    path('orders/',                   views.order_list,    name='order_list'),
    path('buy/<int:product_id>/<int:pickup_point_id>/',
         views.create_order, name='create_order'),
    
    # Редактор и админ - редактирование товаров
    path('product/<int:product_id>/edit/', views.edit_product, name='edit_product'),
    path('product/add/', views.add_product, name='add_product'),
    
    # Только админ - удаление товаров и управление пользователями
    path('product/<int:product_id>/delete/', views.delete_product, name='delete_product'),
    path('users/', views.manage_users, name='manage_users'),
    path('user/<int:user_id>/edit-role/', views.edit_user_role, name='edit_user_role'),
    path('user/<int:user_id>/delete/', views.delete_user, name='delete_user'),
]
```

### Как работает маршрутизация

1. Запрос приходит на сервер (например, `http://127.0.0.1:8000/orders/`)
2. Django проверяет `config/urls.py` — находит `path('', include('bodies.urls'))`
3. Далее проверяет `bodies/urls.py` — находит `path('orders/', views.order_list, name='order_list')`
4. Вызывает функцию `order_list()` из `bodies/views.py`

---

## 11. Регистрация в админ-панели (bodies/admin.py)

Откройте `bodies/admin.py` и замените содержимое:

```python
from django.contrib import admin
from .models import Product, PickupPoint, Order, Profile


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'sku', 'price')
    search_fields = ('name', 'sku')
    list_filter = ('price',)


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
```

### Что настроено

| Модель | list_display | Поиск | Фильтры |
|--------|-------------|-------|---------|
| **Product** | Название, Артикул, Цена | По названию и артикулу | По цене |
| **PickupPoint** | Адрес | — | — |
| **Order** | №, Пользователь, Статус, Дата, Код | По пользователю и коду | По статусу и дате |
| **Profile** | Пользователь, Роль | — | По роли |

---

## 12. Сигналы Django (bodies/signals.py)

Сигналы позволяют автоматически выполнять действия при событиях в Django. Создайте файл `bodies/signals.py`:

```python
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Автоматически создавать профиль при создании пользователя"""
    if created:
        Profile.objects.get_or_create(user=instance, defaults={'role': 'authorized'})


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Сохранять профиль при сохранении пользователя"""
    if hasattr(instance, 'profile'):
        instance.profile.save()
```

### Как это работает

Когда новый `User` создаётся (через форму регистрации, admin, или `createsuperuser`), сигнал `post_save` автоматически:

1. Создаёт объект `Profile` с ролью `'authorized'`
2. Связывает его с созданным пользователем

> **Зачем:** Чтобы не нужно было вручную создавать профиль каждый раз при создании пользователя.

---

## 13. Конфигурация приложения (bodies/apps.py)

Откройте `bodies/apps.py` и замените содержимое:

```python
from django.apps import AppConfig


class BodiesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'bodies'
    
    def ready(self):
        import bodies.signals
```

### Зачем метод `ready()`

Метод `ready()` вызывается при старте Django. Строка `import bodies.signals` подключает наши обработчики сигналов, иначе они не будут работать.

---

## 14. Создание HTML-шаблонов

Все шаблоны создаются в папке `bodies/templates/`. Django автоматически найдёт их, потому что `APP_DIRS = True` в settings.py.

### 14.1. products.html — Каталог товаров (главная страница)

Создайте файл `bodies/templates/products.html`:

```html
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Каталог товаров</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: Arial, sans-serif; background: #f5f5f5; padding: 20px; }
        .container { max-width: 1200px; margin: 0 auto; }
        
        header { background: white; padding: 20px; border-radius: 5px; margin-bottom: 20px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }
        h1 { color: #333; margin-bottom: 10px; }
        
        nav { display: flex; gap: 15px; align-items: center; flex-wrap: wrap; }
        nav a, nav span { text-decoration: none; color: #007bff; font-weight: bold; }
        nav a:hover { text-decoration: underline; }
        nav span { color: #666; }
        
        .admin-controls { margin-top: 15px; display: flex; gap: 10px; }
        .btn-admin { background: #dc3545; color: white; padding: 10px 15px; border-radius: 5px; text-decoration: none; font-weight: bold; }
        .btn-admin:hover { background: #c82333; }
        .btn-users { background: #28a745; color: white; }
        .btn-users:hover { background: #218838; }
        
        .filter-section { background: white; padding: 20px; border-radius: 5px; margin-bottom: 20px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }
        .filter-section h3 { margin-bottom: 15px; color: #333; }
        .filter-form { display: flex; gap: 10px; flex-wrap: wrap; align-items: flex-end; }
        .filter-form input { padding: 8px; border: 1px solid #ddd; border-radius: 3px; }
        .filter-form button { padding: 8px 15px; background: #007bff; color: white; border: none; border-radius: 3px; cursor: pointer; font-weight: bold; }
        .filter-form button:hover { background: #0056b3; }
        .filter-form .btn-clear { background: #6c757d; }
        .filter-form .btn-clear:hover { background: #5a6268; }
        
        .products { display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 20px; }
        .product { background: white; padding: 15px; border-radius: 5px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); position: relative; }
        .product h3 { margin-bottom: 10px; color: #333; font-size: 18px; }
        .product p { color: #666; font-size: 14px; margin: 5px 0; }
        .price { font-size: 20px; font-weight: bold; color: #28a745; margin: 10px 0; }
        
        .btn { display: inline-block; background: #007bff; color: white; padding: 8px 12px; border-radius: 3px; text-decoration: none; margin-top: 10px; cursor: pointer; border: none; font-size: 14px; }
        .btn:hover { background: #0056b3; }
        
        .product-actions { display: flex; gap: 8px; margin-top: 10px; flex-wrap: wrap; }
        .btn-edit { background: #28a745; }
        .btn-edit:hover { background: #218838; }
        .btn-delete { background: #dc3545; }
        .btn-delete:hover { background: #c82333; }
        
        .role-badge { display: inline-block; background: #667eea; color: white; padding: 5px 10px; border-radius: 20px; font-size: 12px; font-weight: bold; }
        
        .empty { text-align: center; padding: 40px; background: white; border-radius: 5px; color: #999; }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🛍️ Интернет-магазин</h1>
            <nav>
                {% if user.is_authenticated %}
                    <span>👤 {{ user.username }}</span>
                    <span class="role-badge">{{ user.profile.get_role_display }}</span>
                    <a href="{% url 'order_list' %}">📦 Мои заказы</a>
                    {% if show_edit or show_delete %}
                        <a href="{% url 'manage_users' %}">👥 Пользователи</a>
                    {% endif %}
                    <a href="{% url 'logout' %}">🚪 Выход</a>
                {% else %}
                    <span style="color: #999;">Не авторизированы</span>
                    <a href="{% url 'login' %}">🔓 Вход</a>
                    <a href="{% url 'register' %}">✍️ Регистрация</a>
                {% endif %}
            </nav>
            
            {% if show_add_product %}
                <div class="admin-controls">
                    <a href="{% url 'add_product' %}" class="btn-admin">➕ Добавить товар</a>
                </div>
            {% endif %}
        </header>

        {% if user.is_authenticated and user.profile.is_authorized %}
            <div class="filter-section">
                <h3>🔍 Фильтр товаров</h3>
                <form method="get" class="filter-form">
                    <input type="text" name="search" placeholder="Поиск по названию..." value="{{ request.GET.search }}">
                    <input type="number" name="price_min" placeholder="Цена от (₽)" value="{{ request.GET.price_min }}" min="0" step="0.01">
                    <input type="number" name="price_max" placeholder="Цена до (₽)" value="{{ request.GET.price_max }}" min="0" step="0.01">
                    <button type="submit">🔎 Найти</button>
                    <a href="{% url 'product_list' %}"><button type="button" class="btn-clear">✖ Сбросить</button></a>
                </form>
            </div>
        {% endif %}

        {% if products %}
            <div class="products">
                {% for product in products %}
                    <div class="product">
                        <h3>{{ product.name }}</h3>
                        <p><strong>SKU:</strong> {{ product.sku }}</p>
                        <p>{{ product.description }}</p>
                        <div class="price">{{ product.price }} ₽</div>
                        
                        <div class="product-actions">
                            {% if user.is_authenticated and user.profile.is_authorized %}
                                <a href="{% url 'create_order' product.id 1 %}" class="btn">Заказать</a>
                            {% elif user.is_authenticated %}
                                <p style="color: #999; font-size: 12px;">Недоступно для вашей роли</p>
                            {% else %}
                                <p style="color: #999; font-size: 12px;">Войдите, чтобы заказать</p>
                            {% endif %}
                            
                            {% if show_edit %}
                                <a href="{% url 'edit_product' product.id %}" class="btn btn-edit">✏️ Редактировать</a>
                            {% endif %}
                            
                            {% if show_delete %}
                                <a href="{% url 'delete_product' product.id %}" class="btn btn-delete">🗑️ Удалить</a>
                            {% endif %}
                        </div>
                    </div>
                {% endfor %}
            </div>
        {% else %}
            <div class="empty">
                <p>📭 Товары не найдены</p>
                {% if show_add_product %}
                    <p style="font-size: 12px; margin-top: 10px;"><a href="{% url 'add_product' %}" style="color: #007bff;">Добавьте первый товар</a></p>
                {% else %}
                    <p style="font-size: 12px; margin-top: 10px;">Товары добавятся администратором</p>
                {% endif %}
            </div>
        {% endif %}
    </div>
</body>
</html>
```

### 14.2. register.html — Регистрация

Создайте файл `bodies/templates/register.html`:

```html
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Регистрация</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: Arial, sans-serif; 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
            display: flex; 
            justify-content: center; 
            align-items: center; 
            min-height: 100vh; 
        }
        .form-container { 
            background: white; 
            padding: 40px; 
            border-radius: 10px; 
            box-shadow: 0 10px 25px rgba(0,0,0,0.2); 
            width: 100%; 
            max-width: 400px; 
        }
        h1 { 
            text-align: center; 
            margin-bottom: 30px; 
            color: #333; 
            font-size: 24px; 
        }
        form { 
            display: flex; 
            flex-direction: column; 
        }
        label { 
            margin-top: 15px; 
            font-weight: bold; 
            color: #333; 
            font-size: 14px; 
        }
        input { 
            padding: 10px; 
            margin-top: 5px; 
            border: 1px solid #ddd; 
            border-radius: 5px; 
            font-size: 14px; 
        }
        input:focus { 
            outline: none; 
            border-color: #667eea; 
            box-shadow: 0 0 5px rgba(102, 126, 234, 0.3); 
        }
        button { 
            margin-top: 20px; 
            padding: 12px; 
            background: #28a745; 
            color: white; 
            border: none; 
            border-radius: 5px; 
            cursor: pointer; 
            font-size: 16px; 
            font-weight: bold; 
        }
        button:hover { 
            background: #218838; 
        }
        .link { 
            text-align: center; 
            margin-top: 20px; 
        }
        .link a { 
            color: #667eea; 
            text-decoration: none; 
        }
        .link a:hover { 
            text-decoration: underline; 
        }
        .help-text { 
            font-size: 12px; 
            color: #999; 
            margin-top: 5px; 
        }
        ul { 
            list-style: none; 
            padding: 0; 
        }
        li { 
            color: #666; 
            font-size: 12px; 
            margin: 5px 0; 
        }
        .form-group {
            margin-bottom: 15px;
        }
        .form-group label {
            display: block;
            margin-bottom: 5px;
            font-weight: bold;
            color: #333;
        }
        .form-group input {
            width: 100%;
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 5px;
            font-size: 14px;
            box-sizing: border-box;
        }
        .form-group input:focus {
            outline: none;
            border-color: #667eea;
            box-shadow: 0 0 5px rgba(102, 126, 234, 0.3);
        }
        .error-message {
            color: #dc3545;
            font-size: 12px;
            margin-top: 5px;
        }
        .help-text {
            font-size: 12px;
            color: #666;
            margin-top: 5px;
            font-style: italic;
        }
        .success-message {
            background: #d4edda;
            color: #155724;
            padding: 10px;
            border-radius: 5px;
            margin-bottom: 15px;
            border: 1px solid #c3e6cb;
        }
    </style>
</head>
<body>
    <div class="form-container">
        <h1>✍️ Регистрация</h1>
        {% if form.non_field_errors %}
            <div style="background: #f8d7da; color: #721c24; padding: 10px; border-radius: 5px; margin-bottom: 15px; border: 1px solid #f5c6cb;">
                <strong>Ошибка регистрации:</strong>
                {% for error in form.non_field_errors %}
                    <p style="margin: 5px 0;">• {{ error }}</p>
                {% endfor %}
            </div>
        {% endif %}
        <form method="post">
            {% csrf_token %}
            
            <!-- Username field -->
            <div class="form-group">
                {{ form.username.label_tag }}
                {{ form.username }}
                {% if form.username.errors %}
                    <div class="error-message">
                        {% for error in form.username.errors %}
                            <p>⚠️ {{ error }}</p>
                        {% endfor %}
                    </div>
                {% endif %}
                {% if form.username.help_text %}
                    <div class="help-text">{{ form.username.help_text|safe }}</div>
                {% endif %}
            </div>
            
            <!-- Password1 field -->
            <div class="form-group">
                {{ form.password1.label_tag }}
                {{ form.password1 }}
                {% if form.password1.errors %}
                    <div class="error-message">
                        {% for error in form.password1.errors %}
                            <p>⚠️ {{ error }}</p>
                        {% endfor %}
                    </div>
                {% endif %}
                {% if form.password1.help_text %}
                    <div class="help-text">{{ form.password1.help_text|safe }}</div>
                {% endif %}
            </div>
            
            <!-- Password2 field -->
            <div class="form-group">
                {{ form.password2.label_tag }}
                {{ form.password2 }}
                {% if form.password2.errors %}
                    <div class="error-message">
                        {% for error in form.password2.errors %}
                            <p>⚠️ {{ error }}</p>
                        {% endfor %}
                    </div>
                {% endif %}
                {% if form.password2.help_text %}
                    <div class="help-text">{{ form.password2.help_text|safe }}</div>
                {% endif %}
            </div>
            
            <button type="submit">Зарегистрироваться</button>
        </form>
        <div class="link">
            Уже есть аккаунт? <a href="{% url 'login' %}">Войдите</a>
        </div>
    </div>
</body>
</html>
```

### 14.3. login.html — Вход в систему

Создайте файл `bodies/templates/login.html`:

```html
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Вход</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: Arial, sans-serif; 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
            display: flex; 
            justify-content: center; 
            align-items: center; 
            min-height: 100vh; 
        }
        .form-container { 
            background: white; 
            padding: 40px; 
            border-radius: 10px; 
            box-shadow: 0 10px 25px rgba(0,0,0,0.2); 
            width: 100%; 
            max-width: 400px; 
        }
        h1 { 
            text-align: center; 
            margin-bottom: 30px; 
            color: #333; 
            font-size: 24px; 
        }
        form { 
            display: flex; 
            flex-direction: column; 
        }
        label { 
            margin-top: 15px; 
            font-weight: bold; 
            color: #333; 
            font-size: 14px; 
        }
        input { 
            padding: 10px; 
            margin-top: 5px; 
            border: 1px solid #ddd; 
            border-radius: 5px; 
            font-size: 14px; 
        }
        input:focus { 
            outline: none; 
            border-color: #667eea; 
            box-shadow: 0 0 5px rgba(102, 126, 234, 0.3); 
        }
        button { 
            margin-top: 20px; 
            padding: 12px; 
            background: #667eea; 
            color: white; 
            border: none; 
            border-radius: 5px; 
            cursor: pointer; 
            font-size: 16px; 
            font-weight: bold; 
        }
        button:hover { 
            background: #5568d3; 
        }
        .link { 
            text-align: center; 
            margin-top: 20px; 
        }
        .link a { 
            color: #667eea; 
            text-decoration: none; 
        }
        .link a:hover { 
            text-decoration: underline; 
        }
        .error { 
            color: #dc3545; 
            font-size: 12px; 
            margin-top: 5px; 
            background: #f8d7da; 
            padding: 10px; 
            border-radius: 3px; 
            border: 1px solid #f5c6cb; 
        }
    </style>
</head>
<body>
    <div class="form-container">
        <h1>🔓 Вход в систему</h1>
        {% if error %}
            <div class="error">{{ error }}</div>
        {% endif %}
        <form method="post">
            {% csrf_token %}
            <label for="username">Имя пользователя:</label>
            <input type="text" id="username" name="username" required>
            
            <label for="password">Пароль:</label>
            <input type="password" id="password" name="password" required>
            
            <button type="submit">Войти</button>
        </form>
        <div class="link">
            Нет аккаунта? <a href="{% url 'register' %}">Зарегистрируйтесь</a>
        </div>
    </div>
</body>
</html>
```

### 14.4. order_list.html — Мои заказы

Создайте файл `bodies/templates/order_list.html`:

```html
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Мои заказы</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: Arial, sans-serif; background: #f5f5f5; padding: 20px; }
        .container { max-width: 1200px; margin: 0 auto; }
        header { background: white; padding: 20px; border-radius: 5px; margin-bottom: 20px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }
        h1 { color: #333; margin-bottom: 10px; }
        nav { margin: 10px 0; }
        nav a { margin-right: 15px; text-decoration: none; color: #007bff; font-weight: bold; }
        nav a:hover { text-decoration: underline; }
        nav span { color: #666; margin-right: 15px; }
        table { 
            width: 100%; 
            border-collapse: collapse; 
            background: white; 
            border-radius: 5px; 
            overflow: hidden; 
            box-shadow: 0 2px 5px rgba(0,0,0,0.1); 
        }
        th, td { 
            padding: 15px; 
            text-align: left; 
            border-bottom: 1px solid #ddd; 
        }
        th { 
            background: #f0f0f0; 
            font-weight: bold; 
            color: #333; 
        }
        tr:hover { 
            background: #f9f9f9; 
        }
        .empty { 
            text-align: center; 
            padding: 40px; 
            background: white; 
            border-radius: 5px; 
            color: #999; 
            box-shadow: 0 2px 5px rgba(0,0,0,0.1); 
        }
        .badge { 
            padding: 5px 10px; 
            border-radius: 3px; 
            font-size: 12px; 
            font-weight: bold; 
        }
        .badge-new { 
            background: #ffc107; 
            color: white; 
        }
        .badge-delivered { 
            background: #28a745; 
            color: white; 
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>📦 Мои заказы</h1>
            <nav>
                <a href="{% url 'product_list' %}">← Назад в каталог</a>
                <span>👤 {{ user.username }}</span>
                <a href="{% url 'logout' %}">🚪 Выход</a>
            </nav>
        </header>

        {% if orders %}
            <table>
                <thead>
                    <tr>
                        <th>№ Заказа</th>
                        <th>Товары (SKU)</th>
                        <th>Дата заказа</th>
                        <th>Статус</th>
                        <th>Пункт выдачи</th>
                        <th>Код получения</th>
                    </tr>
                </thead>
                <tbody>
                    {% for order in orders %}
                    <tr>
                        <td><strong>#{{ order.id }}</strong></td>
                        <td>{{ order.get_skus }}</td>
                        <td>{{ order.createdAt|date:"d.m.Y H:i" }}</td>
                        <td>
                            {% if order.status == 'new' %}
                                <span class="badge badge-new">{{ order.get_status_display }}</span>
                            {% else %}
                                <span class="badge badge-delivered">{{ order.get_status_display }}</span>
                            {% endif %}
                        </td>
                        <td>{{ order.pickupPoint.address }}</td>
                        <td><strong style="color: #28a745;">{{ order.receiveCode }}</strong></td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        {% else %}
            <div class="empty">
                <p>📭 У вас нет заказов</p>
                <p><a href="{% url 'product_list' %}" style="color: #007bff;">← Перейти в каталог</a></p>
            </div>
        {% endif %}
    </div>
</body>
</html>
```

### 14.5. add_product.html — Добавление товара

Создайте файл `bodies/templates/add_product.html`:

```html
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Добавить товар</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: Arial, sans-serif; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; display: flex; align-items: center; justify-content: center; padding: 20px; }
        .container { background: white; padding: 40px; border-radius: 10px; box-shadow: 0 10px 25px rgba(0,0,0,0.2); max-width: 600px; width: 100%; }
        h1 { margin-bottom: 30px; color: #333; text-align: center; }
        .form-group { margin-bottom: 20px; }
        label { display: block; margin-bottom: 5px; color: #555; font-weight: bold; }
        input, textarea { width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 5px; font-size: 14px; font-family: Arial, sans-serif; }
        input:focus, textarea:focus { outline: none; border-color: #667eea; box-shadow: 0 0 5px rgba(102, 126, 234, 0.3); }
        textarea { resize: vertical; min-height: 100px; }
        .btn-group { display: flex; gap: 10px; margin-top: 30px; }
        button { flex: 1; padding: 12px; border: none; border-radius: 5px; font-size: 16px; font-weight: bold; cursor: pointer; transition: all 0.3s ease; }
        .btn-submit { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; }
        .btn-submit:hover { transform: translateY(-2px); box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4); }
        .btn-cancel { background: #f0f0f0; color: #666; }
        .btn-cancel:hover { background: #e0e0e0; }
    </style>
</head>
<body>
    <div class="container">
        <h1>➕ Добавить новый товар</h1>
        <form method="post">
            {% csrf_token %}
            <div class="form-group">
                <label for="name">Название товара *</label>
                <input type="text" id="name" name="name" required>
            </div>
            <div class="form-group">
                <label for="sku">Артикул (SKU) *</label>
                <input type="text" id="sku" name="sku" required>
            </div>
            <div class="form-group">
                <label for="price">Цена (руб.) *</label>
                <input type="number" id="price" name="price" step="0.01" min="0" required>
            </div>
            <div class="form-group">
                <label for="description">Описание</label>
                <textarea id="description" name="description"></textarea>
            </div>
            <div class="btn-group">
                <button type="submit" class="btn-submit">Добавить товар</button>
                <a href="{% url 'product_list' %}" style="flex: 1;">
                    <button type="button" class="btn-cancel" onclick="window.history.back()">Отмена</button>
                </a>
            </div>
        </form>
    </div>
</body>
</html>
```

### 14.6. edit_product.html — Редактирование товара

Создайте файл `bodies/templates/edit_product.html`:

```html
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Редактировать товар</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: Arial, sans-serif; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; display: flex; align-items: center; justify-content: center; padding: 20px; }
        .container { background: white; padding: 40px; border-radius: 10px; box-shadow: 0 10px 25px rgba(0,0,0,0.2); max-width: 600px; width: 100%; }
        h1 { margin-bottom: 30px; color: #333; text-align: center; }
        .form-group { margin-bottom: 20px; }
        label { display: block; margin-bottom: 5px; color: #555; font-weight: bold; }
        input, textarea { width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 5px; font-size: 14px; font-family: Arial, sans-serif; }
        input:focus, textarea:focus { outline: none; border-color: #667eea; box-shadow: 0 0 5px rgba(102, 126, 234, 0.3); }
        textarea { resize: vertical; min-height: 100px; }
        .btn-group { display: flex; gap: 10px; margin-top: 30px; }
        button { flex: 1; padding: 12px; border: none; border-radius: 5px; font-size: 16px; font-weight: bold; cursor: pointer; transition: all 0.3s ease; }
        .btn-submit { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; }
        .btn-submit:hover { transform: translateY(-2px); box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4); }
        .btn-cancel { background: #f0f0f0; color: #666; }
        .btn-cancel:hover { background: #e0e0e0; }
    </style>
</head>
<body>
    <div class="container">
        <h1>✏️ Редактировать товар</h1>
        <form method="post">
            {% csrf_token %}
            <div class="form-group">
                <label for="name">Название товара *</label>
                <input type="text" id="name" name="name" value="{{ product.name }}" required>
            </div>
            <div class="form-group">
                <label for="sku">Артикул (SKU) *</label>
                <input type="text" id="sku" name="sku" value="{{ product.sku }}" required>
            </div>
            <div class="form-group">
                <label for="price">Цена (руб.) *</label>
                <input type="number" id="price" name="price" step="0.01" min="0" value="{{ product.price }}" required>
            </div>
            <div class="form-group">
                <label for="description">Описание</label>
                <textarea id="description" name="description">{{ product.description }}</textarea>
            </div>
            <div class="btn-group">
                <button type="submit" class="btn-submit">Сохранить изменения</button>
                <a href="{% url 'product_list' %}" style="flex: 1;">
                    <button type="button" class="btn-cancel" onclick="window.history.back()">Отмена</button>
                </a>
            </div>
        </form>
    </div>
</body>
</html>
```

### 14.7. confirm_delete.html — Подтверждение удаления

Создайте файл `bodies/templates/confirm_delete.html`:

```html
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Подтвердить удаление</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: Arial, sans-serif; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; display: flex; align-items: center; justify-content: center; padding: 20px; }
        .container { background: white; padding: 40px; border-radius: 10px; box-shadow: 0 10px 25px rgba(0,0,0,0.2); max-width: 400px; width: 100%; text-align: center; }
        .icon { font-size: 48px; margin-bottom: 20px; }
        h1 { margin-bottom: 15px; color: #333; }
        .message { color: #666; margin-bottom: 30px; font-size: 16px; }
        .object-name { background: #f0f0f0; padding: 10px; border-radius: 5px; margin: 20px 0; font-weight: bold; color: #333; }
        .btn-group { display: flex; gap: 10px; margin-top: 30px; }
        button, a { flex: 1; padding: 12px; border: none; border-radius: 5px; font-size: 16px; font-weight: bold; cursor: pointer; transition: all 0.3s ease; text-decoration: none; display: flex; align-items: center; justify-content: center; }
        .btn-delete { background: #dc3545; color: white; }
        .btn-delete:hover { background: #c82333; transform: translateY(-2px); box-shadow: 0 5px 15px rgba(220, 53, 69, 0.4); }
        .btn-cancel { background: #f0f0f0; color: #666; }
        .btn-cancel:hover { background: #e0e0e0; }
    </style>
</head>
<body>
    <div class="container">
        <div class="icon">⚠️</div>
        <h1>Подтвердить удаление</h1>
        <p class="message">Вы уверены, что хотите удалить {{ object_type }}?</p>
        <div class="object-name">{{ object }}</div>
        <p style="color: #999; font-size: 14px;">Это действие невозможно отменить.</p>
        <form method="post" style="display: inline-block; width: 100%;">
            {% csrf_token %}
            <div class="btn-group">
                <button type="submit" class="btn-delete">Удалить</button>
                <a href="{% url 'product_list' %}" class="btn-cancel">Отмена</a>
            </div>
        </form>
    </div>
</body>
</html>
```

### 14.8. manage_users.html — Управление пользователями

Создайте файл `bodies/templates/manage_users.html`:

```html
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Управление пользователями</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: Arial, sans-serif; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; padding: 20px; }
        .container { max-width: 900px; margin: 0 auto; background: white; border-radius: 10px; box-shadow: 0 10px 25px rgba(0,0,0,0.2); padding: 30px; }
        header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 30px; padding-bottom: 20px; border-bottom: 2px solid #f0f0f0; }
        h1 { color: #333; }
        .btn { padding: 10px 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; text-decoration: none; border: none; border-radius: 5px; cursor: pointer; transition: all 0.3s ease; font-weight: bold; }
        .btn:hover { transform: translateY(-2px); box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4); }
        .btn-back { background: #f0f0f0; color: #666; }
        .btn-back:hover { background: #e0e0e0; }
        table { width: 100%; border-collapse: collapse; margin-top: 20px; }
        th { background: #f8f9fa; padding: 15px; text-align: left; color: #333; font-weight: bold; border-bottom: 2px solid #ddd; }
        td { padding: 12px 15px; border-bottom: 1px solid #ddd; }
        tr:hover { background: #f8f9fa; }
        .role-badge { display: inline-block; padding: 5px 12px; border-radius: 20px; font-size: 12px; font-weight: bold; text-transform: uppercase; }
        .role-admin { background: #dc3545; color: white; }
        .role-editor { background: #ffc107; color: #333; }
        .role-authorized { background: #28a745; color: white; }
        .role-unauthorized { background: #6c757d; color: white; }
        .actions { display: flex; gap: 10px; }
        .btn-small { padding: 6px 12px; font-size: 12px; text-decoration: none; display: inline-block; }
        .btn-edit { background: #007bff; color: white; }
        .btn-edit:hover { background: #0056b3; }
        .btn-delete { background: #dc3545; color: white; }
        .btn-delete:hover { background: #c82333; }
        .empty-message { text-align: center; padding: 40px; color: #666; }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>👥 Управление пользователями</h1>
            <a href="{% url 'product_list' %}" class="btn btn-back">← Вернуться</a>
        </header>

        {% if users %}
            <table>
                <thead>
                    <tr>
                        <th>Пользователь</th>
                        <th>Email</th>
                        <th>Роль</th>
                        <th>Дата регистрации</th>
                        <th>Действия</th>
                    </tr>
                </thead>
                <tbody>
                    {% for user in users %}
                        <tr>
                            <td><strong>{{ user.username }}</strong></td>
                            <td>{{ user.email|default:"—" }}</td>
                            <td>
                                <span class="role-badge role-{{ user.profile.role }}">
                                    {{ user.profile.get_role_display }}
                                </span>
                            </td>
                            <td>{{ user.date_joined|date:"d.m.Y H:i" }}</td>
                            <td>
                                <div class="actions">
                                    <a href="{% url 'edit_user_role' user.id %}" class="btn btn-small btn-edit">✏️ Роль</a>
                                    {% if user.id != request.user.id %}
                                        <a href="{% url 'delete_user' user.id %}" class="btn btn-small btn-delete">🗑️ Удалить</a>
                                    {% else %}
                                        <span style="color: #999;">👤 Ваш профиль</span>
                                    {% endif %}
                                </div>
                            </td>
                        </tr>
                    {% endfor %}
                </tbody>
            </table>
        {% else %}
            <div class="empty-message">
                <p>Нет пользователей в системе</p>
            </div>
        {% endif %}
    </div>
</body>
</html>
```

### 14.9. edit_user_role.html — Изменение роли

Создайте файл `bodies/templates/edit_user_role.html`:

```html
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Изменить роль пользователя</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: Arial, sans-serif; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; display: flex; align-items: center; justify-content: center; padding: 20px; }
        .container { background: white; padding: 40px; border-radius: 10px; box-shadow: 0 10px 25px rgba(0,0,0,0.2); max-width: 500px; width: 100%; }
        h1 { margin-bottom: 10px; color: #333; text-align: center; }
        .username { text-align: center; color: #666; margin-bottom: 30px; font-size: 16px; }
        .form-group { margin-bottom: 25px; }
        label { display: block; margin-bottom: 10px; color: #333; font-weight: bold; }
        select { width: 100%; padding: 12px; border: 2px solid #ddd; border-radius: 5px; font-size: 16px; cursor: pointer; transition: all 0.3s ease; }
        select:focus { outline: none; border-color: #667eea; box-shadow: 0 0 5px rgba(102, 126, 234, 0.3); }
        .btn-group { display: flex; gap: 10px; margin-top: 30px; }
        button { flex: 1; padding: 12px; border: none; border-radius: 5px; font-size: 16px; font-weight: bold; cursor: pointer; transition: all 0.3s ease; }
        .btn-submit { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; }
        .btn-submit:hover { transform: translateY(-2px); box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4); }
        .btn-cancel { background: #f0f0f0; color: #666; }
        .btn-cancel:hover { background: #e0e0e0; }
        .role-descriptions { margin-top: 20px; padding: 15px; background: #f8f9fa; border-radius: 5px; font-size: 13px; }
        .role-descriptions h4 { color: #333; margin-bottom: 10px; }
        .role-desc { margin-bottom: 10px; color: #666; }
        .role-desc strong { color: #333; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🔐 Изменить роль пользователя</h1>
        <div class="username">Пользователь: <strong>{{ user.username }}</strong></div>
        
        <form method="post">
            {% csrf_token %}
            
            <div class="form-group">
                <label for="role">Новая роль</label>
                <select name="role" id="role" required>
                    {% for value, label in profile.ROLE_CHOICES %}
                        <option value="{{ value }}" {% if profile.role == value %}selected{% endif %}>
                            {{ label }}
                        </option>
                    {% endfor %}
                </select>
            </div>

            <div class="role-descriptions">
                <h4>📋 Описание ролей:</h4>
                <div class="role-desc">
                    <strong>Неавторизированный:</strong> Просмотр товаров без фильтрации
                </div>
                <div class="role-desc">
                    <strong>Авторизированный:</strong> Просмотр товаров с фильтрацией, создание заказов
                </div>
                <div class="role-desc">
                    <strong>Редактор:</strong> Редактирование товаров и пользовательских данных
                </div>
                <div class="role-desc">
                    <strong>Администратор:</strong> Полный доступ - создание и удаление товаров и пользователей
                </div>
            </div>

            <div class="btn-group">
                <button type="submit" class="btn-submit">Сохранить роль</button>
                <a href="{% url 'manage_users' %}" style="flex: 1;">
                    <button type="button" class="btn-cancel" onclick="window.history.back()">Отмена</button>
                </a>
            </div>
        </form>
    </div>
</body>
</html>
```

---

## 15. Создание management-команд

Management-команды позволяют запускать скрипты через `python manage.py <команда>`.

### 15.1. Структура файлов

Убедитесь, что существуют папки и `__init__.py`:

```
bodies/
└── management/
    ├── __init__.py          # Пустой файл
    └── commands/
        ├── __init__.py      # Пустой файл
        ├── create_test_users.py
        └── import_products.py
```

### 15.2. create_test_users.py — Создание тестовых пользователей

Создайте файл `bodies/management/commands/create_test_users.py`:

```python
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
```

### 15.3. import_products.py — Импорт товаров из Excel

Создайте файл `bodies/management/commands/import_products.py`:

```python
import openpyxl
from django.core.management.base import BaseCommand
from bodies.models import Product


class Command(BaseCommand):
    """Команда для импорта товаров из Excel файла"""
    
    help = 'Импортирует товары из Excel-файла'

    def add_arguments(self, parser):
        parser.add_argument(
            'file_path',
            type=str,
            help='Путь к Excel-файлу с товарами'
        )

    def handle(self, *args, **options):
        file_path = options['file_path']
        
        try:
            wb = openpyxl.load_workbook(file_path)
            ws = wb.active
            
            # Получить заголовки из первой строки
            headers = [cell.value for cell in ws[1]]
            count = 0
            
            # Пройти по каждой строке, начиная со второй
            for row in ws.iter_rows(min_row=2, values_only=True):
                data = dict(zip(headers, row))
                
                if not data.get('Артикул'):
                    continue
                
                # update_or_create - создаст если не существует, обновит если существует
                Product.objects.update_or_create(
                    sku=data['Артикул'],
                    defaults={
                        'name':        data.get('Наименование товара', ''),
                        'price':       str(data.get('Цена', 0)).replace(',', '.'),
                        'description': data.get('Описание товара', '') or '',
                    }
                )
                count += 1
            
            self.stdout.write(
                self.style.SUCCESS(f'✅ Успешно импортировано {count} товаров')
            )
            
        except FileNotFoundError:
            self.stdout.write(
                self.style.ERROR(f'❌ Файл не найден: {file_path}')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Ошибка при импорте: {str(e)}')
            )
```

---

## 16. Создание базы данных PostgreSQL

Перед миграциями нужно создать базу данных.

### Вариант 1: Через psql (терминал)

```bash
# Подключиться к PostgreSQL
psql -U postgres

# Создать базу данных
CREATE DATABASE shop;

# Выйти
\q
```

### Вариант 2: Через DBeaver

1. Откройте DBeaver
2. Подключитесь к PostgreSQL (localhost, 5432, postgres/postgres)
3. Правой кнопкой → Create Database → Имя: `shop`

### Вариант 3: Через pgAdmin

1. Откройте pgAdmin
2. Servers → PostgreSQL → Databases → Правой кнопкой → Create → Database
3. Введите имя: `shop`

---

## 17. Миграции и запуск

### Шаг 1: Создать миграции

```bash
cd example
python manage.py makemigrations
```

Вывод:
```
Migrations for 'bodies':
  bodies/migrations/0001_initial.py
    - Create model Product
    - Create model PickupPoint
    - Create model Profile
    - Create model Order
```

### Шаг 2: Применить миграции

```bash
python manage.py migrate
```

Вывод:
```
Operations to perform:
  Apply all migrations: admin, auth, bodies, contenttypes, sessions
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  ...
  Applying bodies.0001_initial... OK
  Applying sessions.0001_initial... OK
```

### Шаг 3: Создать суперпользователя (необязательно)

```bash
python manage.py createsuperuser
# Username: admin
# Email: (оставьте пустым)
# Password: admin (подтвердите дважды)
```

### Шаг 4: Создать тестовых пользователей

```bash
python manage.py create_test_users
```

### Шаг 5: Запустить сервер

```bash
python manage.py runserver
```

Вывод:
```
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```

---

## 18. Проверка работоспособности

### Открыть в браузере

| URL | Описание |
|-----|----------|
| `http://127.0.0.1:8000/` | Каталог товаров |
| `http://127.0.0.1:8000/register/` | Регистрация |
| `http://127.0.0.1:8000/login/` | Вход |
| `http://127.0.0.1:8000/admin/` | Django админ-панель |
| `http://127.0.0.1:8000/orders/` | Мои заказы |
| `http://127.0.0.1:8000/users/` | Управление пользователями (admin) |

### Тестовые аккаунты

| Логин | Пароль | Роль |
|-------|--------|------|
| `admin` | `admin` | Администратор (полный доступ) |
| `editor` | `editor` | Редактор (редактирование товаров) |
| `user` | `user` | Авторизированный (заказы и фильтрация) |
| `guest` | `guest` | Неавторизированный (только просмотр) |

### Контрольный список

- [ ] Сервер запускается без ошибок: `python manage.py runserver`
- [ ] Проверка системы: `python manage.py check` → System check identified no issues
- [ ] Главная страница открывается: `http://127.0.0.1:8000/`
- [ ] Регистрация нового пользователя работает
- [ ] Вход и выход работают
- [ ] Админ-панель доступна: `http://127.0.0.1:8000/admin/`
- [ ] Фильтрация товаров работает для авторизированных пользователей
- [ ] Администратор может добавлять, редактировать и удалять товары
- [ ] Администратор может управлять пользователями и их ролями
- [ ] Заказы создаются и отображаются в истории

---

## 📁 Итоговая структура проекта

После выполнения всех шагов структура проекта будет:

```
example/
├── manage.py                          # Django CLI
├── requirements.txt                   # Зависимости
│
├── config/                            # ⚙️ Конфигурация
│   ├── __init__.py
│   ├── settings.py                    # Настройки проекта
│   ├── urls.py                        # Главные маршруты
│   ├── wsgi.py                        # WSGI
│   └── asgi.py                        # ASGI
│
├── bodies/                            # 🎯 Основное приложение
│   ├── __init__.py
│   ├── models.py                      # Модели БД
│   ├── views.py                       # Представления
│   ├── forms.py                       # Формы
│   ├── urls.py                        # Маршруты приложения
│   ├── admin.py                       # Админ-панель
│   ├── signals.py                     # Сигналы
│   ├── apps.py                        # Конфигурация приложения
│   ├── tests.py                       # Тесты
│   │
│   ├── templates/                     # 🎨 HTML-шаблоны
│   │   ├── products.html              # Каталог товаров
│   │   ├── register.html              # Регистрация
│   │   ├── login.html                 # Вход
│   │   ├── order_list.html            # Мои заказы
│   │   ├── add_product.html           # Добавление товара
│   │   ├── edit_product.html          # Редактирование товара
│   │   ├── confirm_delete.html        # Подтверждение удаления
│   │   ├── manage_users.html          # Управление пользователями
│   │   └── edit_user_role.html        # Изменение роли
│   │
│   ├── management/                    # 🔧 Management-команды
│   │   ├── __init__.py
│   │   └── commands/
│   │       ├── __init__.py
│   │       ├── create_test_users.py   # Создание тестовых пользователей
│   │       └── import_products.py     # Импорт товаров из Excel
│   │
│   └── migrations/                    # 🗄️ Миграции БД
│       ├── __init__.py
│       └── 0001_initial.py            # Автоматически сгенерирована
│
└── venv/                              # 🔒 Виртуальное окружение (не коммитится)
```

---

## 🔄 Порядок создания файлов (Краткое резюме)

| Шаг | Действие | Файлы |
|-----|----------|-------|
| 1 | Установка Python и PostgreSQL | — |
| 2 | Создать venv, установить пакеты | `requirements.txt` |
| 3 | `django-admin startproject config .` | `manage.py`, `config/*` |
| 4 | `python manage.py startapp bodies` | `bodies/*` |
| 5 | Настроить settings.py | `config/settings.py` |
| 6 | Написать модели | `bodies/models.py` |
| 7 | Написать формы | `bodies/forms.py` |
| 8 | Написать представления | `bodies/views.py` |
| 9 | Настроить маршруты | `config/urls.py`, `bodies/urls.py` |
| 10 | Настроить админку | `bodies/admin.py` |
| 11 | Написать сигналы | `bodies/signals.py` |
| 12 | Подключить сигналы | `bodies/apps.py` |
| 13 | Создать шаблоны (9 файлов) | `bodies/templates/*.html` |
| 14 | Создать команды | `bodies/management/commands/*.py` |
| 15 | Создать БД PostgreSQL | `CREATE DATABASE shop;` |
| 16 | Миграции | `python manage.py makemigrations && migrate` |
| 17 | Создать пользователей | `python manage.py create_test_users` |
| 18 | Запустить сервер | `python manage.py runserver` |

---

**Готово! 🎉 Проект полностью собран с нуля и готов к работе!**
