# 📝 Какие Python файлы создать и какие обновить

Полный список всех Python файлов, которые нужны для проекта, разделенные на две категории.

---

## 📂 Структура после выполнения

```
back/
├── back/                          # Папка конфигурации (создается Django)
│   ├── __init__.py               # ❌ Не трогать
│   ├── settings.py               # ✏️ ОБНОВИТЬ
│   ├── urls.py                   # ✏️ ОБНОВИТЬ
│   ├── asgi.py                   # ❌ Не трогать
│   └── wsgi.py                   # ❌ Не трогать
│
├── bodies/                        # Папка приложения (создается Django)
│   ├── migrations/               # Папка миграций (создается Django)
│   │   ├── __init__.py           # ❌ Не трогать
│   │   └── 0001_initial.py       # 🤖 Создается автоматически (makemigrations)
│   │
│   ├── management/               # 📁 СОЗДАТЬ ПАПКУ
│   │   ├── __init__.py           # 📄 СОЗДАТЬ пустой файл
│   │   └── commands/             # 📁 СОЗДАТЬ ПАПКУ
│   │       ├── __init__.py       # 📄 СОЗДАТЬ пустой файл
│   │       └── import_products.py # 📄 СОЗДАТЬ и написать код
│   │
│   ├── templates/                # 📁 СОЗДАТЬ ПАПКУ
│   │   ├── products.html         # 📄 СОЗДАТЬ HTML
│   │   ├── login.html            # 📄 СОЗДАТЬ HTML
│   │   ├── register.html         # 📄 СОЗДАТЬ HTML
│   │   └── order_list.html       # 📄 СОЗДАТЬ HTML
│   │
│   ├── __init__.py               # ❌ Не трогать
│   ├── admin.py                  # ✏️ ОБНОВИТЬ
│   ├── apps.py                   # ❌ Не трогать
│   ├── models.py                 # ✏️ ОБНОВИТЬ
│   ├── tests.py                  # ❌ Не трогать (опционально)
│   ├── views.py                  # ✏️ ОБНОВИТЬ
│   └── urls.py                   # 📄 СОЗДАТЬ
│
├── manage.py                      # ❌ Не трогать
├── db.sqlite3                     # 🗄️ БД (создается автоматически, заменить на PostgreSQL)
├── venv/                          # Виртуальное окружение (создается автоматически)
└── README.md                      # 📄 СОЗДАТЬ (опционально, документация)
```

---

## 🟢 СОЗДАТЬ НОВЫЕ ФАЙЛЫ (не существуют в Django)

### 1. **bodies/urls.py** ➕ СОЗДАТЬ

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
]
```

**Где:** `d:\Test_Django_1\back\bodies\urls.py`  
**Действие:** Новый файл  
**Строк кода:** ~10

---

### 2. **bodies/management/__init__.py** ➕ СОЗДАТЬ

```python
# Пустой файл - нужен только для того, чтобы Python распознал папку как пакет
```

**Где:** `d:\Test_Django_1\back\bodies\management\__init__.py`  
**Действие:** Новый пустой файл  
**Строк кода:** 0 (пусто)

---

### 3. **bodies/management/commands/__init__.py** ➕ СОЗДАТЬ

```python
# Пустой файл - нужен только для того, чтобы Python распознал папку как пакет
```

**Где:** `d:\Test_Django_1\back\bodies\management\commands\__init__.py`  
**Действие:** Новый пустой файл  
**Строк кода:** 0 (пусто)

---

### 4. **bodies/management/commands/import_products.py** ➕ СОЗДАТЬ

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

**Где:** `d:\Test_Django_1\back\bodies\management\commands\import_products.py`  
**Действие:** Новый файл  
**Строк кода:** ~50  
**Использование:** `python manage.py import_products "path/to/file.xlsx"`

---

### 5. **bodies/templates/products.html** ➕ СОЗДАТЬ

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
        .container { max-width: 1000px; margin: 0 auto; }
        header { background: white; padding: 20px; border-radius: 5px; margin-bottom: 20px; }
        nav { margin: 10px 0; }
        nav a { margin-right: 15px; text-decoration: none; color: #007bff; }
        nav a:hover { text-decoration: underline; }
        .products { display: grid; grid-template-columns: repeat(auto-fill, minmax(250px, 1fr)); gap: 20px; }
        .product { background: white; padding: 15px; border-radius: 5px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }
        .product h3 { margin-bottom: 10px; color: #333; }
        .product p { color: #666; font-size: 14px; margin: 5px 0; }
        .price { font-size: 18px; font-weight: bold; color: #28a745; margin: 10px 0; }
        .empty { text-align: center; padding: 40px; color: #999; }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🛍️ Интернет-магазин</h1>
            <nav>
                {% if user.is_authenticated %}
                    <span>👤 {{ user.username }}</span> |
                    <a href="{% url 'order_list' %}">📦 Мои заказы</a> |
                    <a href="{% url 'logout' %}">🚪 Выход</a>
                {% else %}
                    <a href="{% url 'login' %}">🔓 Вход</a> |
                    <a href="{% url 'register' %}">✍️ Регистрация</a>
                {% endif %}
            </nav>
        </header>

        {% if products %}
            <div class="products">
                {% for product in products %}
                    <div class="product">
                        <h3>{{ product.name }}</h3>
                        <p><strong>Артикул:</strong> {{ product.sku }}</p>
                        <p>{{ product.description }}</p>
                        <div class="price">{{ product.price }} ₽</div>
                        {% if user.is_authenticated %}
                            <a href="{% url 'create_order' product.id 1 %}" style="display: inline-block; background: #007bff; color: white; padding: 8px 12px; border-radius: 3px; text-decoration: none; margin-top: 10px;">Заказать</a>
                        {% else %}
                            <p style="color: #999; font-size: 12px; margin-top: 10px;">Войдите, чтобы заказать</p>
                        {% endif %}
                    </div>
                {% endfor %}
            </div>
        {% else %}
            <div class="empty">
                <p>Товары не найдены</p>
                <p style="font-size: 12px; margin-top: 10px;">Добавьте товары через админ-панель: /admin/</p>
            </div>
        {% endif %}
    </div>
</body>
</html>
```

