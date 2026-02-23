#!/usr/bin/env python
import csv
import os
import sys
from decimal import Decimal
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

import django

django.setup()

from bodies.models import Product

COLUMNS = {
    'name': ['name', 'Название', 'название'],
    'sku': ['sku', 'Артикул', 'артикул'],
    'price': ['price', 'Цена', 'цена'],
    'description': ['description', 'Описание', 'описание'],
}


def find_col(row, key):
    return next((row[k].strip() for k in COLUMNS[key] if row.get(k, '').strip()), None)


def import_csv(file_path):
    for enc in ['utf-8-sig', 'utf-8', 'cp1251', 'latin-1']:
        try:
            open(file_path, encoding=enc).read(1024)
            break
        except (UnicodeDecodeError, UnicodeError):
            enc = 'utf-8'

    with open(file_path, encoding=enc) as f:
        dialect = csv.Sniffer().sniff(f.read(1024), delimiters=',;\t')
        f.seek(0)
        imported = 0

        for i, row in enumerate(csv.DictReader(f, dialect=dialect), 2):
            name, sku, price = find_col(row, 'name'), find_col(row, 'sku'), find_col(row, 'price')
            if not all([name, sku, price]):
                continue
            try:
                price = Decimal(price.replace(',', '.'))
            except Exception:
                continue

            _, created = Product.objects.update_or_create(
                sku=sku,
                defaults={'name': name, 'price': price, 'description': find_col(row, 'description') or ''}
            )
            imported += 1

    return imported


if __name__ == '__main__':
    print(import_csv(sys.argv[1]))

