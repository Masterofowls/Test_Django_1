# 📚 Подробное руководство по SQL для таблиц базы данных

## Общая информация
- **СУБД:** PostgreSQL
- **База данных:** `shop`
- **Подключение:** localhost:5432
- **Пользователь:** postgres / postgres

---

## 📊 Структура таблиц

### 1. **auth_user** (встроенная таблица Django)
Таблица пользователей системы.

```sql
-- Просмотр структуры
\d auth_user

-- Содержит колонки:
-- id (PRIMARY KEY)
-- username (VARCHAR, UNIQUE)
-- password (VARCHAR)
-- email (VARCHAR)
-- first_name (VARCHAR)
-- last_name (VARCHAR)
-- is_staff (BOOLEAN)
-- is_active (BOOLEAN)
-- date_joined (TIMESTAMP)
```

---

### 2. **bodies_product** 
Таблица товаров магазина.

```sql
CREATE TABLE bodies_product (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    price NUMERIC(10, 2) NOT NULL,
    description TEXT DEFAULT '',
    sku VARCHAR(50) NOT NULL UNIQUE
);

-- Индексы (создаются автоматически)
-- PRIMARY KEY: id
-- UNIQUE: sku
```

**Структура:**
| Колонка | Тип | Описание |
|---------|------|---------|
| id | BIGSERIAL | Уникальный идентификатор товара |
| name | VARCHAR(255) | Название товара |
| price | NUMERIC(10,2) | Цена в рублях (макс. 99999999.99) |
| description | TEXT | Описание товара (опционально) |
| sku | VARCHAR(50) | Артикул товара (уникален) |

---

### 3. **bodies_pickuppoint**
Таблица пунктов выдачи заказов.

```sql
CREATE TABLE bodies_pickuppoint (
    id BIGSERIAL PRIMARY KEY,
    address VARCHAR(500) NOT NULL
);
```

**Структура:**
| Колонка | Тип | Описание |
|---------|------|---------|
| id | BIGSERIAL | Уникальный идентификатор пункта |
| address | VARCHAR(500) | Адрес пункта выдачи |

---

### 4. **bodies_order**
Таблица заказов пользователей.

```sql
CREATE TABLE bodies_order (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL REFERENCES auth_user(id),
    createdAt TIMESTAMP NOT NULL,
    deliveryDate TIMESTAMP NULL,
    receiveCode VARCHAR(10) NOT NULL,
    pickupPoint_id BIGINT NULL REFERENCES bodies_pickuppoint(id),
    status VARCHAR(20) DEFAULT 'new' CHECK (status IN ('new', 'delivered'))
);

-- Внешние ключи:
-- user_id -> auth_user.id (CASCADE DELETE)
-- pickupPoint_id -> bodies_pickuppoint.id (SET NULL)
```

**Структура:**
| Колонка | Тип | Описание |
|---------|------|---------|
| id | BIGSERIAL | Уникальный идентификатор заказа |
| user_id | BIGINT | ID пользователя (внешний ключ) |
| createdAt | TIMESTAMP | Дата создания заказа |
| deliveryDate | TIMESTAMP | Дата доставки (опционально) |
| receiveCode | VARCHAR(10) | Код для получения заказа (6 символов) |
| pickupPoint_id | BIGINT | ID пункта выдачи (внешний ключ) |
| status | VARCHAR(20) | Статус: 'new' или 'delivered' |

---

### 5. **bodies_order_products** 
Таблица связи "многие-ко-многим" между заказами и товарами.

```sql
CREATE TABLE bodies_order_products (
    id BIGSERIAL PRIMARY KEY,
    order_id BIGINT NOT NULL REFERENCES bodies_order(id),
    product_id BIGINT NOT NULL REFERENCES bodies_product(id)
);
```

**Структура:**
| Колонка | Тип | Описание |
|---------|------|---------|
| id | BIGSERIAL | Уникальный идентификатор строки |
| order_id | BIGINT | ID заказа (внешний ключ) |
| product_id | BIGINT | ID товара (внешний ключ) |

---

### 6. **bodies_profile**
Профили пользователей с ролями доступа.

```sql
CREATE TABLE bodies_profile (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL UNIQUE REFERENCES auth_user(id),
    role VARCHAR(20) DEFAULT 'authorized' 
         CHECK (role IN ('unauthorized', 'authorized', 'editor', 'admin'))
);
```

