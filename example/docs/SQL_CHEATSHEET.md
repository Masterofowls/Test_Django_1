# ⚡ SQL Шпаргалка (Quick Reference)

## Быстрое подключение к БД

```bash
# PostgreSQL консоль
psql -U postgres -d shop -h localhost

# Выход из консоли
\q
```

---

## 🛒 ТОП ОПЕРАЦИИ

### ТОВАРЫ

| Операция | SQL |
|----------|-----|
| **Все товары** | `SELECT * FROM bodies_product ORDER BY id;` |
| **Найти товар** | `SELECT * FROM bodies_product WHERE sku = 'ABC123';` |
| **Добавить товар** | `INSERT INTO bodies_product (name, sku, price, description) VALUES ('Товар', 'SKU', 99.99, 'Опис');` |
| **Обновить цену** | `UPDATE bodies_product SET price = 99.99 WHERE sku = 'SKU';` |
| **Удалить товар** | `DELETE FROM bodies_product WHERE sku = 'SKU';` |
| **Товары дороже** | `SELECT * FROM bodies_product WHERE price > 10000 ORDER BY price;` |
| **Топ 10 товаров** | `SELECT * FROM bodies_product ORDER BY id DESC LIMIT 10;` |

### ПОЛЬЗОВАТЕЛИ

| Операция | SQL |
|----------|-----|
| **Все пользователи** | `SELECT u.id, u.username, p.role FROM auth_user u LEFT JOIN bodies_profile p ON u.id = p.user_id;` |
| **Админы** | `SELECT u.username FROM auth_user u JOIN bodies_profile p ON u.id = p.user_id WHERE p.role = 'admin';` |
| **Редакторы** | `SELECT u.username FROM auth_user u JOIN bodies_profile p ON u.id = p.user_id WHERE p.role IN ('editor', 'admin');` |
| **Назначить админом** | `UPDATE bodies_profile SET role = 'admin' WHERE user_id = 5;` |
| **Назначить редактором** | `UPDATE bodies_profile SET role = 'editor' WHERE user_id = 5;` |
| **Деактивировать** | `UPDATE auth_user SET is_active = false WHERE username = 'user';` |

### ЗАКАЗЫ

| Операция | SQL |
|----------|-----|
| **Все заказы** | `SELECT o.*, u.username FROM bodies_order o JOIN auth_user u ON o.user_id = u.id ORDER BY o.createdAt DESC;` |
| **Заказы пользователя** | `SELECT * FROM bodies_order WHERE user_id = 1 ORDER BY createdAt DESC;` |
| **Новые заказы** | `SELECT * FROM bodies_order WHERE status = 'new' ORDER BY createdAt DESC;` |
| **Доставленные** | `SELECT * FROM bodies_order WHERE status = 'delivered' ORDER BY createdAt DESC;` |
| **Товары в заказе** | `SELECT p.* FROM bodies_order_products op JOIN bodies_product p ON op.product_id = p.id WHERE op.order_id = 1;` |
| **Отметить доставлен** | `UPDATE bodies_order SET status = 'delivered', deliveryDate = NOW() WHERE id = 1;` |
| **Удалить заказ** | `DELETE FROM bodies_order WHERE id = 1;` |

---

## 📊 СТАТИСТИКА

```sql
-- Количество товаров
SELECT COUNT(*) as всего FROM bodies_product;

-- Количество заказов
SELECT COUNT(*) as всего FROM bodies_order;

-- Количество пользователей
SELECT COUNT(*) as всего FROM auth_user;

-- Средняя цена товара
SELECT AVG(price) as средняя FROM bodies_product;

-- Самый дорогой товар
SELECT MAX(price) as макс FROM bodies_product;

-- Самый дешевый товар
SELECT MIN(price) as мин FROM bodies_product;

-- Сумма всех заказов (доход)
SELECT SUM(p.price) as доход 
FROM bodies_order o
LEFT JOIN bodies_order_products op ON o.id = op.order_id
LEFT JOIN bodies_product p ON op.product_id = p.id;
```

---

## 🔍 ПОИСК И ФИЛЬТРЫ

