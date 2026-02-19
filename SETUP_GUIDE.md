# 🔧 Подробное руководство — Создание моделей, БД, настройка Django

Полошаговое руководство по созданию Django проекта с нуля, включая настройку моделей, пользователей, базы данных, settings.py и urls.py.

---

## 📋 Содержание

1. [Подготовка окружения](#подготовка-окружения)
2. [Создание проекта и приложения](#создание-проекта-и-приложения)
3. [Подключение PostgreSQL](#подключение-postgresql)
4. [Настройка settings.py](#настройка-settingspy)
5. [Создание моделей](#создание-моделей)
6. [Миграции и создание таблиц](#миграции-и-создание-таблиц)
7. [Создание суперпользователя](#создание-суперпользователя)
8. [Регистрация моделей в админ-панели](#регистрация-моделей-в-админ-панели)
9. [Настройка URLs](#настройка-urls)
10. [Проверка и тестирование](#проверка-и-тестирование)

---

# 1️⃣ Подготовка окружения

## Шаг 1.1 — Создание папки проекта

```bash
# Windows PowerShell
mkdir C:\exam\django_shop
cd C:\exam\django_shop

# Или Linux/Mac
mkdir ~/exam/django_shop
cd ~/exam/django_shop
```

## Шаг 1.2 — Создание виртуального окружения

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

После активации в начале строки должно появиться `(venv)`.

## Шаг 1.3 — Обновление pip

```bash
pip install --upgrade pip
```

## Шаг 1.4 — Установка зависимостей

```bash
pip install django==6.0.1 psycopg2-binary openpyxl
```

**Что устанавливается:**
- `django` — веб-фреймворк
- `psycopg2-binary` — драйвер для PostgreSQL
- `openpyxl` — работа с Excel-файлами

Проверить установку:
```bash
python -m django --version
# Output: 6.0.1
```

---

# 2️⃣ Создание проекта и приложения

## Шаг 2.1 — Создание Django проекта

```bash
django-admin startproject back .
```

**Результат:**
```
back/                    <- папка конфигурации проекта
  __init__.py
  settings.py           <- главный файл конфигурации
  urls.py               <- маршруты главного проекта
  asgi.py
  wsgi.py
manage.py               <- интерфейс командной строки
db.sqlite3              <- база данных (по умолчанию)
venv/                   <- виртуальное окружение
```

## Шаг 2.2 — Создание приложения

```bash
python manage.py startapp bodies
```

**Результат:**
```
bodies/                 <- папка приложения
  migrations/           <- папка для миграций
    __init__.py
  __init__.py
  admin.py              <- настройка админ-панели
  apps.py               <- конфигурация приложения
  models.py             <- модели БД
  tests.py              <- тесты
  views.py              <- представления (контроллеры)
  urls.py               <- маршруты приложения (нужно создать)
```

---

# 3️⃣ Подключение PostgreSQL

## Шаг 3.1 — Создание базы данных (DBeaver)

**Вариант 1: Через DBeaver (рекомендуется на экзамене)**

1. Открыть **DBeaver**
2. **Database → New Connection**
3. Выбрать **PostgreSQL** → **Next**
4. Заполнить параметры подключения:
   ```
   Server Host: localhost
   Port: 5432
   Database: postgres (по умолчанию)
   Username: postgres
   Password: postgres
   ```
5. Нажать **Test Connection** (должно сказать "Connected")
6. Нажать **Finish**
7. Раскрыть подключение → ПКМ на **postgres** → **Create** → **Database**
8. Параметры:
   ```
   Database Name: shop
   Encoding: UTF8
   ```
9. Нажать **OK**

**Результат:** Новая база данных `shop` создана.

## Шаг 3.2 — Создание базы данных (командная строка)

Если DBeaver не используется:

```bash
# Windows (PowerShell как администратор)
psql -U postgres -c "CREATE DATABASE shop;"

# Проверить создание
psql -U postgres -l
# Должна появиться база "shop"
```

## Шаг 3.3 — Проверка подключения

```bash
# Проверить подключение к PostgreSQL
psql -U postgres -h localhost -d shop

# Если успешно, введёт пароль и откроет консоль PostgreSQL
# Выход: \q
```

---

# 4️⃣ Настройка settings.py

Открыть файл [back/settings.py](back/back/settings.py)

## Шаг 4.1 — Подключение базы данных PostgreSQL

**Найти блок `DATABASES` (примерно строка 78):**

```python
# ❌ БЫЛО (SQL Lite)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

**Заменить на PostgreSQL:**

```python
# ✅ СТАЛО (PostgreSQL)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',  # Движок PostgreSQL
        'NAME': 'shop',                             # Имя базы (которую создали)
        'USER': 'postgres',                         # Пользователь PostgreSQL
        'PASSWORD': 'postgres',                     # Пароль PostgreSQL
        'HOST': 'localhost',                        # Адрес сервера
        'PORT': '5432',                             # Порт PostgreSQL (по умолчанию)
    }
}
```

> ⚠️ **Важно:** ENGINE должен быть `postgresql`, не `postgre**s**ql` или `mysql`!

## Шаг 4.2 — Добавление приложения в INSTALLED_APPS

**Найти блок `INSTALLED_APPS` (примерно строка 33):**

```python
# ❌ БЫЛО
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]
```

**Добавить приложение в конец:**

```python
# ✅ СТАЛО
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    'bodies',  # 👈 Добавить сюда
]
```

## Шаг 4.3 — Проверка настроек

```bash
python manage.py check
```

**Ожидаемый результат:**
```
System check identified no issues (0 silenced).
```

---

# 5️⃣ Создание моделей

Открыть файл [bodies/models.py](bodies/models.py) и заменить содержимое.

## Шаг 5.1 — Product (Товар)

```python
from django.db import models

class Product(models.Model):
    """Модель товара в магазине"""
    
    name = models.CharField(
        max_length=255,
        verbose_name="Название товара"
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Цена (руб.)"
    )
    description = models.TextField(
        blank=True,
        verbose_name="Описание товара"
    )
    sku = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="Артикул (уникальный)"
    )

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
        ordering = ['-id']

    def __str__(self):
        return f"{self.name} ({self.sku})"
```

**Поля:**
- `name` — название товара (обязательно, макс 255 символов)
- `price` — цена (10 цифр, 2 знака после точки) — можно вводить как `99.99`
- `description` — описание (может быть пусто)
- `sku` — артикул, уникальное значение (например, `SKU001`), используется для импорта

## Шаг 5.2 — PickupPoint (Пункт выдачи)

```python
class PickupPoint(models.Model):
    """Пункты выдачи заказов"""
    
    address = models.CharField(
        max_length=500,
        verbose_name="Адрес пункта выдачи"
    )

    class Meta:
        verbose_name = "Пункт выдачи"
        verbose_name_plural = "Пункты выдачи"

    def __str__(self):
        return self.address
```

**Поля:**
- `address` — полный адрес пункта выдачи

## Шаг 5.3 — Order (Заказ) и вспомогательная функция

```python
import random
import string

def generate_receive_code():
    """Генерирует 6-значный код для получения заказа"""
    return ''.join(random.choices(
        string.ascii_uppercase + string.digits,
        k=6
    ))


class Order(models.Model):
    """Заказ пользователя"""
    
    STATUS_CHOICES = [
        ('new', 'Новый'),
        ('delivered', 'Завершен'),
    ]
    
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="orders",
        verbose_name="Пользователь"
    )
    products = models.ManyToManyField(
        Product,
        verbose_name="Товары в заказе"
    )
    createdAt = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания заказа"
    )
    deliveryDate = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Дата доставки"
    )
    receiveCode = models.CharField(
        max_length=10,
        default=generate_receive_code,  # 🔴 БЕЗ скобок!
        verbose_name="Код для получения"
    )
    pickupPoint = models.ForeignKey(
        PickupPoint,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Пункт выдачи"
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='new',
        verbose_name="Статус заказа"
    )

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
```

**Поля:**
- `user` — ForeignKey на User (один пользователь — много заказов)
- `products` — ManyToManyField на Product (один заказ может содержать много товаров)
- `createdAt` — дата создания заказа (устанавливается автоматически)
- `deliveryDate` — дата доставки (может быть в будущем, опционально)
- `receiveCode` — код доставки, генерируется автоматически
- `pickupPoint` — ForeignKey на PickupPoint (где получить заказ)
- `status` — выбор из двух вариантов (new или delivered)

> ⚠️ **Важно:** `default=generate_receive_code` БЕЗ скобок! Иначе все заказы получат один и тот же код.

## Шаг 5.4 — Profile (Профиль пользователя с ролью)

```python
from django.contrib.auth.models import User

class Profile(models.Model):
    """Профиль пользователя с ролью"""
    
    ROLE_CHOICES = [
        ('admin', 'Администратор'),
        ('manager', 'Менеджер'),
        ('customer', 'Покупатель'),
    ]

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        verbose_name="Пользователь"
    )
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='customer',
        verbose_name="Роль"
    )

    class Meta:
        verbose_name = "Профиль"
        verbose_name_plural = "Профили"

    def __str__(self):
        return f"{self.user.username} ({self.get_role_display()})"