**Структура:**
| Колонка | Тип | Описание |
|---------|------|---------|
| id | BIGSERIAL | Уникальный идентификатор профиля |
| user_id | BIGINT | ID пользователя (UNIQUE, внешний ключ) |
| role | VARCHAR(20) | Роль: 'unauthorized', 'authorized', 'editor', 'admin' |

---

## 🔍 Практические SQL запросы

### **A. РАБОТА С ТОВАРАМИ (bodies_product)**

#### 1. Просмотр всех товаров
```sql
SELECT id, name, price, sku, description 
FROM bodies_product 
ORDER BY id DESC;
```

#### 2. Поиск товара по артикулу
```sql
SELECT * FROM bodies_product WHERE sku = 'ABC123';
```

#### 3. Добавление нового товара
```sql
INSERT INTO bodies_product (name, price, sku, description)
VALUES ('iPhone 15', 99999.99, 'IPHONE15', 'Смартфон последнего поколения');
```

#### 4. Обновление цены товара
```sql
UPDATE bodies_product 
SET price = 85000.00 
WHERE sku = 'IPHONE15';
```

#### 5. Удаление товара
```sql
DELETE FROM bodies_product WHERE sku = 'OLD_SKU';
```

#### 6. Найти товары дороже 10 000 рублей
```sql
SELECT name, price, sku 
FROM bodies_product 
WHERE price > 10000 
ORDER BY price DESC;
```

#### 7. Поиск товара по названию (частичное совпадение)
```sql
SELECT * FROM bodies_product 
WHERE name ILIKE '%iPhone%';  -- ILIKE для регистронезависимого поиска
```

#### 8. Статистика по товарам
```sql
SELECT 
    COUNT(*) as total_products,
    AVG(price) as avg_price,
    MIN(price) as min_price,
    MAX(price) as max_price
FROM bodies_product;
```

---

### **B. РАБОТА С ПОЛЬЗОВАТЕЛЯМИ И ПРОФИЛЯМИ**

#### 1. Просмотр всех пользователей с их ролями
```sql
SELECT 
    u.id,
    u.username,
    u.email,
    p.role as user_role
FROM auth_user u
LEFT JOIN bodies_profile p ON u.id = p.user_id
ORDER BY u.id DESC;
```

#### 2. Добавить нового пользователя (только в auth_user)
```sql
-- ВАЖНО: Пароль ДОЛЖЕН быть закодирован методом Django!
-- Используйте эту команду только для тестирования
INSERT INTO auth_user (username, email, password, is_active, is_staff, date_joined)
VALUES ('newuser', 'newuser@mail.com', 'pbkdf2_sha256$...', true, false, NOW());
```

**ЛУЧШЕ:** Используйте Django ORM или `python manage.py createsuperuser`

#### 3. Найти администраторов
```sql
SELECT 
    u.id,
    u.username,
    u.email,
    p.role
FROM auth_user u
JOIN bodies_profile p ON u.id = p.user_id
WHERE p.role = 'admin';
```

#### 4. Найти редакторов
```sql
SELECT u.username, p.role
FROM auth_user u
JOIN bodies_profile p ON u.id = p.user_id
WHERE p.role IN ('editor', 'admin');
```

#### 5. Назначить пользователю роль администратора
```sql
UPDATE bodies_profile 
SET role = 'admin' 
WHERE user_id = 5;
```

#### 6. Деактивировать пользователя
```sql
UPDATE auth_user 
SET is_active = false 
WHERE username = 'username_to_disable';
```

---

### **C. РАБОТА С ЗАКАЗАМИ (bodies_order)**

#### 1. Просмотр всех заказов
```sql
SELECT 
    o.id,
    o.receiveCode,
    u.username as customer,
    o.createdAt,
    o.status,
    pp.address as pickup_point
FROM bodies_order o
JOIN auth_user u ON o.user_id = u.id
LEFT JOIN bodies_pickuppoint pp ON o.pickupPoint_id = pp.id
ORDER BY o.createdAt DESC;
```

#### 2. Заказы конкретного пользователя
```sql
SELECT 
    o.id,
    o.receiveCode,
    o.createdAt,
    o.status,
    COUNT(op.product_id) as items_count
FROM bodies_order o
LEFT JOIN bodies_order_products op ON o.id = op.order_id
WHERE o.user_id = 3
GROUP BY o.id
ORDER BY o.createdAt DESC;
```

#### 3. Заказы со статусом "Новый"
```sql
SELECT 
    o.id,
    o.receiveCode,
    u.username,
    o.createdAt
FROM bodies_order o
JOIN auth_user u ON o.user_id = u.id
WHERE o.status = 'new'
ORDER BY o.createdAt ASC;
```

