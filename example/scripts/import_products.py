#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Импорт товаров из CSV файла с изображениями"""

import os
import sys
import csv
import django
from pathlib import Path
from decimal import Decimal
from django.core.files.base import ContentFile

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from bodies.models import Product


def detect_encoding(file_path):
    """Определить кодировку файла"""
    for encoding in ['utf-8', 'utf-8-sig', 'cp1251', 'latin-1']:
        try:
            with open(file_path, 'r', encoding=encoding) as f:
                f.read(1024)
            return encoding
        except:
            continue
    return 'utf-8'


def import_csv(file_path):
    """Импортировать товары из CSV файла с изображениями"""
    encoding = detect_encoding(file_path)
    imported = 0
    errors = []
    
    with open(file_path, 'r', encoding=encoding) as f:
        sample = f.read(1024)
        f.seek(0)
        dialect = csv.Sniffer().sniff(sample, delimiters=',;\t')
        reader = csv.DictReader(f, dialect=dialect)
        
        for row_num, row in enumerate(reader, start=2):
            try:
                # Ищем столбцы
                name = next((row.get(k) for k in ['name', 'Название', 'название', 'Name'] if row.get(k)), None)
                sku = next((row.get(k) for k in ['sku', 'Артикул', 'артикул', 'SKU'] if row.get(k)), None)
                price = next((row.get(k) for k in ['price', 'Цена', 'цена', 'Price'] if row.get(k)), None)
                desc = next((row.get(k) for k in ['description', 'Описание', 'описание', 'Description'] if row.get(k)), None)
                image_path = next((row.get(k) for k in ['image', 'Изображение', 'изображение', 'Image', 'image_path', 'путь_изображения'] if row.get(k)), None)
                
                if not all([name, sku, price]):
                    errors.append(f"Строка {row_num}: недостаточно данных")
                    continue
                
                name = str(name).strip()
                sku = str(sku).strip()
                desc = (str(desc).strip() if desc else '')
                image_path = (str(image_path).strip() if image_path else None)
                
                try:
                    price = Decimal(str(price).replace(',', '.'))
                except:
                    errors.append(f"Строка {row_num}: неверная цена")
                    continue
                
                # Подготовка данных для создания/обновления
                product_data = {
                    'name': name,
                    'price': price,
                    'description': desc
                }
                
                # Обработка изображения если указано
                if image_path:
                    product_data['image'] = load_image_file(image_path, sku, row_num, errors)
                
                # Create or update
                product, created = Product.objects.update_or_create(
                    sku=sku,
                    defaults=product_data
                )
                
                status = "✓ Добавлен" if created else "♻️  Обновлен"
                img_status = " + 📸" if image_path else ""
                print(f"{status}{img_status}: {name} ({sku}) - {price} ₽")
                imported += 1
                
            except Exception as e:
                errors.append(f"Строка {row_num}: {str(e)}")
    
    return imported, errors


def load_image_file(image_path, sku, row_num, errors):
    """
    Загрузить файл изображения из пути (может быть абсолютный или относительный путь)
    
    Args:
        image_path: Путь к файлу изображения (абсолютный или относительный к data/)
        sku: SKU товара (для логирования)
        row_num: Номер строки в CSV (для логирования)
        errors: Список ошибок для добавления сообщений
    
    Returns:
        ImageFieldFile или None
    """
    if not image_path:
        return None
    
    # Проверить несколько возможных путей
    possible_paths = [
        Path(image_path),  # Абсолютный путь или путь от текущей директории
        Path('data') / image_path,  # Относительно папки data
        project_root / 'data' / image_path,  # Полный путь к папке data
        project_root / image_path,  # От корня проекта
    ]
    
    image_file = None
    for path in possible_paths:
        if path.exists() and path.is_file():
            image_file = path
            break
    
    if not image_file:
        errors.append(f"Строка {row_num} ({sku}): файл изображения не найден: {image_path}")
        return None
    
    # Проверить что это изображение
    valid_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp'}
    if image_file.suffix.lower() not in valid_extensions:
        errors.append(f"Строка {row_num} ({sku}): неподдерживаемый формат изображения: {image_file.suffix}")
        return None
    
    # Читаем файл и возвращаем
    try:
        with open(image_file, 'rb') as f:
            file_content = f.read()
        return ContentFile(file_content, name=image_file.name)
    except Exception as e:
        errors.append(f"Строка {row_num} ({sku}): ошибка при чтении изображения: {str(e)}")
        return None


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Использование: python import_products.py <файл.csv>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    
    if not os.path.exists(file_path):
        print(f"Ошибка: файл не найден: {file_path}")
        sys.exit(1)
    
    if not file_path.lower().endswith('.csv'):
        print("Ошибка: поддерживается только CSV формат")
        sys.exit(1)
    
    print(f"📂 Импортирование: {file_path}")
    print("-" * 40)
    
    imported, errors = import_csv(file_path)
    
    print("-" * 40)
    print(f"✅ Импортировано: {imported} товаров")
    if errors:
        print(f"\n⚠️  Ошибок: {len(errors)}")
        for error in errors[:10]:
            print(f"  • {error}")
        if len(errors) > 10:
            print(f"  ... и еще {len(errors) - 10} ошибок")
