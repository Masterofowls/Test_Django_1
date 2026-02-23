# 📐 Схема базы данных

## ER-диаграмма (Entity-Relationship Diagram)

```
┌─────────────┐
│  auth_user  │
├─────────────┤
│ id (PK)     │
│ username    │
│ password    │
│ email       │
│ first_name  │
│ last_name   │
│ is_active   │
│ date_joined │
└────┬────────┘
     │ (1)
     │
     ├─────────────────────────┐
     │ (1)                     │ (многие)
     │                         │
     │ 1:N                     │ 1:N
     │                         │
     ↓                         ↓
┌─────────────────────┐   ┌──────────────────┐
│  bodies_profile     │   │  bodies_order    │
├─────────────────────┤   ├──────────────────┤
│ id (PK)             │   │ id (PK)          │
│ user_id (FK,UNIQUE) │   │ user_id (FK)     │
│ role                │   │ pickupPoint_id   │
│                     │   │ createdAt        │
│ - unauthorized      │   │ deliveryDate     │
│ - authorized        │   │ receiveCode      │
│ - editor            │   │ status           │
│ - admin             │   │ - new            │
└─────────────────────┘   │ - delivered      │
                          └────┬─────────────┘
                               │ (многие)
                               │
                               │ N:M (Many-to-Many)
                               │
                               ↓
                    ┌─────────────────────────┐
                    │ bodies_order_products   │
                    ├─────────────────────────┤
                    │ id (PK)                 │
                    │ order_id (FK)           │
                    │ product_id (FK)         │
                    └──────┬──────────────────┘
                           │
                           │ (многие)
                           │
                           ↓
                    ┌──────────────────────┐
                    │  bodies_product      │
                    ├──────────────────────┤
                    │ id (PK)              │
                    │ name                 │
                    │ price                │
                    │ sku (UNIQUE)         │
                    │ description          │
                    └──────────────────────┘


┌──────────────────────┐
│ bodies_pickuppoint   │
├──────────────────────┤
│ id (PK)              │
│ address              │
└──────┬───────────────┘
       │ (1)
       │
       │ 0:N
       │
       ↓
┌──────────────────┐
│  bodies_order    │
│ (pickupPoint_id) │
└──────────────────┘
```

---

## Описание таблиц и связей

### Основные таблицы

#### **auth_user** (встроенная таблица Django)
- **Назначение:** Хранение данных пользователей
- **Связи:**
  - 1:1 → bodies_profile (один пользователь имеет один профиль)
  - 1:N → bodies_order (один пользователь может иметь много заказов)

#### **bodies_profile**
- **Назначение:** Хранение ролей и доп. информации о пользователе
- **Связи:**
  - 1:1 ← auth_user

#### **bodies_product**
- **Назначение:** Каталог товаров магазина
- **Связи:**
  - N:M ← bodies_order (товар может быть в разных заказах)

#### **bodies_order**
- **Назначение:** Заказы пользователей
- **Связи:**
  - N:1 → auth_user (много заказов от одного пользователя)
  - 0:1 → bodies_pickuppoint (заказ может быть выдан в одном пункте)
  - N:M ↔ bodies_product (заказ содержит много товаров)

#### **bodies_order_products** (таблица промежуточная)
- **Назначение:** Связь между заказами и товарами (для N:M отношения)
- **Связи:**
  - N:1 → bodies_order
  - N:1 → bodies_product

#### **bodies_pickuppoint**
- **Назначение:** Пункты выдачи заказов
- **Связи:**
  - 1:N → bodies_order (один пункт может выдать много заказов)

---

## Примеры SQL по типам операций

### Вставка данных (INSERT)

#### Добавить товар
```sql
INSERT INTO bodies_product (name, price, sku, description)
VALUES ('iPhone 15 Pro', 120000.00, 'IPHONE15PRO', 'Флагман Apple 2024');
```

#### Создать заказ (с товарами)
```sql
-- Шаг 1: Создать заказ
INSERT INTO bodies_order (user_id, createdAt, receiveCode, status, pickupPoint_id)
VALUES (1, NOW(), 'ABC123', 'new', 1)
RETURNING id;

-- Шаг 2: Добавить товары (вместо <order_id> подставьте полученный ID)
INSERT INTO bodies_order_products (order_id, product_id)
VALUES 
    (1, 5),   -- заказ 1, товар 5
    (1, 7),   -- заказ 1, товар 7
    (1, 12);  -- заказ 1, товар 12
```

#### Добавить пункт выдачи
```sql
INSERT INTO bodies_pickuppoint (address)
VALUES ('Москва, улица Советская, д. 42');
```

---

### Обновление данных (UPDATE)

#### Обновить цену товара
```sql
UPDATE bodies_product 
SET price = 99999.99 
WHERE sku = 'IPHONE15PRO';
```

