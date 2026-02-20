#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Скрипт для импорта товаров из CSV и XLSX файлов
Поддерживает кодировку UTF-8 и CP1251 (Windows-1251)
"""

import os
import sys
import csv
import django
from pathlib import Path
from decimal import Decimal

# Добавляем корень проекта в Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Установка Django окружения
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from bodies.models import Product


def detect_encoding(file_path):
    """Определить кодировку файла"""
    encodings = ['utf-8', 'utf-8-sig', 'cp1251', 'latin-1', 'iso-8859-5']
    
    for encoding in encodings:
        try:
            with open(file_path, 'r', encoding=encoding) as f:
                f.read()
            print(f"✓ Обнаружена кодировка: {encoding}")
            return encoding
        except (UnicodeDecodeError, UnicodeError):
            continue
    
    print("✗ Не удалось определить кодировку файла")
    return None


def import_from_csv(file_path):
    """Импортировать товары из CSV файла"""
    encoding = detect_encoding(file_path)
    if not encoding:
        return 0
    
    imported_count = 0
    errors = []
    
    try:
        with open(file_path, 'r', encoding=encoding) as csvfile:
            # Пытаемся определить разделитель
            sample = csvfile.read(1024)
            csvfile.seek(0)
            
            dialect = csv.Sniffer().sniff(sample, delimiters=',;\t')
            reader = csv.DictReader(csvfile, dialect=dialect)
            
            # Нормализуем названия столбцов
            if reader.fieldnames:
                print(f"\n📋 Найдены столбцы: {', '.join(reader.fieldnames)}")
            
            for row_num, row in enumerate(reader, start=2):
                try:
                    # Ищем столбцы с разными возможными названиями
                    name = row.get('name') or row.get('Название') or row.get('название') or row.get('Name')
                    sku = row.get('sku') or row.get('Артикул') or row.get('артикул') or row.get('SKU')
                    price = row.get('price') or row.get('Цена') or row.get('цена') or row.get('Price')
                    description = row.get('description') or row.get('Описание') or row.get('описание') or row.get('Description')
                    
                    # Валидация
                    if not name or not sku or not price:
                        errors.append(f"Строка {row_num}: Отсутствуют обязательные поля (название, артикул, цена)")
                        continue
                    
                    # Очистка данных
                    name = str(name).strip()
                    sku = str(sku).strip()
                    description = (str(description) if description else '').strip()
                    
                    # Преобразование цены
                    try:
                        price = Decimal(str(price).replace(',', '.'))
                    except:
                        errors.append(f"Строка {row_num}: Некорректная цена: {price}")
                        continue
                    
                    # Проверка дубликатов
                    if Product.objects.filter(sku=sku).exists():
                        existing = Product.objects.get(sku=sku)
                        existing.name = name
                        existing.price = price
                        existing.description = description
                        existing.save()
                        print(f"  ♻️  Обновлен товар: {name} ({sku})")
                    else:
                        Product.objects.create(
                            name=name,
                            sku=sku,
                            price=price,
                            description=description
                        )
                        print(f"  ✓ Добавлен товар: {name} ({sku}) - {price} ₽")
                    
                    imported_count += 1
                    
                except Exception as e:
                    errors.append(f"Строка {row_num}: {str(e)}")
                    continue
        
        return imported_count, errors
        
    except Exception as e:
        print(f"✗ Ошибка при чтении CSV файла: {str(e)}")
        return 0, [str(e)]


def import_from_xlsx(file_path):
    """Импортировать товары из XLSX файла"""
    try:
        import openpyxl
    except ImportError:
        print("✗ Модуль openpyxl не установлен. Установите: pip install openpyxl")
        return 0, []
    
    imported_count = 0
    errors = []
    
    try:
        workbook = openpyxl.load_workbook(file_path)
        worksheet = workbook.active
        
        # Получаем заголовки
        headers = {}
        for col_num, cell in enumerate(worksheet[1], start=1):
            headers[col_num] = str(cell.value).strip() if cell.value else ''
        
        print(f"\n📋 Найдены столбцы: {', '.join(str(v) for v in headers.values() if v)}")
        
        # Ищем нужные столбцы
        name_col = None
        sku_col = None
        price_col = None
        desc_col = None
        
        for col_num, header in headers.items():
            header_lower = header.lower()
            if 'назв' in header_lower or 'name' in header_lower:
                name_col = col_num
            elif 'артикул' in header_lower or 'sku' in header_lower:
                sku_col = col_num
            elif 'цена' in header_lower or 'price' in header_lower:
                price_col = col_num
            elif 'описа' in header_lower or 'description' in header_lower:
                desc_col = col_num
        
        if not (name_col and sku_col and price_col):
            errors.append("Не найдены необходимые столбцы (Название, Артикул, Цена)")
            return 0, errors
        
        # Импорт данных
        for row_num, row in enumerate(worksheet.iter_rows(min_row=2), start=2):
            try:
                name = str(row[name_col - 1].value).strip() if row[name_col - 1].value else ''
                sku = str(row[sku_col - 1].value).strip() if row[sku_col - 1].value else ''
                price = row[price_col - 1].value
                description = str(row[desc_col - 1].value).strip() if desc_col and row[desc_col - 1].value else ''
                
                # Валидация
                if not name or not sku or price is None:
                    errors.append(f"Строка {row_num}: Отсутствуют обязательные поля")
                    continue
                
                # Преобразование цены
                try:
                    price = Decimal(str(price).replace(',', '.'))
                except:
                    errors.append(f"Строка {row_num}: Некорректная цена: {price}")
                    continue
                
                # Проверка дубликатов
                if Product.objects.filter(sku=sku).exists():
                    existing = Product.objects.get(sku=sku)
                    existing.name = name
                    existing.price = price
                    existing.description = description
                    existing.save()
                    print(f"  ♻️  Обновлен товар: {name} ({sku})")
                else:
                    Product.objects.create(
                        name=name,
                        sku=sku,
                        price=price,
                        description=description
                    )
                    print(f"  ✓ Добавлен товар: {name} ({sku}) - {price} ₽")
                
                imported_count += 1
                
            except Exception as e:
                errors.append(f"Строка {row_num}: {str(e)}")
                continue
        
        workbook.close()
        return imported_count, errors
        
    except Exception as e:
        errors.append(f"Ошибка при чтении XLSX: {str(e)}")
        return 0, errors


def main():
    """Главная функция"""
    print("=" * 60)
    print("📦 Импортер товаров из CSV и XLSX файлов")
    print("=" * 60)
    
    # Получаем путь к файлу
    if len(sys.argv) < 2:
        print("\nИспользование: python import_products.py <путь_к_файлу>")
        print("\nПримеры:")
        print("  python import_products.py products.csv")
        print("  python import_products.py products.xlsx")
        print("  python import_products.py D:/files/products.csv")
        return
    
    file_path = sys.argv[1]
    
    # Проверяем существование файла
    if not os.path.exists(file_path):
        print(f"✗ Файл не найден: {file_path}")
        return
    
    file_ext = Path(file_path).suffix.lower()
    
    print(f"\n📂 Файл: {file_path}")
    print(f"📄 Расширение: {file_ext}")
    
    imported_count = 0
    errors = []
    
    if file_ext == '.csv':
        print("\n🔄 Импорт из CSV...")
        imported_count, errors = import_from_csv(file_path)
    elif file_ext in ['.xlsx', '.xls']:
        print("\n🔄 Импорт из XLSX...")
        imported_count, errors = import_from_xlsx(file_path)
    else:
        print(f"✗ Неподдерживаемый формат: {file_ext}")
        print("Поддерживаемые форматы: .csv, .xlsx, .xls")
        return
    
    # Результаты
    print("\n" + "=" * 60)
    print(f"✅ Успешно импортировано: {imported_count} товаров")
    
    if errors:
        print(f"\n⚠️  Ошибок: {len(errors)}")
        for error in errors[:10]:  # Показываем первые 10 ошибок
            print(f"  • {error}")
        if len(errors) > 10:
            print(f"  ... и еще {len(errors) - 10} ошибок")
    
    print("=" * 60)


if __name__ == '__main__':
    main()
