# 💼 Практические примеры SQL для магазина

## Выполнение этих запросов

Подключитесь к базе:
```bash
psql -U postgres -d shop -h localhost
```

Или используйте DBeaver (рекомендуется для предпросмотра)

---

## 1️⃣ ИМПОРТ ТОВАРОВ

### Вариант 1: Использовать Python скрипт (РЕКОМЕНДУЕТСЯ)
```bash
cd d:\Test_Django_1\example
python scripts/import_products.py data/products_from_exam.csv
```

**Преимущества:**
- Валидирует данные
- Обновляет существующие товары
- Обрабатывает ошибки
- Вывод статуса

### Вариант 2: Прямой импорт через SQL (если CSV уже в нужном формате)

```sql
-- Сначала создайте временную таблицу
CREATE TEMP TABLE temp_products (
    name VARCHAR(255),
    sku VARCHAR(50),
    price VARCHAR(20),
    description TEXT
);

-- Импортируйте CSV в временную таблицу
COPY temp_products(name, sku, price, description) 
FROM 'C:\\path\\to\\products.csv' 
WITH (FORMAT csv, HEADER true, DELIMITER ',', ENCODING 'UTF8');

-- Добавьте или обновите товары в основную таблицу
INSERT INTO bodies_product (name, price, sku, description)
SELECT name, price::NUMERIC(10,2), sku, COALESCE(description, '')
FROM temp_products
ON CONFLICT (sku) DO UPDATE SET
    name = EXCLUDED.name,
    price = EXCLUDED.price,
    description = EXCLUDED.description;

-- Удалите временную таблицу
DROP TABLE temp_products;

-- Проверка результата
SELECT COUNT(*) as всего_товаров FROM bodies_product;
```

---

## 2️⃣ СОЗДАНИЕ И УПРАВЛЕНИЕ ЗАКАЗАМИ

### Создать новый заказ для пользователя

```sql
-- Пример 1: Заказ с одним товаром
WITH new_order AS (
    INSERT INTO bodies_order (user_id, createdAt, receiveCode, status, pickupPoint_id)
    VALUES (
        1,              -- ID пользователя
        NOW(),          -- текущее время
        'ABC123',       -- код получения
        'new',          -- статус
        1               -- ID пункта выдачи
    )
    RETURNING id
)
INSERT INTO bodies_order_products (order_id, product_id)
SELECT (SELECT id FROM new_order), 5;  -- товар с ID 5

-- Проверка
SELECT * FROM bodies_order WHERE status = 'new' ORDER BY createdAt DESC LIMIT 1;
```

### Добавить несколько товаров в существующий заказ

```sql
-- Добавить товары 3, 5, 7 в заказ с ID 1
INSERT INTO bodies_order_products (order_id, product_id)
VALUES 
    (1, 3),
    (1, 5),
    (1, 7);
```

### Получить полную информацию о заказе

```sql
SELECT 
    o.id as "ID Заказа",
    o.receiveCode as "Код получения",
    u.username as "Пользователь",
    u.email as "Email",
    COUNT(op.product_id) as "Количество товаров",
    SUM(p.price) as "Сумма заказа (₽)",
    o.createdAt as "Дата создания",
    o.deliveryDate as "Дата доставки",
    o.status as "Статус",
    CASE o.status 
        WHEN 'new' THEN 'Не доставлен'
        WHEN 'delivered' THEN 'Доставлен'
    END as "Название статуса",
    pp.address as "Пункт выдачи"
FROM bodies_order o
JOIN auth_user u ON o.user_id = u.id
LEFT JOIN bodies_pickuppoint pp ON o.pickupPoint_id = pp.id
LEFT JOIN bodies_order_products op ON o.id = op.order_id
LEFT JOIN bodies_product p ON op.product_id = p.id
WHERE o.id = 1
GROUP BY o.id, u.id, u.username, u.email, pp.id;
```

### Список товаров в заказе

```sql
SELECT 
    p.id,
    p.name as "Товар",
    p.sku as "Артикул",
    p.price as "Цена (₽)",
    p.description as "Описание"
FROM bodies_order_products op
JOIN bodies_product p ON op.product_id = p.id
WHERE op.order_id = 1
ORDER BY p.name;
```

