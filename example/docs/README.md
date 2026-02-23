# 🛍️ Django E-commerce - Интернет-магазин

**Демонстрационный экзамен по специальности 09.02.07 — Инфраструктура информационных технологий**

Полностью готовый Django проект для управления интернет-магазином с системой заказов, доставкой на пункты выдачи и четырёхуровневой системой ролей пользователей.

---

## 📚 Документация

| Документ | Описание |
|----------|---------|
| 📖 **[README.md](docs/)** | Главная документация проекта |
| 🏗️ **[BUILD_FROM_SCRATCH.md](docs/BUILD_FROM_SCRATCH.md)** | Полная сборка проекта с нуля — от установки до запуска |
| 🔌 **[DBEAVER_GUIDE.md](docs/DBEAVER_GUIDE.md)** | Как подключиться к БД через DBeaver и экспортировать диаграмму |
| 📥 **[IMPORT_GUIDE.md](docs/IMPORT_GUIDE.md)** | Инструкция для импорта товаров из CSV/XLSX |
| 🔐 **[LOGIN_CREDENTIALS.md](docs/LOGIN_CREDENTIALS.md)** | Учетные данные тестовых пользователей |

---

## 🚀 Быстрый старт (2 минуты)

### 1. Создать виртуальное окружение

```bash
python -m venv venv
venv\Scripts\activate
```

### 2. Установить зависимости

```bash
pip install django==6.0.1 psycopg2-binary openpyxl
```

### 3. Создать базу данных

В DBeaver или psql:
```sql
CREATE DATABASE shop;
```

### 4. Миграции

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Создать админа

```bash
python manage.py createsuperuser
# Username: admin
# Password: (введите пароль)
```

### 6. Запустить сервер

```bash
python manage.py runserver
```

Открыть: `http://127.0.0.1:8000/`

---

## 📂 Структура проекта

```
back/
├── docs/                          # 📖 Документация
│   ├── DBEAVER_GUIDE.md          # Как работать с БД через DBeaver
│   ├── IMPORT_GUIDE.md           # Импорт товаров из CSV/XLSX
│   └── LOGIN_CREDENTIALS.md      # Учетные данные тестовых пользователей
│
├── scripts/                       # 🔧 Скрипты и утилиты
│   ├── import_products.py        # Импорт товаров из файла
│   └── create_xlsx_template.py   # Создание шаблона Excel
│
├── data/                          # 📊 Примеры данных
│   ├── products_template.csv     # Пример CSV с товарами
│   └── products_template.xlsx    # Пример Excel шаблона
│
├── config/                    # ⚙️ Конфигурация Django
│   ├── settings.py               # Настройки проекта
│   ├── urls.py                   # Главные маршруты
│   ├── asgi.py
│   └── wsgi.py
│
├── bodies/                        # 🎯 Основное приложение
│   ├── models.py                 # Модели БД (User, Product, Order и т.д.)
│   ├── views.py                  # Представления и контроллеры
│   ├── urls.py                   # Маршруты приложения
│   ├── admin.py                  # Админ-панель
│   ├── signals.py                # Сигналы Django (создание Profile)
│   ├── apps.py                   # Конфигурация приложения
│   ├── templates/                # HTML шаблоны
│   │   ├── products.html         # Каталог товаров
│   │   ├── add_product.html      # Добавление товара (admin)
│   │   ├── edit_product.html     # Редактирование товара
│   │   ├── manage_users.html     # Управление пользователями
│   │   ├── edit_user_role.html   # Редактирование роли
│   │   └── confirm_delete.html   # Подтверждение удаления
│   ├── management/commands/      # Django команды
│   │   └── setup.py              # Инициализация системы (тестовые данные)
│   └── migrations/               # Миграции БД
│
├── manage.py                      # Django CLI
├── requirements.txt               # Зависимости Python

---

## � Технологии

| Технология | Версия | Роль |
|-----------|--------|------|
| **Django** | 6.0.1 | Web фреймворк |
| **PostgreSQL** | 12+ | База данных |
| **Python** | 3.12+ | Язык программирования |
| **psycopg** | 3.1.18 | Драйвер PostgreSQL |
| **openpyxl** | 3.1.5 | Работа с Excel файлами |

---

## 👥 Система ролей (4 уровня)

```
┌──────────────┬─────────────────────────────────────┐
│ Роль         │ Доступ                              │
├──────────────┼─────────────────────────────────────┤
│ 👻 Anonymous │ Просмотр каталога (без фильтров)   │
│ 👤 User      │ Фильтрация товаров, заказы         │
│ ✏️  Editor    │ Редактирование товаров             │
│ 👑 Admin     │ Полные права (управление всем)     │
└──────────────┴─────────────────────────────────────┘
```

---

## 🗄️ Модели БД

- ✅ **Каталог товаров** — показ всех доступных товаров
- ✅ **Аутентификация** — регистрация и вход пользователей
- ✅ **Заказы** — пользователи могут заказать товар
- ✅ **История заказов** — просмотр своих заказов со статусом
- ✅ **Админ-панель** — управление товарами, заказами, пользователями
- ✅ **Импорт товаров** — загрузка товаров из Excel

---

## 📊 Модели БД

| Модель | Описание |
|--------|----------|
| **User** | Пользователь (встроенная в Django) |
| **Product** | Товар (name, price, sku, description) |
| **PickupPoint** | Пункт выдачи (address) |
| **Order** | Заказ (user, products, status, receiveCode) |
| **Profile** | Профиль пользователя (role) |

---

## 🔗 URL-маршруты

| URL | Назначение |
|-----|-----------|
| `/` | Каталог товаров |
| `/register/` | Регистрация пользователя |
| `/login/` | Вход в систему |
| `/logout/` | Выход из системы |
| `/orders/` | История заказов (защищено) |
| `/buy/<id>/<point>/` | Создать заказ (защищено) |
| `/admin/` | Админ-панель |

---

## 🔐 Аутентификация

- **Незащищённые:** `/`, `/register/`, `/login/`, `/admin/`
- **Защищённые:** `/orders/`, `/buy/...` (требуют логин)

---

## 📥 Импорт товаров

Из Excel файла (Tovar.xlsx):

```bash
python manage.py import_products "path/to/Tovar.xlsx"
```

Требуемые колонки в Excel:
- `Артикул` → SKU
- `Наименование товара` → Name
- `Цена` → Price
- `Описание товара` → Description

---

## ✅ Проверка работоспособности

```bash
# Синтаксис и конфигурация
python manage.py check

# Подключение к БД
python manage.py dbshell
\q

# Запуск сервера
python manage.py runserver

# Открыть браузер
# http://127.0.0.1:8000/
# http://127.0.0.1:8000/admin/
```

---

## 🔍 SQL Примеры

```sql
-- Все товары
SELECT * FROM bodies_product;

-- Заказы пользователя
SELECT * FROM bodies_order WHERE user_id = 1;

-- Товары в заказе
SELECT p.name FROM bodies_product p
JOIN bodies_order_products op ON p.id = op.product_id
WHERE op.order_id = 1;
```

---

## 🎓 Для экзамена

1. **Проверить что всё работает:** `python manage.py check`
2. **Создать администратора:** `python manage.py createsuperuser`
3. **Запустить сервер:** `python manage.py runserver`
4. **Показать админ-панель:** http://127.0.0.1:8000/admin/
5. **Показать каталог:** http://127.0.0.1:8000/
6. **Показать регистрацию:** http://127.0.0.1:8000/register/
7. **Показать заказы:** http://127.0.0.1:8000/orders/

---

**Полностью готовый проект к демонстрации и сдаче экзамена! ✅**
