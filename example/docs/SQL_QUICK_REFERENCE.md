# ⚡ SQL Quick Reference (Одна страница)

**Для печати - экономия: настроить на одну станицу (File → Print → Fit to page)**

---

## 🔗 Подключение
```bash
psql -U postgres -d shop -h localhost
```

---

## 📦 ТОВАРЫ (bodies_product)

| Операция | SQL |
|----------|-----|
| Все товары | `SELECT * FROM bodies_product;` |
| Найти | `SELECT * FROM bodies_product WHERE sku = 'ABC';` |
| Добавить | `INSERT INTO bodies_product (name, sku, price) VALUES ('Name', 'SKU', 99);` |
| Обновить цену | `UPDATE bodies_product SET price = 99 WHERE sku = 'SKU';` |
| Удалить | `DELETE FROM bodies_product WHERE sku = 'SKU';` |

---

## 👥 ПОЛЬЗОВАТЕЛИ (auth_user + bodies_profile)

| Операция | SQL |
|----------|-----|
| Все юзеры | `SELECT u.*, p.role FROM auth_user u LEFT JOIN bodies_profile p ON u.id = p.user_id;` |
| Админы | `SELECT * FROM auth_user u JOIN bodies_profile p ON u.id = p.user_id WHERE p.role = 'admin';` |
| Редакторы | `SELECT * FROM auth_user u JOIN bodies_profile p ON u.id = p.user_id WHERE p.role IN ('editor','admin');` |
| Назначить админ | `UPDATE bodies_profile SET role = 'admin' WHERE user_id = 5;` |
| Деактивировать | `UPDATE auth_user SET is_active = false WHERE username = 'user';` |

---

## 🛒 ЗАКАЗЫ (bodies_order)

| Операция | SQL |
|----------|-----|
| Все заказы | `SELECT * FROM bodies_order ORDER BY createdAt DESC;` |
| Заказы юзера | `SELECT * FROM bodies_order WHERE user_id = 1;` |
| Новые | `SELECT * FROM bodies_order WHERE status = 'new';` |
| Товары в заказе | `SELECT p.* FROM bodies_order_products op JOIN bodies_product p ON op.product_id = p.id WHERE op.order_id = 1;` |
| Создать | `INSERT INTO bodies_order (user_id, createdAt, receiveCode, status) VALUES (1, NOW(), 'CODE', 'new');` |
| Добавить товар | `INSERT INTO bodies_order_products (order_id, product_id) VALUES (1, 5);` |
| Отметить доставлен | `UPDATE bodies_order SET status = 'delivered', deliveryDate = NOW() WHERE id = 1;` |
| Удалить | `DELETE FROM bodies_order WHERE id = 1;` |

---

## 📊 СТАТИСТИКА

| Запрос | SQL |
|--------|-----|
| Кол-во товаров | `SELECT COUNT(*) FROM bodies_product;` |
| Средняя цена | `SELECT AVG(price) FROM bodies_product;` |
| Макс/мин цена | `SELECT MAX(price), MIN(price) FROM bodies_product;` |
| Кол-во заказов | `SELECT COUNT(*) FROM bodies_order;` |
| Новые заказы | `SELECT COUNT(*) FROM bodies_order WHERE status = 'new';` |
| Популярные товары | `SELECT p.name, COUNT(*) as times FROM bodies_product p JOIN bodies_order_products op ON p.id = op.product_id GROUP BY p.id ORDER BY COUNT(*) DESC LIMIT 10;` |

---

## 🔍 ФИЛЬТРЫ

```sql
WHERE price > 100           -- больше
WHERE price < 100           -- меньше  
WHERE price BETWEEN 10 AND 100  -- диапазон
WHERE name ILIKE '%iPhone%' -- содержит текст
WHERE status = 'new'        -- точное совпадение
WHERE user_id IS NULL       -- пусто
WHERE createdAt >= NOW() - INTERVAL '7 days'  -- за неделю
```

---

## 🎯 СОРТИРОВКА & ЛИМИТ

```sql
ORDER BY price DESC         -- дороже первыми
ORDER BY price ASC          -- дешевле первыми
ORDER BY createdAt DESC     -- новейшие первыми
LIMIT 10                    -- первые 10
LIMIT 10 OFFSET 20          -- пропустить 20, взять 10
```

---

## 🔑 ОСНОВНЫЕ ТАБЛИЦЫ

| Таблица | Колонки |
|---------|---------|
| **products** | id, name, price, sku, description |
| **orders** | id, user_id, status, createdAt, deliveryDate |
| **users** | id, username, email, password |
| **profiles** | id, user_id, role |
| **pickuppoints** | id, address |

---

## ⚙️ НАСТРОЙКА

```
Хост: localhost
Порт: 5432
БД: shop
Пользователь: postgres
Пароль: postgres
```

---

## 📌 DBeaver команды

- **Ctrl+Enter** - выполнить запрос
- **Ctrl+Shift+F** - форматировать SQL
- **Ctrl+Alt+N** - новый SQL скрипт
- **Правый клик на таблице** → View Data

---

## ✅ Типичный рабочий процесс

1. **Напишите SELECT** - проверьте какие строки
2. **Используйте WHERE** - фильтруйте нужные
3. **Напишите UPDATE/DELETE** - делайте изменение
4. **Выполните в DBeaver** или `psql`
5. **SELECT снова** - подтвердите изменения

---

## ⚠️ Помните!

- ✅ Делайте бэкап перед крупными операциями
- ✅ Проверяйте SELECT перед DELETE
- ❌ Не удаляйте django_* таблицы
- ❌ Не редактируйте пароли вручную

---

**📚 Полная документация: [SQL_DOCUMENTATION_INDEX.md](SQL_DOCUMENTATION_INDEX.md)**

*Напечатайте эту страницу —她очень поможет!* 🎯