#### 4. Создать новый заказ
```sql
-- 1. Создать запись в bodies_order
INSERT INTO bodies_order (user_id, createdAt, receiveCode, status, pickupPoint_id)
VALUES (3, NOW(), 'ABC123', 'new', 1)
RETURNING id;  -- Это вернет ID созданного заказа

-- 2. Добавить товары в заказ (используя ID заказа)
INSERT INTO bodies_order_products (order_id, product_id)
VALUES 
    (5, 2),   -- заказ 5, товар 2
    (5, 7);   -- заказ 5, товар 7
```

#### 5. Получить товары в конкретном заказе
```sql
SELECT 
    p.id,
    p.name,
    p.sku,
    p.price
FROM bodies_order_products op
JOIN bodies_product p ON op.product_id = p.id
WHERE op.order_id = 5
ORDER BY p.name;
```

#### 6. Полная информация по заказу
```sql
SELECT 
    o.id as order_id,
    o.receiveCode,
    u.username,
    u.email,
    o.createdAt,
    COALESCE(o.deliveryDate, 'Не доставлен') as delivery_date,
    o.status,
    pp.address as pickup_point,
    STRING_AGG(p.name, ', ') as products,
    SUM(p.price) as total_amount
FROM bodies_order o
JOIN auth_user u ON o.user_id = u.id
LEFT JOIN bodies_pickuppoint pp ON o.pickupPoint_id = pp.id
LEFT JOIN bodies_order_products op ON o.id = op.order_id
LEFT JOIN bodies_product p ON op.product_id = p.id
WHERE o.id = 5
GROUP BY o.id, u.id, u.username, u.email, pp.id;
```

#### 7. Изменить статус заказа на "Завершен"
```sql
UPDATE bodies_order 
SET 
    status = 'delivered',
    deliveryDate = NOW()
WHERE id = 5;
```

#### 8. Удалить товар из заказа
```sql
DELETE FROM bodies_order_products 
WHERE order_id = 5 AND product_id = 7;
```

#### 9. Удалить весь заказ
```sql
DELETE FROM bodies_order WHERE id = 5;
-- Товары удалятся автоматически (CASCADE для bodies_order_products)
```

#### 10. Статистика по заказам
```sql
SELECT 
    COUNT(*) as total_orders,
    SUM(CASE WHEN status = 'new' THEN 1 ELSE 0 END) as new_orders,
    SUM(CASE WHEN status = 'delivered' THEN 1 ELSE 0 END) as delivered_orders,
    COUNT(DISTINCT user_id) as unique_customers
FROM bodies_order;
```

---

### **D. РАБОТА С ПУНКТАМИ ВЫДАЧИ (bodies_pickuppoint)**

#### 1. Просмотр всех пунктов выдачи
```sql
SELECT id, address FROM bodies_pickuppoint ORDER BY id;
```

#### 2. Добавить новый пункт выдачи
```sql
INSERT INTO bodies_pickuppoint (address)
VALUES ('Москва, ул. Тверская, д. 5');
```

#### 3. Получить заказы для конкретного пункта выдачи
```sql
SELECT 
    o.id,
    o.receiveCode,
    u.username,
    o.status
FROM bodies_order o
JOIN auth_user u ON o.user_id = u.id
WHERE o.pickupPoint_id = 1
ORDER BY o.createdAt DESC;
```

#### 4. Обновить адрес пункта выдачи
```sql
UPDATE bodies_pickuppoint 
SET address = 'Москва, Красная площадь, д. 1' 
WHERE id = 1;
```

#### 5. Удалить пункт выдачи (нельзя если есть заказы)
```sql
DELETE FROM bodies_pickuppoint WHERE id = 1;
```

---

### **E. АНАЛИТИКА И ОТЧЕТЫ**

#### 1. Самые популярные товары
```sql
SELECT 
    p.name,
    p.sku,
    COUNT(op.id) as times_ordered,
    SUM(p.price) as total_revenue
FROM bodies_product p
LEFT JOIN bodies_order_products op ON p.id = op.product_id
GROUP BY p.id, p.name, p.sku
ORDER BY times_ordered DESC
LIMIT 10;
```

#### 2. Активные пользователи (сделавшие заказы)
```sql
SELECT 
    u.id,
    u.username,
    COUNT(o.id) as order_count,
    MAX(o.createdAt) as last_order
FROM auth_user u
LEFT JOIN bodies_order o ON u.id = o.user_id
GROUP BY u.id, u.username
ORDER BY order_count DESC;
```