### Изменить статус заказа

```sql
-- Отметить заказ как доставленный
UPDATE bodies_order 
SET 
    status = 'delivered',
    deliveryDate = NOW()
WHERE id = 1;

-- Проверка
SELECT id, receiveCode, status, deliveryDate 
FROM bodies_order 
WHERE id = 1;
```

### Удалить товар из заказа

```sql
-- Удалить товар с ID 5 из заказа с ID 1
DELETE FROM bodies_order_products 
WHERE order_id = 1 AND product_id = 5;

-- Проверка
SELECT COUNT(*) as товаров_в_заказе
FROM bodies_order_products
WHERE order_id = 1;
```

### Отменить весь заказ

```sql
-- Удалить заказ (товары удалятся автоматически)
DELETE FROM bodies_order WHERE id = 1;
```

---

## 3️⃣ РАБОТА С ТОВАРАМИ

### Найти товар по артикулу

```sql
SELECT * FROM bodies_product 
WHERE sku = 'IPHONE15PRO';
```

### Поиск товаров по названию

```sql
-- Частичный поиск (не зависит от регистра)
SELECT * FROM bodies_product 
WHERE name ILIKE '%iPhone%'
ORDER BY price DESC;
```

### Товары в диапазоне цен

```sql
SELECT 
    name,
    sku,
    price,
    description
FROM bodies_product
WHERE price BETWEEN 5000 AND 50000
ORDER BY price;
```

### Самые дорогие товары

```sql
SELECT 
    name,
    sku,
    price
FROM bodies_product
ORDER BY price DESC
LIMIT 10;
```

### Самые дешевые товары

```sql
SELECT 
    name,
    sku,
    price
FROM bodies_product
ORDER BY price ASC
LIMIT 5;
```

### Обновить цену товара

```sql
-- Увеличить цену на 10%
UPDATE bodies_product 
SET price = price * 1.1
WHERE sku = 'IPHONE15PRO';

-- Или установить конкретную цену
UPDATE bodies_product 
SET price = 85000.00
WHERE sku = 'IPHONE15PRO';

-- Проверить
SELECT name, price FROM bodies_product WHERE sku = 'IPHONE15PRO';
```

### Обновить описание товара

```sql
UPDATE bodies_product 
SET description = 'Высокопроизводительный смартфон последнего поколения'
WHERE sku = 'IPHONE15PRO';
```

### Дублирующиеся товары (одинаковый SKU)

```sql
-- Должно быть 0, т.к. SKU UNIQUE
SELECT sku, COUNT(*) as count
FROM bodies_product
GROUP BY sku
HAVING COUNT(*) > 1;
```

### Витрина товаров с информацией о популярности

```sql
SELECT 
    p.id,
    p.name,
    p.sku,
    p.price,
    COUNT(op.id) as "раз заказан",
    SUM(p.price) as "сумма продаж (₽)"
FROM bodies_product p
LEFT JOIN bodies_order_products op ON p.id = op.product_id
GROUP BY p.id, p.name, p.sku, p.price
ORDER BY COUNT(op.id) DESC;
```

---

## 4️⃣ РАБОТА С ПОЛЬЗОВАТЕЛЯМИ И РОЛЯМИ

### Список всех пользователей с ролями

```sql
SELECT 
    u.id,
    u.username as "Логин",
    u.email as "Email",
    COALESCE(p.role, 'нет профиля') as "Роль",
    u.is_active as "Активен",
    u.date_joined as "Дата регистрации"
FROM auth_user u
LEFT JOIN bodies_profile p ON u.id = p.user_id
ORDER BY u.id;
```

### Найти администраторов

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

### Найти редакторов

```sql
SELECT 
    u.id,
    u.username,
    u.email,
    p.role
FROM auth_user u
JOIN bodies_profile p ON u.id = p.user_id
WHERE p.role IN ('editor', 'admin');
```

### Найти авторизованных пользователей (не админов)

