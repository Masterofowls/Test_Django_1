# Django Models & SQL

Django ORM заменяет написание SQL вручную. Вы описываете таблицы как Python-классы, а Django сам генерирует SQL.

---

## Как модель превращается в таблицу

```python
# models.py
class Product(models.Model):
    name  = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    sku   = models.CharField(max_length=50, unique=True)
```

Django выполнит:

```sql
CREATE TABLE bodies_product (
    id    INTEGER PRIMARY KEY AUTOINCREMENT,
    name  VARCHAR(255) NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    sku   VARCHAR(50) NOT NULL UNIQUE
);
```

> `id` создается автоматически. Имя таблицы = `<app>_<model>` (например `bodies_product`).

---

## Типы полей → типы колонок SQL

| Django                          | SQL                  | Пример                    |
|---------------------------------|----------------------|---------------------------|
| `CharField(max_length=N)`       | `VARCHAR(N)`         | Название, артикул         |
| `TextField()`                   | `TEXT`               | Описание                  |
| `IntegerField()`                | `INTEGER`            | Количество                |
| `DecimalField(max_digits, ...)`  | `DECIMAL(M,N)`       | Цена                      |
| `BooleanField()`                | `BOOLEAN`            | Активен/неактивен         |
| `DateTimeField()`               | `DATETIME`           | Дата создания             |
| `ImageField()`                  | `VARCHAR(100)`       | Путь к файлу              |

Параметры полей:

| Параметр       | SQL эквивалент          |
|----------------|-------------------------|
| `unique=True`  | `UNIQUE`                |
| `null=True`    | убирает `NOT NULL`      |
| `blank=True`   | только Django (не SQL)  |
| `default=...`  | `DEFAULT ...`           |

---

## Связи между таблицами

### ForeignKey — один ко многим

Один пользователь → много заказов.

```python
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
```

SQL:

```sql
CREATE TABLE bodies_order (
    id      INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES auth_user(id) ON DELETE CASCADE
);
```

Параметры `on_delete`:

| Значение         | SQL                | Что делает                          |
|------------------|--------------------|-------------------------------------|
| `CASCADE`        | `ON DELETE CASCADE`| Удаляет заказы при удалении юзера   |
| `SET_NULL`       | `ON DELETE SET NULL`| Ставит NULL (нужен `null=True`)    |
| `PROTECT`        | нет аналога        | Запрещает удаление                  |

### OneToOneField — один к одному

Один пользователь → один профиль.

```python
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, default='authorized')
```

SQL:

```sql
CREATE TABLE bodies_profile (
    id      INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL UNIQUE REFERENCES auth_user(id) ON DELETE CASCADE,
    role    VARCHAR(20) NOT NULL DEFAULT 'authorized'
);
```

### ManyToManyField — многие ко многим

Один заказ → много товаров. Один товар → в нескольких заказах.

```python
class Order(models.Model):
    products = models.ManyToManyField(Product)
```

Django создает промежуточную таблицу:

```sql
CREATE TABLE bodies_order_products (
    id         INTEGER PRIMARY KEY,
    order_id   INTEGER NOT NULL REFERENCES bodies_order(id),
    product_id INTEGER NOT NULL REFERENCES bodies_product(id),
    UNIQUE (order_id, product_id)
);
```

---

## Полная схема проекта

```
auth_user (встроенная Django)
    ├── id, username, password, email, ...
    │
    ├──── bodies_profile (OneToOne)
    │         ├── user_id → auth_user.id
    │         └── role
    │
    └──── bodies_order (ForeignKey)
              ├── user_id → auth_user.id
              ├── pickupPoint_id → bodies_pickuppoint.id
              ├── status, createdAt, receiveCode
              │
              └──── bodies_order_products (ManyToMany)
                        ├── order_id → bodies_order.id
                        └── product_id → bodies_product.id

bodies_product
    ├── id, name, price, description, sku, image

bodies_pickuppoint
    ├── id, address
```

---

## Создание таблиц

```bash
# 1. Создать файлы миграций из models.py
python manage.py makemigrations

# 2. Применить миграции (выполнить SQL)
python manage.py migrate

# 3. Посмотреть какой SQL будет выполнен
python manage.py sqlmigrate bodies 0001
```

---

## ORM запросы → SQL

### Получить все товары

```python
Product.objects.all()
```
```sql
SELECT * FROM bodies_product;
```

### Фильтрация

```python
Product.objects.filter(price__gte=1000, price__lte=5000)
```
```sql
SELECT * FROM bodies_product WHERE price >= 1000 AND price <= 5000;
```

### Поиск по тексту

```python
Product.objects.filter(name__icontains='кроссовки')
```
```sql
SELECT * FROM bodies_product WHERE LOWER(name) LIKE '%кроссовки%';
```

### Создание

```python
Product.objects.create(name='Ботинки', sku='BOOT-001', price=3000)
```
```sql
INSERT INTO bodies_product (name, sku, price, description) VALUES ('Ботинки', 'BOOT-001', 3000, '');
```

### Обновление или создание

```python
Product.objects.update_or_create(
    sku='BOOT-001',
    defaults={'name': 'Ботинки', 'price': 3500}
)
```
```sql
-- Если существует:
UPDATE bodies_product SET name='Ботинки', price=3500 WHERE sku='BOOT-001';
-- Если нет:
INSERT INTO bodies_product (name, sku, price) VALUES ('Ботинки', 'BOOT-001', 3500);
```

### Удаление

```python
Product.objects.filter(sku='BOOT-001').delete()
```
```sql
DELETE FROM bodies_product WHERE sku='BOOT-001';
```

### Связанные данные

```python
# Заказы пользователя
Order.objects.filter(user=request.user)

# Товары в заказе
order.products.all()

# Добавить товар в заказ
order.products.add(product)
```
```sql
SELECT * FROM bodies_order WHERE user_id = 1;

SELECT p.* FROM bodies_product p
JOIN bodies_order_products op ON p.id = op.product_id
WHERE op.order_id = 1;

INSERT INTO bodies_order_products (order_id, product_id) VALUES (1, 5);
```

---

## Raw SQL в Django

Если нужен чистый SQL:

```python
# Через модель
products = Product.objects.raw('SELECT * FROM bodies_product WHERE price > %s', [1000])

# Через курсор
from django.db import connection
with connection.cursor() as cursor:
    cursor.execute('SELECT COUNT(*) FROM bodies_product')
    count = cursor.fetchone()[0]
```