#### 3. Сумма заказов по пользователям
```sql
SELECT 
    u.username,
    COUNT(DISTINCT o.id) as order_count,
    COUNT(DISTINCT op.product_id) as items_count,
    SUM(p.price) as total_spent
FROM auth_user u
LEFT JOIN bodies_order o ON u.id = o.user_id
LEFT JOIN bodies_order_products op ON o.id = op.order_id
LEFT JOIN bodies_product p ON op.product_id = p.id
GROUP BY u.id, u.username
ORDER BY total_spent DESC NULLS LAST;
```

#### 4. Заказы за последние 30 дней
```sql
SELECT 
    DATE(o.createdAt) as order_date,
    COUNT(*) as orders_count,
    COUNT(DISTINCT o.user_id) as unique_customers
FROM bodies_order o
WHERE o.createdAt >= CURRENT_DATE - INTERVAL '30 days'
GROUP BY DATE(o.createdAt)
ORDER BY order_date DESC;
```

---

## 🛠️ ОПЕРАЦИИ ПРИ РАБОТЕ С PostgreSQL

### Подключение к базе данных
```bash
psql -U postgres -d shop -h localhost
```

### Основные команды в psql

```sql
-- Показать все базы данных
\l

-- Подключиться к базе
\c shop

-- Показать все таблицы
\dt

-- Показать структуру таблицы
\d bodies_product

-- Показать индексы
\di

-- Показать внешние ключи
\d bodies_order

-- Выйти из psql
\q
```

---

## ⚠️ ВАЖНЫЕ ПРАВИЛА

### 1. **Никогда не редактируйте напрямую через SQL:**
- Пароли в `auth_user` - используйте Django ORM
- Таблицы миграций `django_*` - используйте `python manage.py migrate`

### 2. **При импорте товаров используйте Python скрипт:**
```bash
python scripts/import_products.py data/products_from_exam.csv
```

Вместо прямого SQL INSERT, потому что:
- Валидируются данные
- Обновляются существующие товары
- Обрабатываются ошибки

### 3. **Резервное копирование**
```bash
pg_dump -U postgres shop > backup.sql
```

### 4. **Восстановление из резервной копии**
```bash
psql -U postgres -d shop < backup.sql
```

---

## 📝 ПРИМЕРЫ СЛОЖНЫХ ЗАПРОСОВ

### Заказы пользователя со всеми деталями
```sql
WITH user_orders AS (
    SELECT 
        o.id,
        o.receiveCode,
        u.username,
        u.email,
        o.createdAt,
        o.status,
        o.deliveryDate,
        pp.address
    FROM bodies_order o
    JOIN auth_user u ON o.user_id = u.id
    LEFT JOIN bodies_pickuppoint pp ON o.pickupPoint_id = pp.id
    WHERE o.user_id = 3
)
SELECT 
    uo.*,
    p.name,
    p.price,
    p.sku
FROM user_orders uo
LEFT JOIN bodies_order_products op ON uo.id = op.order_id
LEFT JOIN bodies_product p ON op.product_id = p.id
ORDER BY uo.createdAt DESC;
```

### Недавно не доставленные заказы
```sql
SELECT 
    o.id,
    o.receiveCode,
    u.username,
    o.createdAt,
    EXTRACT(DAY FROM NOW() - o.createdAt) as days_pending,
    pp.address
FROM bodies_order o
JOIN auth_user u ON o.user_id = u.id
LEFT JOIN bodies_pickuppoint pp ON o.pickupPoint_id = pp.id
WHERE o.status = 'new' 
  AND o.createdAt < NOW() - INTERVAL '7 days'
ORDER BY o.createdAt ASC;
```

---

## 🔧 ПОЛЕЗНЫЕ ФУНКЦИИ PostgreSQL

```sql
-- Текущая дата и время
NOW()

-- Дата в формате
DATE(o.createdAt)

-- Сумма с условием
SUM(CASE WHEN condition THEN value ELSE 0 END)

-- Объединение строк
STRING_AGG(column, ', ')

-- Подсчет с условием
COUNT(CASE WHEN condition THEN 1 END)

-- Выборка диапазона дат
WHERE createdAt BETWEEN '2025-01-01' AND '2025-12-31'

-- Сортировка с пропусками NULL значений
ORDER BY column DESC NULLS LAST
```

---

*Документ создан на основе структуры Django проекта*
