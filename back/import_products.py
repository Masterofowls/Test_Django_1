import os, csv, django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'back.settings')
django.setup()
from bodies.models import Product

def import_csv():

    file_path = 'products.csv'
    with open(file_path, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter=';') 
        for row in reader:
            Product.objects.create(
                sku=row['Артикул_в_файле'],
                name=row['Название_в_файле'],
                price=row['Цена_в_файле'],
                description=row.get('Описание_в_файле', '')
            )
if __name__ == '__main__':
    import_csv()