```

**Поля:**
- `user` — OneToOneField (1:1 связь с User, у каждого пользователя один профиль)
- `role` — роль пользователя (admin, manager или customer)

## Итоговый файл models.py

```python
import random
import string
from django.db import models
from django.contrib.auth.models import User


def generate_receive_code():
    """Генерирует 6-значный код для получения заказа"""
    return ''.join(random.choices(
        string.ascii_uppercase + string.digits,
        k=6
    ))


class Product(models.Model):
    """Товар в магазине"""
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
        ('admin', 'Администратор'),
        ('manager', 'Менеджер'),
        ('customer', 'Покупатель'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='customer', verbose_name="Роль")

    class Meta:
        verbose_name = "Профиль"
        verbose_name_plural = "Профили"

    def __str__(self):
        return f"{self.user.username} ({self.get_role_display()})"
```

---

# 6️⃣ Миграции и создание таблиц

## Шаг 6.1 — Создание миграции

После того как все модели созданы, нужно создать миграцию (инструкцию для БД):

```bash
python manage.py makemigrations
```

**Результат:**
```
Migrations for 'bodies':
  bodies/migrations/0001_initial.py
    - Create model Product
    - Create model PickupPoint
    - Create model Order
    - Create model Profile
```

## Шаг 6.2 — Применение миграции к БД

```bash
python manage.py migrate
```

**Результат:**
```
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, sessions, bodies
Running migrations:
  ...
  Applying bodies.0001_initial... OK
