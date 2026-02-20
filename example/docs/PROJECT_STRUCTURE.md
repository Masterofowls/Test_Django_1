# 📦 Структура проекта Django E-commerce

## 🗂️ Полная иерархия файлов

```
Test_Django_1/example/back/
│
├── 📖 Документация (главная папка)
│   └── README.md
│
├── 🎯 Django приложение
│   ├── manage.py                      # Django CLI (главная команда)
│   ├── requirements.txt               # Зависимости Python
│   ├── .gitignore                     # Git конфигурация
│   │
│   ├── config/                        # Настройки проекта
│   │   ├── __init__.py
│   │   ├── settings.py                # Конфиг БД, приложения
│   │   ├── urls.py                    # Главные маршруты
│   │   ├── asgi.py                    # ASGI сервер
│   │   └── wsgi.py                    # WSGI сервер
│   │
│   └── bodies/                        # Основное приложение Django
│       ├── __init__.py
│       ├── apps.py                    # Конфигурация приложения
│       ├── models.py                  # Модели БД (6 моделей)
│       ├── views.py                   # Представления и логика
│       ├── urls.py                    # Маршруты приложения
│       ├── admin.py                   # Админ-панель
│       ├── signals.py                 # Сигналы (автосоздание Profile)
│       ├── tests.py                   # Тесты
│       │
│       ├── templates/                 # HTML шаблоны (9 файлов)
│       │   ├── products.html          # Каталог товаров
│       │   ├── add_product.html       # Добавление товара
│       │   ├── edit_product.html      # Редактирование товара
│       │   ├── manage_users.html      # Управление пользователями
│       │   ├── edit_user_role.html    # Редактирование роли
│       │   ├── confirm_delete.html    # Подтверждение удаления
│       │   ├── login.html             # Вход в систему
│       │   ├── register.html          # Регистрация
│       │   └── order_list.html        # История заказов
│       │
│       ├── management/                # Django команды
│       │   └── commands/
│       │       └── setup.py           # Инициализация (тестовые данные)
│       │
│       └── migrations/                # Миграции БД
│           ├── __init__.py
│           ├── 0001_initial.py        # Создание всех таблиц
│           └── 0002_alter_profile_role.py
│
├── 📚 Документация
│   └── docs/
│       ├── README.md                  # Навигация по документам
│       ├── DBEAVER_GUIDE.md           # DBeaver и работа с БД
│       ├── IMPORT_GUIDE.md            # Импорт товаров
│       └── LOGIN_CREDENTIALS.md       # Пароли тестовых пользователей
│
├── 🔧 Скрипты
│   └── scripts/
│       ├── README.md                  # Описание скриптов
│       ├── import_products.py         # Импорт товаров из CSV/XLSX
│       └── create_xlsx_template.py    # Создание Excel шаблона
│
├── 📊 Данные
│   └── data/
│       ├── README.md                  # Описание данных
│       ├── products_template.csv      # Пример CSV (5 товаров)
│       └── products_template.xlsx     # Пример Excel (5 товаров)
│
└── 🐍 Окружение
    └── venv/                          # Виртуальное окружение (ИГНОРИРУЕТСЯ)
        └── ... (Python пакеты)
```

---

## 📋 Назначение каждой папки

### 📖 docs/ - Документация
```
docs/
├── README.md                 # Навигация по документам (НАЧНИТЕ ОТСЮДА!)
├── DBEAVER_GUIDE.md         # Как подключиться к БД и экспортировать диаграмму
├── IMPORT_GUIDE.md          # Инструкция по импорту товаров
└── LOGIN_CREDENTIALS.md     # Учетные данные тестовых пользователей
```

**Для кого?** Новые разработчики, тестировщики, демонстрация проекта

---

### 🔧 scripts/ - Утилиты
```
scripts/
├── README.md                      # Описание скриптов
├── import_products.py             # Импорт товаров
└── create_xlsx_template.py        # Создание шаблона Excel
```

**Для кого?** Как использовать скрипты и автоматизацию

---

### 📊 data/ - Примеры данных
```
data/
├── README.md                      # Описание примеров
├── products_template.csv          # CSV пример
└── products_template.xlsx         # Excel пример
```

**Для кого?** Тестирование и демонстрация импорта

---

### 🎯 Корневая структура example/
```
back/
├── manage.py                # Главная команда Django
├── requirements.txt         # Зависимости
├── .gitignore              # Что игнорировать в Git
├── config/                 # Конфигурация (settings, urls)
├── bodies/                  # Основное приложение (models, views, templates)
└── venv/                    # Виртуальное окружение (НЕ КОММИТИТЬ!)
```

**Для кого?** Разработчики при написании кода

---

## 🚀 Как начать работу с проектом