**Где:** `d:\Test_Django_1\back\bodies\templates\products.html`  
**Действие:** Новый файл  
**Строк кода:** ~70 (HTML)

---

### 6. **bodies/templates/login.html** ➕ СОЗДАТЬ

```html
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Вход</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: Arial; background: #f5f5f5; display: flex; justify-content: center; align-items: center; min-height: 100vh; }
        .form-container { background: white; padding: 30px; border-radius: 5px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); width: 100%; max-width: 400px; }
        h1 { text-align: center; margin-bottom: 20px; color: #333; }
        form { display: flex; flex-direction: column; }
        label { margin-top: 15px; font-weight: bold; color: #333; }
        input, textarea { padding: 10px; margin-top: 5px; border: 1px solid #ddd; border-radius: 3px; font-size: 14px; }
        input:focus { outline: none; border-color: #007bff; }
        button { margin-top: 20px; padding: 10px; background: #007bff; color: white; border: none; border-radius: 3px; cursor: pointer; font-size: 16px; }
        button:hover { background: #0056b3; }
        .link { text-align: center; margin-top: 15px; }
        .link a { color: #007bff; text-decoration: none; }
        .error { color: red; font-size: 12px; margin-top: 5px; }
    </style>
</head>
<body>
    <div class="form-container">
        <h1>🔓 Вход</h1>
        <form method="post">
            {% csrf_token %}
            {{ form.as_p }}
            <button type="submit">Войти</button>
        </form>
        <div class="link">
            Нет аккаунта? <a href="{% url 'register' %}">Зарегистрируйтесь</a>
        </div>
    </div>
</body>
</html>
```

**Где:** `d:\Test_Django_1\back\bodies\templates\login.html`  
**Действие:** Новый файл  
**Строк кода:** ~50 (HTML)

---

### 7. **bodies/templates/register.html** ➕ СОЗДАТЬ

```html
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Регистрация</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: Arial; background: #f5f5f5; display: flex; justify-content: center; align-items: center; min-height: 100vh; }
        .form-container { background: white; padding: 30px; border-radius: 5px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); width: 100%; max-width: 400px; }
        h1 { text-align: center; margin-bottom: 20px; color: #333; }
        form { display: flex; flex-direction: column; }
        label { margin-top: 15px; font-weight: bold; color: #333; }
        input, textarea { padding: 10px; margin-top: 5px; border: 1px solid #ddd; border-radius: 3px; font-size: 14px; }
        input:focus { outline: none; border-color: #007bff; }
        button { margin-top: 20px; padding: 10px; background: #28a745; color: white; border: none; border-radius: 3px; cursor: pointer; font-size: 16px; }
        button:hover { background: #218838; }
        .link { text-align: center; margin-top: 15px; }
        .link a { color: #007bff; text-decoration: none; }
        .help-text { font-size: 12px; color: #999; margin-top: 5px; }
    </style>
</head>
<body>
    <div class="form-container">
        <h1>✍️ Регистрация</h1>
        <form method="post">
            {% csrf_token %}
            {{ form.as_p }}
            <button type="submit">Зарегистрироваться</button>
        </form>
        <div class="link">
            Уже есть аккаунт? <a href="{% url 'login' %}">Войдите</a>
        </div>
    </div>
</body>
</html>
```