```sql
SELECT 
    u.id,
    u.username,
    u.email
FROM auth_user u
JOIN bodies_profile p ON u.id = p.user_id
WHERE p.role = 'authorized';
```

### Пользователи без профиля

```sql
SELECT 
    u.id,
    u.username,
    u.email
FROM auth_user u
LEFT JOIN bodies_profile p ON u.id = p.user_id
WHERE p.id IS NULL;
```

### Назначить пользователю роль администратора

```sql
-- Вариант 1: Если профиль существует
UPDATE bodies_profile 
SET role = 'admin' 
WHERE user_id = 3;

-- Вариант 2: Если профиля нет, создать его
INSERT INTO bodies_profile (user_id, role)
VALUES (3, 'admin')
ON CONFLICT (user_id) DO UPDATE SET role = 'admin';

-- Проверка
SELECT u.username, p.role 
FROM auth_user u
JOIN bodies_profile p ON u.id = p.user_id
WHERE u.id = 3;
```

### Понизить роль пользователя

```sql
UPDATE bodies_profile 
SET role = 'authorized' 
WHERE user_id = 3;
```

### Деактивировать пользователя

```sql
UPDATE auth_user 
SET is_active = false 
WHERE username = 'username';

-- Проверка
SELECT username, is_active FROM auth_user WHERE username = 'username';
```

### Активировать пользователя

```sql
UPDATE auth_user 
SET is_active = true 
WHERE username = 'username';
```

### Удалить пользователя (и все его заказы)

```sql
DELETE FROM auth_user WHERE id = 5;
-- Каскадно удалятся:
-- - его профиль
-- - его заказы
-- - товары из его заказов
```

---

## 5️⃣ АНАЛИТИКА И ОТЧЕТЫ

### Сумма всех заказов по пользователям

```sql
SELECT 
    u.username as "Пользователь",
    COUNT(DISTINCT o.id) as "Заказов",
    COUNT(DISTINCT op.product_id) as "Товаров",
    SUM(p.price)::NUMERIC(10,2) as "Сумма (₽)"
FROM auth_user u
LEFT JOIN bodies_order o ON u.id = o.user_id
LEFT JOIN bodies_order_products op ON o.id = op.order_id
LEFT JOIN bodies_product p ON op.product_id = p.id
GROUP BY u.id, u.username
ORDER BY SUM(p.price) DESC NULLS LAST;
```

### Активные пользователи (те, что делали заказы)

```sql
SELECT 
    u.username,
    COUNT(DISTINCT o.id) as "заказов",
    MIN(o.createdAt) as "первый заказ",
    MAX(o.createdAt) as "последний заказ"
FROM auth_user u
JOIN bodies_order o ON u.id = o.user_id
GROUP BY u.id, u.username
ORDER BY COUNT(DISTINCT o.id) DESC;
```

### Неактивные пользователи (без заказов)

```sql
SELECT 
    u.username,
    u.email,
    u.date_joined
FROM auth_user u
LEFT JOIN bodies_order o ON u.id = o.user_id
WHERE o.id IS NULL
ORDER BY u.date_joined DESC;
```

### Статистика по заказам

```sql
SELECT 
    COUNT(*) as "всего заказов",
    SUM(CASE WHEN status = 'new' THEN 1 ELSE 0 END) as "новых",
    SUM(CASE WHEN status = 'delivered' THEN 1 ELSE 0 END) as "доставлено",
    COUNT(DISTINCT user_id) as "уникальных клиентов",
    ROUND(AVG(price)::NUMERIC, 2) as "средняя сумма заказа (₽)"
FROM (
    SELECT 
        o.id,
        o.status,
        o.user_id,
        SUM(p.price) as price
    FROM bodies_order o
    LEFT JOIN bodies_order_products op ON o.id = op.order_id
    LEFT JOIN bodies_product p ON op.product_id = p.id
    GROUP BY o.id, o.status, o.user_id
) order_stats;
```

### Заказы по дням

