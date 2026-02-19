# 🗄️ Полная инструкция SQL и работа с PostgreSQL

Подробное руководство по созданию и управлению базой данных PostgreSQL для Django проекта.

---

## 📋 Содержание

1. [Установка PostgreSQL](#установка-postgresql)
2. [Создание базы данных](#создание-базы-данных)
3. [Подключение из Django](#подключение-из-django)
4. [Создание таблиц (миграции)](#создание-таблиц-миграции)
5. [Структура таблиц](#структура-таблиц)
6. [SQL команды для работы](#sql-команды-для-работы)
7. [Импорт данных](#импорт-данных)
8. [Работа в DBeaver](#работа-в-dbeaver)
9. [Резервная копия и восстановление](#резервная-копия-и-восстановление)
10. [Очистка БД](#очистка-бд)

---

# 1️⃣ Установка PostgreSQL

## Вариант 1: Windows (рекомендуется)

### Шаг 1.1 — Скачать установщик

1. Перейти на https://www.postgresql.org/download/windows/
2. Скачать последнюю версию (например, PostgreSQL 15)
3. Запустить `postgresql-15-x64-setup.exe`

### Шаг 1.2 — Установка

1. **Setup Wizard** → **Next**
2. **Installation Directory** → оставить по умолчанию → **Next**
3. **Password** для пользователя `postgres`:
   ```
   Password: postgres
   ```
   ⚠️ **Это пароль администратора БД!** Запомнить!

4. **Port**: `5432` (оставить по умолчанию) → **Next**
5. **Locale**: выбрать язык → **Next**
6. **Pre Installation Summary** → **Next**
7. **Setup Complete** → ✅ **Finish**

### Шаг 1.3 — Проверка установки

Открыть **PowerShell** и выполнить:

```bash
psql --version
# Output: psql (PostgreSQL) 15.0
```

### Шаг 1.4 — Проверка сервера

```bash
# Подключиться к базе (введёт пароль)
psql -U postgres

# Если успешно, откроется консоль PostgreSQL
postgres=#
```

Выход из консоли:
```sql
\q
```

---

## Вариант 2: Linux (Debian/Ubuntu)

```bash
# Установка
sudo apt update
sudo apt install postgresql postgresql-contrib

# Проверка
psql --version

# Запуск сервиса
sudo systemctl start postgresql
sudo systemctl enable postgresql

# Подключение
sudo -u postgres psql
```

---

## Вариант 3: macOS

```bash
# Через Homebrew
brew install postgresql

# Запуск
brew services start postgresql

# Проверка
psql --version
```

---

# 2️⃣ Создание базы данных

## Способ 1: Через DBeaver (на экзамене)

### Шаг 2.1 — Открыть DBeaver

Установить DBeaver (если ещё нет):
```
https://dbeaver.io/download/
```

### Шаг 2.2 — Создать подключение

1. Открыть **DBeaver**
2. **Database** → **New Connection**
3. Выбрать **PostgreSQL** → **Next**

### Шаг 2.3 — Параметры подключения

Заполнить форму:

```
Server Host:     localhost
Port:            5432
Database:        postgres      (по умолчанию)
Username:        postgres
Password:        postgres      (пароль, введённый при установке)
Save password:   ✓ (галочка)
```

Нажать **Test Connection** — должно сказать **Connected**.

### Шаг 2.4 — Создать новую БД

1. В левой панели раскрыть подключение
2. Раскрыть **Databases**
3. ПКМ на **postgres** → **Create** → **Database**

### Шаг 2.5 — Параметры БД

```
Database Name:    shop
Owner:            postgres
Encoding:         UTF8
Collation:        (оставить пусто)
Character Type:   (оставить пусто)
```

Нажать **OK**

**Результат:** В списке появилась база `shop`

---

## Способ 2: Через командную строку (PowerShell)

```bash
# Подключиться к базе postgres (введёт пароль)
psql -U postgres

# Введёт пароль: postgres
# Откроется консоль PostgreSQL

postgres=# CREATE DATABASE shop;
# Output: CREATE DATABASE

postgres=# \l
# Должна отобразиться база "shop"

postgres=# \q
# Выход
```

---

## Способ 3: Через Python + psycopg2

```bash
# Установить драйвер (на случай если не установлен)
pip install psycopg2-binary

# Создать Python скрипт (create_db.py)
```

`create_db.py`:
```python
import psycopg2
from psycopg2 import sql

# Подключиться к базе postgres
conn = psycopg2.connect(
    host='localhost',
    port='5432',
    user='postgres',
    password='postgres',
    database='postgres'  # Подключаемся к системной БД
)

# Создать новую БД
conn.autocommit = True
cursor = conn.cursor()

try:
    cursor.execute('CREATE DATABASE shop;')
    print('✅ База shop создана успешно')
except psycopg2.Error as e:
    print(f'❌ Ошибка: {e}')
finally:
    cursor.close()
    conn.close()
```

Запустить:
```bash
python create_db.py
```

---

# 3️⃣ Подключение из Django

## Шаг 3.1 — Установка драйвера

```bash
pip install psycopg2-binary
```

## Шаг 3.2 — Настройка settings.py

Открыть `back/settings.py` и найти блок `DATABASES`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',  # ← Важно!
        'NAME': 'shop',                             # Имя БД
        'USER': 'postgres',                         # Пользователь
        'PASSWORD': 'postgres',                     # Пароль
        'HOST': 'localhost',                        # Сервер
        'PORT': '5432',                             # Порт
    }
}
```

## Шаг 3.3 — Проверка подключения

```bash
python manage.py dbshell
```

Откроется консоль PostgreSQL если подключение успешно:

```sql
shop=# \dt
# Отобразит таблицы (пусто на начальном этапе)

shop=# \q
# Выход
```

---

# 4️⃣ Создание таблиц (миграции)

## Шаг 4.1 — Создание миграций

После того как модели написаны в `models.py`:

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

Это создаст файл с инструкциями для БД.

## Шаг 4.2 — Применение миграций

```bash
python manage.py migrate
```

**Результат:**
```
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, sessions, bodies
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  Applying bodies.0001_initial... OK
  ...
```

## Шаг 4.3 — Проверка таблиц в DBeaver

1. Открыть DBeaver
2. Раскрыть подключение → **Databases** → **shop** → **Schemas** → **public** → **Tables**
3. Должны быть таблицы:
   ```
   auth_group
   auth_permission
   auth_user
   auth_user_groups
   bodies_order                    ← Наша таблица
   bodies_order_products           ← ManyToMany связь
   bodies_pickuppoint              ← Наша таблица
   bodies_product                  ← Наша таблица
   bodies_profile                  ← Наша таблица
   django_admin_log
   django_content_type
   django_migrations
   django_session
   ```

---

# 5️⃣ Структура таблиц

## Таблица: bodies_product

| Колонка | Тип | Ограничения | Описание |
|---------|-----|------------|---------|
| id | INTEGER | PRIMARY KEY, AUTO INCREMENT | Уникальный ID товара |
| name | VARCHAR(255) | NOT NULL | Название товара |
| price | NUMERIC(10,2) | NOT NULL | Цена в рублях |
| description | TEXT | NULLABLE | Описание товара |
| sku | VARCHAR(50) | UNIQUE, NOT NULL | Артикул товара |

**SQL для просмотра:**
```sql
\d bodies_product
```

**Пример данных:**
```sql
INSERT INTO bodies_product (name, price, sku, description) VALUES
('iPhone 15', 99999.99, 'SKU001', 'Смартфон Apple'),
('Samsung Galaxy', 79999.99, 'SKU002', 'Смартфон Samsung');
```

---

## Таблица: bodies_pickuppoint

| Колонка | Тип | Ограничения | Описание |
|---------|-----|------------|---------|
| id | INTEGER | PRIMARY KEY, AUTO INCREMENT | Уникальный ID пункта |
| address | VARCHAR(500) | NOT NULL | Адрес пункта выдачи |

**SQL для просмотра:**
```sql
\d bodies_pickuppoint
```

**Пример данных:**
```sql
INSERT INTO bodies_pickuppoint (address) VALUES
('ул. Пушкина, д. 1, Москва'),
('ул. Лермонтова, д. 5, Санкт-Петербург');
```

---

## Таблица: bodies_order

| Колонка | Тип | Ограничения | Описание |
|---------|-----|------------|---------|
| id | INTEGER | PRIMARY KEY, AUTO INCREMENT | Уникальный ID заказа |
| user_id | INTEGER | FOREIGN KEY(auth_user) | ID пользователя |
| pickuppoint_id | INTEGER | FOREIGN KEY(bodies_pickuppoint) | ID пункта выдачи |
| createdAt | TIMESTAMP | NOT NULL | Дата создания заказа |
| deliveryDate | TIMESTAMP | NULLABLE | Дата доставки |
| receiveCode | VARCHAR(10) | NOT NULL | Код получения заказа |
| status | VARCHAR(20) | DEFAULT 'new' | Статус (new/delivered) |

**SQL для просмотра:**
```sql
\d bodies_order
```

---

## Таблица: bodies_order_products (ManyToMany)

| Колонка | Тип | Ограничения | Описание |
|---------|-----|------------|---------|
| id | INTEGER | PRIMARY KEY | Уникальный ID связи |
| order_id | INTEGER | FOREIGN KEY(bodies_order) | ID заказа |
| product_id | INTEGER | FOREIGN KEY(bodies_product) | ID товара |

Это связующая таблица для связи "много-ко-многим".

**Пример:** Один заказ может содержать несколько товаров.

---

## Таблица: bodies_profile

| Колонка | Тип | Ограничения | Описание |
|---------|-----|------------|---------|
| id | INTEGER | PRIMARY KEY, AUTO INCREMENT | Уникальный ID профиля |
| user_id | INTEGER | FOREIGN KEY(auth_user), UNIQUE | ID пользователя |
| role | VARCHAR(20) | DEFAULT 'customer' | Роль (admin/manager/customer) |

**SQL для просмотра:**
```sql
\d bodies_profile
```

---

# 6️⃣ SQL команды для работы

## Подключение к БД

```bash
# Подключиться к БД shop
psql -U postgres -d shop -h localhost

# В консоли PostgreSQL
shop=#
```

---

## Просмотр информации

```sql
-- Список всех БД
\l

-- Список всех таблиц в текущей БД
\dt

-- Структура таблицы
\d bodies_product

-- Список колонок таблицы
\d+ bodies_product

-- Список индексов
\di

-- Выход
\q
```

---

## SELECT (Выборка данных)

```sql
-- Все товары
SELECT * FROM bodies_product;

-- Товары дороже 100000
SELECT name, price FROM bodies_product WHERE price > 100000;

-- Все заказы пользователя с ID 1
SELECT * FROM bodies_order WHERE user_id = 1;

-- Заказы со статусом 'new'
SELECT id, user_id, status, createdAt FROM bodies_order WHERE status = 'new';

-- Все пункты выдачи с адресом
SELECT id, address FROM bodies_pickuppoint;

-- Количество товаров в каждом заказе
SELECT order_id, COUNT(product_id) as product_count
FROM bodies_order_products
GROUP BY order_id;
```

---

## INSERT (Добавление данных)

```sql
-- Добавить товар
INSERT INTO bodies_product (name, price, sku, description)
VALUES ('iPhone 15', 99999.99, 'SKU001', 'Смартфон Apple');

-- Добавить несколько товаров
INSERT INTO bodies_product (name, price, sku, description) VALUES
('Samsung Galaxy', 79999.99, 'SKU002', 'Смартфон Samsung'),
('Xiaomi 13', 59999.99, 'SKU003', 'Смартфон Xiaomi');

-- Добавить пункт выдачи
INSERT INTO bodies_pickuppoint (address)
VALUES ('ул. Пушкина, д. 1, Москва');
```

---

## UPDATE (Изменение данных)

```sql
-- Изменить цену товара с ID 1
UPDATE bodies_product
SET price = 89999.99
WHERE id = 1;

-- Изменить статус заказа на 'delivered'
UPDATE bodies_order
SET status = 'delivered'
WHERE id = 1;

-- Изменить адрес пункта выдачи
UPDATE bodies_pickuppoint
SET address = 'ул. Пушкина, д. 2, Москва'
WHERE id = 1;
```

---

## DELETE (Удаление данных)

```sql
-- ⚠️ ОПАСНО! Удалить товар с ID 5
DELETE FROM bodies_product WHERE id = 5;

-- Удалить заказ с ID 1
DELETE FROM bodies_order WHERE id = 1;

-- Удалить все заказы со статусом 'new'
DELETE FROM bodies_order WHERE status = 'new';
```

---

## JOINS (Связывание таблиц)

```sql
-- Все заказы с информацией о пользователе
SELECT 
    o.id,
    u.username,
    o.status,
    o.createdAt
FROM bodies_order o
JOIN auth_user u ON o.user_id = u.id;

-- Все товары в заказе #1
SELECT 
    p.id,
    p.name,
    p.price
FROM bodies_product p
JOIN bodies_order_products op ON p.id = op.product_id
WHERE op.order_id = 1;

-- Полная информация о заказе
SELECT 
    o.id as order_id,
    u.username,
    p.name as product_name,
    pp.address,
    o.receiveCode,
    o.status,
    o.createdAt
FROM bodies_order o
JOIN auth_user u ON o.user_id = u.id
JOIN bodies_order_products op ON o.id = op.order_id
JOIN bodies_product p ON op.product_id = p.id
JOIN bodies_pickuppoint pp ON o.pickuppoint_id = pp.id;
```

---

## Подсчёты и агрегаты

```sql
-- Количество товаров в магазине
SELECT COUNT(*) FROM bodies_product;

-- Средняя цена товара
SELECT AVG(price) FROM bodies_product;

-- Максимальная цена
SELECT MAX(price) FROM bodies_product;

-- Минимальная цена
SELECT MIN(price) FROM bodies_product;

-- Общая сумма товаров
SELECT SUM(price) FROM bodies_product;

-- Количество заказов по статусам
SELECT status, COUNT(*) FROM bodies_order GROUP BY status;

-- Сколько товаров было заказано (всего во всех заказах)
SELECT COUNT(*) FROM bodies_order_products;
```

---

# 7️⃣ Импорт данных

## Вариант 1: Django Management Command (рекомендуется)

Используется файл `bodies/management/commands/import_products.py`

```bash
python manage.py import_products "C:\path\to\file.xlsx"
```

---

## Вариант 2: Через DBeaver (визуально)

1. Открыть DBeaver
2. ПКМ на таблицу `bodies_product` → **Import Data**
3. Выбрать файл `.xlsx` или `.csv`
4. Сопоставить колонки (name ↔ Наименование товара, price ↔ Цена и т.д.)
5. Нажать **Finish**

---

## Вариант 3: Через psql и CSV

Подготовить CSV файл (products.csv):
```csv
id,name,price,sku,description
1,iPhone 15,99999.99,SKU001,Смартфон Apple
2,Samsung Galaxy,79999.99,SKU002,Смартфон Samsung
```

Затем в консоли PostgreSQL:
```sql
COPY bodies_product (id, name, price, sku, description)
FROM '/path/to/products.csv'
WITH (FORMAT csv, HEADER, DELIMITER ',');
```

---

## Вариант 4: INSERT через Python

```python
import psycopg2

conn = psycopg2.connect(
    host='localhost',
    database='shop',
    user='postgres',
    password='postgres'
)

cursor = conn.cursor()

products = [
    ('iPhone 15', 99999.99, 'SKU001', 'Смартфон Apple'),
    ('Samsung Galaxy', 79999.99, 'SKU002', 'Смартфон Samsung'),
]

for name, price, sku, description in products:
    cursor.execute(
        'INSERT INTO bodies_product (name, price, sku, description) VALUES (%s, %s, %s, %s)',
        (name, price, sku, description)
    )

conn.commit()
cursor.close()
conn.close()

print('✅ Данные импортированы')
```

---

# 8️⃣ Работа в DBeaver

## Просмотр данных в таблице

1. Раскрыть **Databases** → **shop** → **Schemas** → **public** → **Tables**
2. Двойной клик на таблицу `bodies_product`
3. Откроется вкладка с данными

## Выполнение SQL запроса

1. **SQL Editor** → **New SQL Script** (или Ctrl+Alt+N)
2. Написать запрос:
   ```sql
   SELECT * FROM bodies_product;
   ```
3. Нажать **Execute** (Ctrl+Enter) или кнопка ▶️
4. Результат в нижней панели

## Редактирование данных

1. В таблице просто кликнуть на ячейку
2. Изменить значение
3. Нажать **Enter**
4. Автоматически сохранится

## Удаление записи

1. Клик правой кнопкой на строку
2. **Delete Row**
3. Подтвердить

---

# 9️⃣ Резервная копия и восстановление

## Создание резервной копии (Dump)

```bash
# Весь сервер
pg_dump -U postgres > backup.sql

# Конкретная БД
pg_dump -U postgres -d shop > shop_backup.sql

# С таблицей пароля
PGPASSWORD=postgres pg_dump -U postgres -h localhost -d shop > shop_backup.sql
```

## Восстановление из резервной копии

```bash
# Из дампа
psql -U postgres < backup.sql

# Конкретную БД
psql -U postgres -d shop < shop_backup.sql
```

---

# 🔟 Очистка БД

## Удалить все данные (но сохранить таблицы)

```sql
-- Удалить все заказы
DELETE FROM bodies_order;

-- Удалить все товары
DELETE FROM bodies_product;

-- Удалить все пункты выдачи
DELETE FROM bodies_pickuppoint;

-- Очистить счётчики ID (вернуть в начало)
ALTER SEQUENCE bodies_product_id_seq RESTART WITH 1;
ALTER SEQUENCE bodies_order_id_seq RESTART WITH 1;
```

## Удалить всю БД (опасно!)

```bash
# Через psql
psql -U postgres -c "DROP DATABASE shop;"

# Или в консоли PostgreSQL
dropdb -U postgres shop
```

## Пересоздать всю БД (нуль)

```bash
# 1. Удалить старую
python manage.py flush

# 2. Или через Django
python manage.py migrate zero bodies

# 3. Пересоздать
python manage.py makemigrations
python manage.py migrate
```

---

## ✅ Чеклист для экзамена

- [ ] PostgreSQL установлена и запущена
- [ ] База `shop` создана в PostgreSQL
- [ ] Параметры в `settings.py` совпадают с БД (логин, пароль, имя)
- [ ] Выполнена: `python manage.py makemigrations`
- [ ] Выполнена: `python manage.py migrate`
- [ ] Таблицы видны в DBeaver
- [ ] Структура таблиц правильная (колонки и типы)
- [ ] Добавлены тестовые данные (товары, пункты выдачи)
- [ ] SQL запросы выполняются в DBeaver
- [ ] Django может подключиться к БД: `python manage.py dbshell`

---

**Создано для демонстрационного экзамена ИРПО**