```

## Шаг 6.3 — Проверка таблиц в DBeaver

1. Открыть DBeaver
2. Раскрыть подключение postgres → Databases → shop → Schemas → public → Tables
3. Должны появиться таблицы:
   ```
   auth_user
   auth_group
   bodies_product
   bodies_pickuppoint
   bodies_order
   bodies_order_products      (ManyToMany таблица)
   bodies_profile
   ```

## Шаг 6.4 — Просмотр структуры таблицы (в DBeaver)

ПКМ на `bodies_product` → **View Structure** — увидите колонки и типы.

---

# 7️⃣ Создание суперпользователя

## Шаг 7.1 — Создание администратора

```bash
python manage.py createsuperuser
```

**Вводить:**
```
Username: admin
Email address: admin@example.com
Password: (ваш пароль, например: admin123)
Password (again): (повторить)
```

**Результат:**
```
Superuser created successfully.
```

## Шаг 7.2 — Создание обычного пользователя (опционально)

Можно через админ-панель после запуска сервера, или через shell:

```bash
python manage.py shell
```

```python
from django.contrib.auth.models import User
from bodies.models import Profile

# Создать пользователя
user = User.objects.create_user(
    username='customer1',
    email='customer1@example.com',
    password='password123'
)

# Создать профиль с ролью
profile = Profile.objects.create(user=user, role='customer')

# Выход
exit()
```

---

# 8️⃣ Регистрация моделей в админ-панели

Открыть [bodies/admin.py](bodies/admin.py) и заменить содержимое:

## Вариант 1: Минимальный (базовый)

```python
from django.contrib import admin
from .models import Product, PickupPoint, Order, Profile

admin.site.register(Product)
admin.site.register(PickupPoint)
admin.site.register(Order)
admin.site.register(Profile)
```

## Вариант 2: С кастомизацией (продвинутый)

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
    search_fields = ('address',)


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
    search_fields = ('user__username',)
```

**Что это делает:**
- `list_display` — какие колонки показывать в списке
- `search_fields` — по каким полям искать
- `list_filter` — фильтры в боковой панели
- `readonly_fields` — поля только для чтения (не редактируются)

---

# 9️⃣ Настройка URLs

## Шаг 9.1 — Создание urls.py в приложении

Создать файл: [bodies/urls.py](bodies/urls.py)

```python
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Безопасные маршруты (без аутентификации)
    path('',                          views.product_list,  name='product_list'),
    path('register/',                 views.register_view, name='register'),
    path('login/',                    views.login_view,    name='login'),
    path('logout/',                   views.logout_view,   name='logout'),
    
    # Защищённые маршруты (требуют аутентификации)
    path('orders/',                   views.order_list,    name='order_list'),
    path('buy/<int:product_id>/<int:pickup_point_id>/',
         views.create_order, name='create_order'),
]
```

**Пояснение маршрутов:**

| URL | Функция | Назначение |
|-----|---------|-----------|
| `/` | `product_list` | Показать все товары |
| `/register/` | `register_view` | Форма регистрации |
| `/login/` | `login_view` | Форма входа |
| `/logout/` | `logout_view` | Выход из системы |
| `/orders/` | `order_list` | Мои заказы (защищено) |
| `/buy/1/2/` | `create_order` | Создать заказ (защищено) |

## Шаг 9.2 — Подключение приложения к главному URLs