```sql
SELECT 
    DATE(o.createdAt) as "Дата",
    COUNT(*) as "Заказов",
    COUNT(DISTINCT o.user_id) as "Клиентов",
    SUM(p.price)::NUMERIC(10,2) as "Сумма (₽)"
FROM bodies_order o
LEFT JOIN bodies_order_products op ON o.id = op.order_id
LEFT JOIN bodies_product p ON op.product_id = p.id
GROUP BY DATE(o.createdAt)
ORDER BY DATE(o.createdAt) DESC;
```

### Заказы за последние 30 дней

```sql
SELECT 
    DATE(o.createdAt) as день,
    COUNT(*) as заказов
FROM bodies_order o
WHERE o.createdAt >= CURRENT_DATE - INTERVAL '30 days'
GROUP BY DATE(o.createdAt)
ORDER BY DATE(o.createdAt) DESC;
```

### Производительность пунктов выдачи

```sql
SELECT 
    pp.address as "Пункт выдачи",
    COUNT(*) as "заказов",
    COUNT(CASE WHEN o.status = 'delivered' THEN 1 END) as "доставлено",
    COUNT(CASE WHEN o.status = 'new' THEN 1 END) as "ожидает"
FROM bodies_pickuppoint pp
LEFT JOIN bodies_order o ON pp.id = o.pickupPoint_id
GROUP BY pp.id, pp.address
ORDER BY COUNT(*) DESC;
```

### Популярные товары (топ 10)

```sql
SELECT 
    p.name as "Товар",
    p.sku as "Артикул",
    COUNT(*) as "раз продан",
    SUM(p.price)::NUMERIC(10,2) as "доход (₽)"
FROM bodies_product p
JOIN bodies_order_products op ON p.id = op.product_id
GROUP BY p.id, p.name, p.sku
ORDER BY COUNT(*) DESC
LIMIT 10;
```

### Товары которые никто не заказывал

```sql
SELECT 
    p.id,
    p.name,
    p.sku,
    p.price
FROM bodies_product p
LEFT JOIN bodies_order_products op ON p.id = op.product_id
WHERE op.id IS NULL
ORDER BY p.price DESC;
```

---

## 6️⃣ ОБСЛУЖИВАНИЕ БАЗЫ

### Статистика по размеру таблиц

```sql
SELECT
    schemaname,
    tablename,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) as "Размер"
FROM pg_tables
WHERE schemaname NOT IN ('pg_catalog', 'information_schema')
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;
```

### Вакуум базы (оптимизация)

```sql
VACUUM ANALYZE;
```

### Восстановление индексов

```sql
REINDEX DATABASE shop;
```

### Backup базы

```bash
pg_dump -U postgres -h localhost shop > backup_2026_02_23.sql
```

### Восстановление из backup

```bash
psql -U postgres -h localhost shop < backup_2026_02_23.sql
```

---

## ⚠️ ЧАСТЫЕ ОШИБКИ

### Ошибка: "duplicate key value violates unique constraint"
```sql
-- Причина: товар с таким SKU уже существует
-- Решение: используйте UPDATE вместо INSERT для существующих SKU

-- Неправильно:
INSERT INTO bodies_product (name, sku, price)
VALUES ('iPhone', 'IPHONE15', 100000);

-- Правильно:
INSERT INTO bodies_product (name, sku, price)
VALUES ('iPhone', 'IPHONE15', 100000)
ON CONFLICT (sku) DO UPDATE SET price = 100000;
```

### Ошибка: "foreign key constraint"
```sql
-- Причина: ссылка на несуществующего пользователя или товара
-- Решение: сначала проверьте существование

SELECT * FROM auth_user WHERE id = 999;  -- проверить пользователя существует
SELECT * FROM bodies_product WHERE id = 999;  -- проверить товар существует
```

### Ошибка: "type mismatch"
```sql
-- Правильный формат цены
UPDATE bodies_product SET price = 99.99 WHERE id = 1;  -- OK
UPDATE bodies_product SET price = '99.99'::NUMERIC WHERE id = 1;  -- Явное преобразование

-- Правильный формат даты
UPDATE bodies_order SET createdAt = NOW() WHERE id = 1;
UPDATE bodies_order SET createdAt = '2025-02-23 10:30:00'::TIMESTAMP WHERE id = 1;
```

---

*Последнее обновление: февраль 2026*