**Где:** `d:\Test_Django_1\back\bodies\templates\register.html`  
**Действие:** Новый файл  
**Строк кода:** ~50 (HTML)

---

### 8. **bodies/templates/order_list.html** ➕ СОЗДАТЬ

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
        .container { max-width: 1000px; margin: 0 auto; }
        header { background: white; padding: 20px; border-radius: 5px; margin-bottom: 20px; }
        nav { margin: 10px 0; }
        nav a { margin-right: 15px; text-decoration: none; color: #007bff; }
        nav a:hover { text-decoration: underline; }
        table { width: 100%; border-collapse: collapse; background: white; border-radius: 5px; overflow: hidden; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }
        th, td { padding: 15px; text-align: left; border-bottom: 1px solid #ddd; }
        th { background: #f0f0f0; font-weight: bold; }
        tr:hover { background: #f9f9f9; }
        .empty { text-align: center; padding: 40px; color: #999; }
        .badge { padding: 5px 10px; border-radius: 3px; font-size: 12px; }
        .badge-new { background: #ffc107; color: white; }
        .badge-delivered { background: #28a745; color: white; }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>📦 Мои заказы</h1>
            <nav>
                <a href="{% url 'product_list' %}">← Назад в каталог</a> |
                <span>👤 {{ user.username }}</span> |
                <a href="{% url 'logout' %}">🚪 Выход</a>
            </nav>
        </header>

        {% if orders %}
            <table>
                <thead>
                    <tr>
                        <th>№ Заказа</th>
                        <th>Товары</th>
                        <th>Дата заказа</th>
                        <th>Статус</th>
                        <th>Пункт выдачи</th>
                        <th>Код получения</th>
                    </tr>
                </thead>
                <tbody>
                    {% for order in orders %}
                    <tr>
                        <td>#{{ order.id }}</td>
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
                        <td><strong>{{ order.receiveCode }}</strong></td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        {% else %}
            <div class="empty">
                <p>У вас нет заказов</p>
                <p><a href="{% url 'product_list' %}">← Перейти в каталог</a></p>
            </div>
        {% endif %}
    </div>
</body>
</html>
```

**Где:** `d:\Test_Django_1\back\bodies\templates\order_list.html`  
**Действие:** Новый файл  
**Строк кода:** ~80 (HTML)

---

## 🔵 ОБНОВИТЬ СУЩЕСТВУЮЩИЕ ФАЙЛЫ (изменить содержимое)

### 1. **back/settings.py** ✏️ ОБНОВИТЬ

**Что изменить:**

#### Пункт 1: INSTALLED_APPS (строка ~33)

Добавить `'bodies'` в конец списка:

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    'bodies',  # ← ДОБАВИТЬ
]
```

#### Пункт 2: DATABASES (строка ~78)

Заменить весь блок DATABASES:

```python
# ❌ БЫЛО
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# ✅ СТАЛО
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
```

**Где:** `d:\Test_Django_1\back\back\settings.py`  
**Строк для изменения:** 2 блока (~6 строк итого)  
**Сложность:** ⭐ Очень просто

---

### 2. **back/urls.py** ✏️ ОБНОВИТЬ

**Что изменить:**

Заменить весь файл:

```python
# ❌ БЫЛО
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
]

# ✅ СТАЛО
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',       include('bodies.urls')),  # ← ДОБАВИТЬ
]
```

**Где:** `d:\Test_Django_1\back\back\urls.py`  
**Строк для изменения:** 1 импорт + 1 маршрут (~3 строки)  
**Сложность:** ⭐ Очень просто

---

### 3. **bodies/models.py** ✏️ ОБНОВИТЬ

**Что изменить:**

Заменить весь файл на полный код всех 4 моделей:

```python
import random
import string
from django.db import models
from django.contrib.auth.models import User


def generate_receive_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))


class Product(models.Model):
    name        = models.CharField(max_length=255, verbose_name="Название товара")
    price       = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена (руб.)")
    description = models.TextField(blank=True, verbose_name="Описание товара")
    sku         = models.CharField(max_length=50, unique=True, verbose_name="Артикул")

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

    def __str__(self):
        return f"{self.name} ({self.sku})"


class PickupPoint(models.Model):
    address = models.CharField(max_length=500, verbose_name="Адрес пункта выдачи")

    class Meta:
        verbose_name = "Пункт выдачи"
        verbose_name_plural = "Пункты выдачи"

    def __str__(self):
        return self.address


class Order(models.Model):
    STATUS_CHOICES = [('new', 'Новый'), ('delivered', 'Завершен')]
    
    user         = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    products     = models.ManyToManyField(Product)
    createdAt    = models.DateTimeField(auto_now_add=True)
    deliveryDate = models.DateTimeField(null=True, blank=True)
    receiveCode  = models.CharField(max_length=10, default=generate_receive_code)
    pickupPoint  = models.ForeignKey(PickupPoint, on_delete=models.SET_NULL, null=True)
    status       = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')

    def __str__(self):
        user_name = self.user.get_full_name() or self.user.username
        return f"Заказ #{self.id} - {user_name}"
    
    def get_skus(self):
        return ', '.join([p.sku for p in self.products.all()])


class Profile(models.Model):
    ROLE_CHOICES = [('admin', 'Администратор'), ('manager', 'Менеджер'), ('customer', 'Покупатель')]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='customer')

    def __str__(self):
        return f"{self.user.username} ({self.get_role_display()})"
```

**Где:** `d:\Test_Django_1\back\bodies\models.py`  
**Строк для изменения:** Весь файл (~80 строк)  
**Сложность:** ⭐⭐ Средняя

---

### 4. **bodies/views.py** ✏️ ОБНОВИТЬ

**Что изменить:**

Заменить весь файл:

```python
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .models import Product, PickupPoint, Order


def product_list(request):
    products = Product.objects.all()
    return render(request, 'products.html', {'products': products})


def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('product_list')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        from django.contrib.auth import authenticate
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('product_list')
    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('product_list')


@login_required(login_url='login')
def order_list(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'order_list.html', {'orders': orders})


@login_required(login_url='login')
def create_order(request, product_id, pickup_point_id):
    product      = get_object_or_404(Product, id=product_id)
    pickup_point = get_object_or_404(PickupPoint, id=pickup_point_id)
    order = Order.objects.create(user=request.user, pickupPoint=pickup_point)
    order.products.add(product)
    return redirect('order_list')
```

**Где:** `d:\Test_Django_1\back\bodies\views.py`  
**Строк для изменения:** Весь файл (~60 строк)  
**Сложность:** ⭐⭐ Средняя

---

### 5. **bodies/admin.py** ✏️ ОБНОВИТЬ

**Что изменить:**

Заменить весь файл:

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

**Где:** `d:\Test_Django_1\back\bodies\admin.py`  
**Строк для изменения:** Весь файл (~30 строк)  
**Сложность:** ⭐⭐ Средняя

---

## 📊 Итоговая таблица

| # | Файл | Действие | Строк | Сложность |
|---|------|----------|-------|-----------|
| 1 | `back/settings.py` | ✏️ Обновить | 2 блока (~6 строк) | ⭐ |
| 2 | `back/urls.py` | ✏️ Обновить | 1 импорт + 1 маршрут | ⭐ |
| 3 | `bodies/models.py` | ✏️ Обновить | Весь файл (~80 строк) | ⭐⭐ |
| 4 | `bodies/views.py` | ✏️ Обновить | Весь файл (~60 строк) | ⭐⭐ |
| 5 | `bodies/admin.py` | ✏️ Обновить | Весь файл (~30 строк) | ⭐⭐ |
| 6 | `bodies/urls.py` | 📄 Создать | ~10 строк | ⭐ |
| 7 | `bodies/management/__init__.py` | 📄 Создать пусто | 0 строк | ⭐ |
| 8 | `bodies/management/commands/__init__.py` | 📄 Создать пусто | 0 строк | ⭐ |
| 9 | `bodies/management/commands/import_products.py` | 📄 Создать | ~50 строк | ⭐⭐ |
| 10 | `bodies/templates/products.html` | 📄 Создать | ~70 строк | ⭐⭐ |
| 11 | `bodies/templates/login.html` | 📄 Создать | ~50 строк | ⭐ |
| 12 | `bodies/templates/register.html` | 📄 Создать | ~50 строк | ⭐ |
| 13 | `bodies/templates/order_list.html` | 📄 Создать | ~80 строк | ⭐⭐ |

---

## ⏱️ Примерное время

- **Обновить 5 файлов:** 30-40 минут
- **Создать 8 файлов:** 40-50 минут
- **Всего:** ~1.5 часа на написание кода

---

## 🔄 Порядок выполнения (важно!)

1. **Сначала обновить:**
   - `back/settings.py` (Database + INSTALLED_APPS)
   - `back/urls.py` (include bodies.urls)

2. **Потом создать модели:**
   - `bodies/models.py` (обновить)
   - Запустить `makemigrations` + `migrate`

3. **Потом остальное:**
   - `bodies/admin.py` (обновить)
   - `bodies/urls.py` (создать)
   - `bodies/views.py` (обновить)
   - `bodies/templates/**` (создать 4 HTML файла)
   - `bodies/management/` (создать команду import)

4. **Проверка:**
   - `python manage.py check`
   - `python manage.py runserver`

---

Файл находится в: **`d:\Test_Django_1\back\FILES_GUIDE.md`**