#### Отметить заказ как доставленный
```sql
UPDATE bodies_order 
SET 
    status = 'delivered',
    deliveryDate = NOW()
WHERE id = 1;
```

#### Изменить роль пользователя
```sql
UPDATE bodies_profile 
SET role = 'editor' 
WHERE user_id = 5;
```

---

### Удаление данных (DELETE)

#### Удалить товар (осторожно!)
```sql
DELETE FROM bodies_product WHERE sku = 'OLD_SKU';
```

#### Удалить заказ (удалят и товары автоматически)
```sql
DELETE FROM bodies_order WHERE id = 1;
```

#### Удалить товар из заказа
```sql
DELETE FROM bodies_order_products 
WHERE order_id = 1 AND product_id = 7;
```

---

### Получение данных (SELECT)

#### Полный список товаров с ценой
```sql
SELECT id, name, sku, price, description
FROM bodies_product
ORDER BY price DESC;
```

#### Все заказы пользователя с деталями
```sql
SELECT 
    o.id as заказ,
    o.receiveCode as код,
    o.createdAt as дата,
    o.status as статус,
    STRING_AGG(p.name, ', ') as товары
FROM bodies_order o
LEFT JOIN bodies_order_products op ON o.id = op.order_id
LEFT JOIN bodies_product p ON op.product_id = p.id
WHERE o.user_id = 1
GROUP BY o.id
ORDER BY o.createdAt DESC;
```

#### Профили с ролями
```sql
SELECT 
    u.id,
    u.username,
    p.role,
    COUNT(o.id) as всего_заказов
FROM auth_user u
LEFT JOIN bodies_profile p ON u.id = p.user_id
LEFT JOIN bodies_order o ON u.id = o.user_id
GROUP BY u.id, u.username, p.role
ORDER BY u.username;
```

---

## Внешние ключи (Foreign Keys)

| Таблица | Колонка | Ссылается на | Действие при удалении |
|---------|---------|-------------|----------------------|
| bodies_profile | user_id | auth_user.id | CASCADE |
| bodies_order | user_id | auth_user.id | CASCADE |
| bodies_order | pickupPoint_id | bodies_pickuppoint.id | SET NULL |
| bodies_order_products | order_id | bodies_order.id | CASCADE |
| bodies_order_products | product_id | bodies_product.id | Set NULL или CASCADE |

---

## Ограничения (Constraints)

| Таблица | Ограничение | Описание |
|---------|-----------|---------|
| bodies_product | sku UNIQUE | Артикул должен быть уникален |
| bodies_product | price > 0 | Цена должна быть положительной |
| bodies_order | status IN (...) | Статус может быть только 'new' или 'delivered' |
| bodies_profile | role IN (...) | Роль выбирается из фиксированного набора |
| bodies_profile | user_id UNIQUE | Один пользователь = один профиль |

---

## Индексы

Автоматически создаются для:
- PRIMARY KEY во всех таблицах
- UNIQUE констреинтов (sku в products, user_id в profile)
- FOREIGN KEY связей

```sql
-- Просмотр индексов
\di

-- Дополнительный индекс для быстрого поиска по статусу
CREATE INDEX idx_order_status ON bodies_order(status);

-- Индекс для быстрого поиска заказов по пользователю
CREATE INDEX idx_order_user ON bodies_order(user_id);
```

---

## Каскадное удаление (Cascade Delete)

Если удалить пользователя (`DELETE FROM auth_user WHERE id = 1`):
1. Удалятся его профиль (bodies_profile)
2. Удалятся его заказы (bodies_order)
3. Удалятся записи о товарах в этих заказах (bodies_order_products)

ТОВАРЫ ОСТАНУТСЯ (bodies_product) - они не удаляются, могут быть в других заказах!

---

## Примеры сложных запросов

### Товары, которые ни разу не заказывали
```sql
SELECT p.*
FROM bodies_product p
LEFT JOIN bodies_order_products op ON p.id = op.product_id
WHERE op.id IS NULL;
```

### Пользователи, не сделавшие ни одного заказа
```sql
SELECT u.*
FROM auth_user u
LEFT JOIN bodies_order o ON u.id = o.user_id
WHERE o.id IS NULL;
```

### Заказы, которые неделю не доставлены
```sql
SELECT *
FROM bodies_order
WHERE status = 'new' 
  AND createdAt < NOW() - INTERVAL '7 days';
```

### Среднее количество товаров в заказе
```sql
SELECT AVG(items_per_order) as среднее
FROM (
    SELECT COUNT(*) items_per_order
    FROM bodies_order_products
    GROUP BY order_id
) subquery;
```

---

*Последнее обновление: февраль 2026*
