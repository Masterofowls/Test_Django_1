import csv
from decimal import Decimal
from django.core.management.base import BaseCommand
from bodies.models import Product


class Command(BaseCommand):
    help = 'Импортирует товары из CSV файла'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='Путь к CSV-файлу')

    def detect_encoding(self, file_path):
        for encoding in ['utf-8', 'utf-8-sig', 'cp1251', 'latin-1']:
            try:
                with open(file_path, 'r', encoding=encoding) as f:
                    f.read(1024)
                return encoding
            except:
                continue
        return 'utf-8'

    def handle(self, *args, **options):
        file_path = options['file_path']
        
        try:
            encoding = self.detect_encoding(file_path)
            imported = 0
            
            with open(file_path, 'r', encoding=encoding) as f:
                sample = f.read(1024)
                f.seek(0)
                dialect = csv.Sniffer().sniff(sample, delimiters=',;\t')
                reader = csv.DictReader(f, dialect=dialect)
                
                for row_num, row in enumerate(reader, start=2):
                    try:
                        name = next((row.get(k) for k in ['name', 'Название', 'название', 'Name'] if row.get(k)), None)
                        sku = next((row.get(k) for k in ['sku', 'Артикул', 'артикул', 'SKU'] if row.get(k)), None)
                        price = next((row.get(k) for k in ['price', 'Цена', 'цена', 'Price'] if row.get(k)), None)
                        desc = next((row.get(k) for k in ['description', 'Описание', 'описание', 'Description'] if row.get(k)), None)
                        
                        if not all([name, sku, price]):
                            continue
                        
                        name = str(name).strip()
                        sku = str(sku).strip()
                        desc = (str(desc).strip() if desc else '')
                        price = Decimal(str(price).replace(',', '.'))
                        
                        Product.objects.update_or_create(
                            sku=sku,
                            defaults={'name': name, 'price': price, 'description': desc}
                        )
                        imported += 1
                        self.stdout.write(f'✓ {name} ({sku})')
                        
                    except:
                        continue
            
            self.stdout.write(self.style.SUCCESS(f'\n✅ Импортировано: {imported} товаров'))
            
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f'❌ Файл не найден: {file_path}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Ошибка: {str(e)}'))