```sql
-- Поиск по названию (частичный)
SELECT * FROM bodies_product WHERE name ILIKE '%iPhone%';

-- Товары в диапазоне цен
SELECT * FROM bodies_product WHERE price BETWEEN 10000 AND 50000;

-- Товары дороже N руб
SELECT * FROM bodies_product WHERE price > 50000;

-- Товары дешевле N руб
SELECT * FROM bodies_product WHERE price < 5000;

-- Заказы за период
SELECT * FROM bodies_order WHERE createdAt BETWEEN '2025-01-01' AND '2025-02-28';

-- Заказы за последние N дней
SELECT * FROM bodies_order WHERE createdAt >= NOW() - INTERVAL '7 days';

-- Активные пользователи
SELECT * FROM auth_user WHERE is_active = true;

-- Неактивные пользователи
SELECT * FROM auth_user WHERE is_active = false;
```

---

## ➕ ДОБАВЛЕНИЕ ДАННЫХ

```sql
-- Добавить товар
INSERT INTO bodies_product (name, sku, price, description)
VALUES ('Название', 'SKU123', 99.99, 'Описание');

-- Добавить пункт выдачи
INSERT INTO bodies_pickuppoint (address)
VALUES ('Город, улица, д. 1');

-- Добавить заказ (без товаров)
INSERT INTO bodies_order (user_id, createdAt, receiveCode, status)
VALUES (1, NOW(), 'CODE123', 'new');

-- Добавить товар в заказ
INSERT INTO bodies_order_products (order_id, product_id)
VALUES (1, 5);  -- заказ 1, товар 5

-- Добавить несколько товаров в заказ
INSERT INTO bodies_order_products (order_id, product_id)
VALUES (1, 5), (1, 7), (1, 12);
```

---

## ✏️ ОБНОВЛЕНИЕ ДАННЫХ

```sql
-- Изменить название товара
UPDATE bodies_product SET name = 'Новое название' WHERE sku = 'SKU123';

-- Изменить цену
UPDATE bodies_product SET price = 85.00 WHERE sku = 'SKU123';

-- Увеличить цену на 10%
UPDATE bodies_product SET price = price * 1.1 WHERE id = 1;

-- Уменьшить цену на 20%
UPDATE bodies_product SET price = price * 0.8 WHERE id = 1;

-- Отметить заказ как доставленный
UPDATE bodies_order SET status = 'delivered', deliveryDate = NOW() WHERE id = 1;

-- Назначить пункт выдачи заказу
UPDATE bodies_order SET pickupPoint_id = 2 WHERE id = 1;

-- Изменить роль пользователя
UPDATE bodies_profile SET role = 'editor' WHERE user_id = 5;
```

---

## ❌ УДАЛЕНИЕ ДАННЫХ

```sql
-- Удалить товар
DELETE FROM bodies_product WHERE sku = 'SKU123';

-- Удалить товар из заказа
DELETE FROM bodies_order_products WHERE order_id = 1 AND product_id = 5;

-- Удалить пункт выдачи
DELETE FROM bodies_pickuppoint WHERE id = 1;

-- Удалить заказ
DELETE FROM bodies_order WHERE id = 1;

-- Удалить пользователя (и его заказы)
DELETE FROM auth_user WHERE id = 5;

-- Удалить все новые заказы (ОСТОРОЖНО!)
DELETE FROM bodies_order WHERE status = 'new';
```

---

## 📋 СЛОЖНЫЕ ЗАПРОСЫ

```sql
-- Заказы с полной информацией
SELECT 
    o.id, o.receiveCode, u.username, o.createdAt, o.status,
    COUNT(op.product_id) as товаров,
    SUM(p.price) as сумма
FROM bodies_order o
JOIN auth_user u ON o.user_id = u.id
LEFT JOIN bodies_order_products op ON o.id = op.order_id
LEFT JOIN bodies_product p ON op.product_id = p.id
GROUP BY o.id, u.username
ORDER BY o.createdAt DESC;

-- Популярные товары
SELECT p.name, COUNT(*) as раз_заказан
FROM bodies_product p
JOIN bodies_order_products op ON p.id = op.product_id
GROUP BY p.id, p.name
ORDER BY COUNT(*) DESC
LIMIT 10;

-- Лучшие клиенты (по сумме)
SELECT 
    u.username, 
    COUNT(o.id) as заказов,
    SUM(p.price) as потрачено
FROM auth_user u
LEFT JOIN bodies_order o ON u.id = o.user_id
LEFT JOIN bodies_order_products op ON o.id = op.order_id
LEFT JOIN bodies_product p ON op.product_id = p.id
GROUP BY u.id, u.username
ORDER BY SUM(p.price) DESC;

-- Заказы ждут более неделю
SELECT * FROM bodies_order 
WHERE status = 'new' AND createdAt < NOW() - INTERVAL '7 days';

-- Товары которые никто не заказывал
SELECT * FROM bodies_product p
LEFT JOIN bodies_order_products op ON p.id = op.product_id
WHERE op.id IS NULL;
```