Открыть [back/urls.py](back/back/urls.py) и убедиться что приложение подключено:

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',       include('bodies.urls')),  # 👈 Подключить приложение
]
```

## Шаг 9.3 — Проверка маршрутов

```bash
# Просмотреть все доступные маршруты
python manage.py show_urls
```

**Результат:**
```
/                         product_list
/register/                register_view
/login/                   login_view
/logout/                  logout_view
/orders/                  order_list
/buy/<product_id>/<point_id>/  create_order
/admin/                   admin site
```

---

# 🔟 Проверка и тестирование

## Шаг 10.1 — Запуск сервера

```bash
python manage.py runserver
```

**Результат:**
```
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```

## Шаг 10.2 — Проверка доступности страниц

В браузере открыть:

| URL | Что должно быть |
|-----|-----------------|
| `http://127.0.0.1:8000/` | Список товаров (может быть пусто) |
| `http://127.0.0.1:8000/register/` | Форма регистрации |
| `http://127.0.0.1:8000/login/` | Форма входа |
| `http://127.0.0.1:8000/admin/` | Логин в админ-панель |

## Шаг 10.3 — Вход в админ-панель

1. Открыть `http://127.0.0.1:8000/admin/`
2. Username: `admin`
3. Password: (пароль суперпользователя)
4. Нажать **Sign in**

## Шаг 10.4 — Добавление тестовых данных

В админ-панели:

1. **Пункты выдачи** → **Add Pickup Point**
   ```
   Address: ул. Пушкина, д. 1, Москва
   ```
   Нажать **Save**

2. **Товары** → **Add Product**
   ```
   Name: iPhone 15
   Price: 99999.99
   SKU: SKU001
   Description: Смартфон Apple
   ```
   Нажать **Save**

3. **Товары** → **Add Product** (ещё один)
   ```
   Name: Samsung Galaxy
   Price: 79999.99
   SKU: SKU002
   Description: Смартфон Samsung
   ```
   Нажать **Save**

## Шаг 10.5 — Проверка перечисления товаров

Открыть `http://127.0.0.1:8000/` — должны видеть добавленные товары.

## Шаг 10.6 — Проверка регистрации и заказов

1. Нажать **Register**
2. Создать аккаунт (username, password)
3. Войти с новым аккаунтом
4. Нажать на товар (или создать заказ, если реализовано)
5. Перейти в **Мои заказы** — должен появиться новый заказ

---

## 🔍 Дополнительная проверка через Django Shell

```bash
python manage.py shell
```

```python
# Проверить товары
from bodies.models import Product
products = Product.objects.all()
for p in products:
    print(f"'{p.name}' ({p.sku}) - {p.price} руб.")

# Проверить пункты выдачи
from bodies.models import PickupPoint
points = PickupPoint.objects.all()
for p in points:
    print(f"{p.address}")

# Проверить заказы
from bodies.models import Order
orders = Order.objects.all()
for o in orders:
    print(f"Заказ #{o.id}: товары = {o.get_skus()}, код = {o.receiveCode}")

# Выход
exit()
```

---

## 🚨 Частые ошибки

### ❌ `django.db.utils.ProgrammingError: relation "bodies_product" does not exist`

**Причина:** Миграции не были применены или БД не создана

**Решение:**
```bash
python manage.py makemigrations
python manage.py migrate
```

### ❌ `django.core.exceptions.ImproperlyConfigured: Requested setting DATABASES`

**Причина:** PostgreSQL не установлен или не запущен

**Решение:** Убедиться что PostgreSQL запущен, и параметры в settings.py верные

### ❌ `no module named 'psycopg2'`

**Причина:** Не установлена библиотека

**Решение:**
```bash
pip install psycopg2-binary
```

### ❌ Все заказы получают один и тот же код получения

**Причина:** В моделе написано `default=generate_receive_code()` вместо `default=generate_receive_code`

**Решение:** Убрать скобки в models.py

---

## ✅ Финальный чеклист

- [ ] Виртуальное окружение активировано: `(venv)` в начале строки
- [ ] Django установлен: `python -m django --version`
- [ ] PostgreSQL установлен и запущен
- [ ] База `shop` создана в PostgreSQL
- [ ] `settings.py` настроен на PostgreSQL
- [ ] `bodies` добавлен в `INSTALLED_APPS`
- [ ] `models.py` содержит все 4 модели (Product, PickupPoint, Order, Profile)
- [ ] Созданы миграции: `makemigrations` выполнена
- [ ] Миграции применены: `migrate` выполнена
- [ ] Таблицы видны в DBeaver (F5 для обновления)
- [ ] Суперпользователь создан: `createsuperuser`
- [ ] `admin.py` регистрирует все модели
- [ ] `bodies/urls.py` создан и содержит маршруты
- [ ] `back/urls.py` подключает `bodies.urls`
- [ ] Сервер запускается: `runserver` без ошибок
- [ ] Админ-панель доступна и работает

Если все пункты отмечены ✅ — проект готов к разработке!

---

**Создано для демонстрационного экзамена ИРПО**
