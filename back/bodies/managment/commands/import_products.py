import csv

from django.core.management.base import BaseCommand

from bodies.models import Product
# Артикул	Наименование товара	Единица измерения	Цена	Поставщик	Производитель	Категория товара	Действующая скидка	Кол-во на складе	Описание товара	Фото

class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument("file_path", type=str)

    def handle(self, *args, **options):
        file_path = options["file_path"]

        mapping = {
            "Артикул": "sku",
            "Наименование товара": "name",
            "Цена": "price",
            "Описание товара": "description"
        }   

        try: 
            with open(file_path, mode="r", encoding="utf-8") as f:
                reader = csv.DictReader(f, delimiter=";")

                count = 0
                for row in reader:
                    obj, created = Product.objects.update_or_create(
                        sku=row["Артикул"],
                        defaults={
                            "name": row["Наименование товара"],
                            "price": row["Цена"].replace(",", "."),
                            "description": row.get("Описание товара", ""),

                        }
                    )
                    count += 1

                self.stdout.write(self.style.SUCCESS(f"success: {count}"))

            
        except FileExistsError, FileNotFoundError:
            self.stdout.write(self.style.ERROR(f"error"))