---

## 🔑 УСЛОВИЯ И ПАРАМЕТРЫ

### WHERE условия
```sql
WHERE price > 100              -- больше
WHERE price < 100              -- меньше
WHERE price >= 100             -- больше или равно
WHERE price <= 100             -- меньше или равно
WHERE price = 100              -- равно
WHERE price <> 100             -- не равно
WHERE price BETWEEN 10 AND 100 -- диапазон
WHERE name LIKE 'iPhone%'      -- начинаается с
WHERE name ILIKE '%phone%'     -- содержит (без учета регистра)
WHERE status IN ('new', 'delivered')  -- один из списка
WHERE user_id IS NULL          -- пусто
WHERE user_id IS NOT NULL      -- не пусто
```

### ORDER BY
```sql
ORDER BY price ASC              -- возрастание (дешевле → дороже)
ORDER BY price DESC             -- убывание (дороже → дешевле)
ORDER BY name                   -- по названию (А-Я)
ORDER BY createdAt DESC         -- новейшие первыми
ORDER BY price DESC, name ASC   -- несколько параметров
ORDER BY price DESC NULLS LAST  -- NULL значения в конце
```

### LIMIT и OFFSET
```sql
LIMIT 10              -- первые 10 записей
LIMIT 10 OFFSET 20    -- пропустить 20, взять 10
LIMIT 10 OFFSET 0     -- то же что LIMIT 10
```

---

## 🎯 СЛУЧАЙНЫЕ ПОЛЕЗНЫЕ КОМАНДЫ

```sql
-- Очистить таблицу (удалить все)
TRUNCATE bodies_product CASCADE;

-- Сбросить счетчик ID
ALTER SEQUENCE bodies_product_id_seq RESTART WITH 1;

-- Текущее время сервера
SELECT NOW();

-- Текущую дату
SELECT CURRENT_DATE;

-- Версия PostgreSQL
SELECT version();

-- Размер БД
SELECT pg_size_pretty(pg_database_size('shop'));

-- Переопределить пароль пользователя PostgreSQL
ALTER USER postgres WITH PASSWORD 'новый_пароль';
```

---

## 📌 ПРИМЕРЫ НА ВКУС

### Найти заказ по коду получения
```sql
SELECT * FROM bodies_order WHERE receiveCode = 'ABC123';
```

### Получить количество товаров в каждом заказе
```sql
SELECT order_id, COUNT(*) as товаров
FROM bodies_order_products
GROUP BY order_id;
```

### Клиент с большинством заказов
```sql
SELECT u.username, COUNT(o.id) as заказов
FROM auth_user u
LEFT JOIN bodies_order o ON u.id = o.user_id
GROUP BY u.id, u.username
ORDER BY COUNT(o.id) DESC
LIMIT 1;
```

### Товар, который приносит больше всего доход
```sql
SELECT p.name, SUM(p.price) as доход
FROM bodies_product p
JOIN bodies_order_products op ON p.id = op.product_id
GROUP BY p.id, p.name
ORDER BY SUM(p.price) DESC
LIMIT 1;
```

### Пункт выдачи с большинством заказов
```sql
SELECT pp.address, COUNT(o.id) as заказов
FROM bodies_pickuppoint pp
LEFT JOIN bodies_order o ON pp.id = o.pickupPoint_id
GROUP BY pp.id, pp.address
ORDER BY COUNT(o.id) DESC;
```

---

## 🆘 КОМАНДЫ ПОМОЩИ

```bash
# В консоли psql:
\h                    # помощь по SQL командам
\h SELECT             # помощь по SELECT
\d                    # показать все таблицы
\d bodies_product     # структура таблицы
\l                    # список БД
\du                   # список пользователей
\dt                   # таблицы
\di                   # индексы
\df                   # функции
```

---

*Сохраните эту страницу закладкой! ⭐*