### Шаг 1: Понять структуру
→ Прочитайте главный [README.md](README.md)

### Шаг 2: Подготовить окружение
```bash
# Виртуальное окружение уже создано в venv/
venv\Scripts\activate

# Установить зависимости (если нужно)
pip install -r requirements.txt
```

### Шаг 3: Подключиться к БД
→ Следуйте [docs/DBEAVER_GUIDE.md](docs/DBEAVER_GUIDE.md)

### Шаг 4: Импортировать тестовые данные
→ Следуйте [docs/IMPORT_GUIDE.md](docs/IMPORT_GUIDE.md)

### Шаг 5: Запустить сервер
```bash
python manage.py runserver
# Открыть http://127.0.0.1:8000/
```

### Шаг 6: Залогиниться и тестировать
→ Пароли в [docs/LOGIN_CREDENTIALS.md](docs/LOGIN_CREDENTIALS.md)

---

## 📚 Таблица быстрых ссылок

| Что мне нужно? | Смотрите файл |
|---|---|
| 🎓 Учась работать с проектом | [docs/README.md](docs/README.md) |
| 🔌 Подключиться к БД | [docs/DBEAVER_GUIDE.md](docs/DBEAVER_GUIDE.md) |
| 📥 Импортировать товары | [docs/IMPORT_GUIDE.md](docs/IMPORT_GUIDE.md) |
| 🔐 Найти пароли | [docs/LOGIN_CREDENTIALS.md](docs/LOGIN_CREDENTIALS.md) |
| 🔧 Использовать скрипты | [scripts/README.md](scripts/README.md) |
| 📊 Понять примеры данных | [data/README.md](data/README.md) |
| 📋 Полная информация проекта | [README.md](README.md) |

---

## ✅ Файлы, которые НУЖНО коммитить в Git

- ✅ `config/` (Django конфигурация)
- ✅ `bodies/` (приложение с моделями, views, templates)
- ✅ `docs/` (документация)
- ✅ `scripts/` (скрипты)
- ✅ `data/` (примеры данных)
- ✅ `README.md` (главная документация)
- ✅ `requirements.txt` (зависимости)
- ✅ `.gitignore` (что игнорировать)
- ✅ `manage.py` (Django CLI)

---

## ❌ Файлы, которые НЕЛЬЗЯ коммитить в Git

- ❌ `venv/` (виртуальное окружение)
- ❌ `db.sqlite3` (локальная БД)
- ❌ `__pycache__/` (кэш Python)
- ❌ `*.pyc` (скомпилированный Python)
- ❌ `.env` (переменные окружения)
- ❌ `.idea/` (IDE конфигурация)

**Все эти файлы уже добавлены в `.gitignore`!**

---

## 🎓 Для экзамена

**Демонстрируйте в этом порядке:**

1. ✅ Структура проекта (эта папка)
2. ✅ Исходный код (bodies/ приложение)
3. ✅ БД диаграмма (экспортировать из DBeaver)
4. ✅ Админ-панель (http://127.0.0.1:8000/admin/)
5. ✅ Каталог товаров (http://127.0.0.1:8000/)
6. ✅ Систему ролей (разные аккаунты с разными правами)
7. ✅ Импорт товаров (использовать скрипт import_products.py)

---

## 📞 Быстрая помощь

**Вопрос:** Где установить Django?  
**Ответ:** `pip install -r requirements.txt` (все зависимости в одном файле)

**Вопрос:** Как запустить импорт товаров?  
**Ответ:** `python scripts/import_products.py data/products_template.csv`

**Вопрос:** Где хранятся пароли?  
**Ответ:** [docs/LOGIN_CREDENTIALS.md](docs/LOGIN_CREDENTIALS.md)

**Вопрос:** Как подключиться к БД?  
**Ответ:** [docs/DBEAVER_GUIDE.md](docs/DBEAVER_GUIDE.md)

**Вопрос:** Как модифицировать товары?  
**Ответ:** Админ-панель (http://127.0.0.1:8000/admin/) или через импорт

---

## 📊 Статистика проекта

- **Всего файлов:** ~50
- **Python файлов:** ~20
- **HTML шаблонов:** 9
- **Таблиц БД:** 6
- **Моделей Django:** 6
- **Views функций:** ~15
- **URL маршрутов:** ~10
- **Роли пользователей:** 4

---

## 🎉 Готово!

Проект полностью организован и готов к:
- ✅ Разработке
- ✅ Тестированию
- ✅ Демонстрации на экзамене
- ✅ Git коммитам

**Начните с чтения документации в папке `docs/`!**

---

**Дата организации:** 2026-02-20  
**Версия структуры:** 2.0  
**Статус:** ✅ Полностью организовано
