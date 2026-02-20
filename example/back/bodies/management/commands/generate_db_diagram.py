#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Django команда для генерации диаграммы базы данных
Использование: python manage.py generate_db_diagram
"""

from django.core.management.base import BaseCommand
from django.apps import apps
from django.db import models as django_models


class Command(BaseCommand):
    help = 'Генерирует диаграмму БД в форматах текст и Mermaid'

    def generate_mermaid_diagram(self):
        """Генерирует диаграмму ER в формате Mermaid"""
        
        diagram = "erDiagram\n"
        
        # Получаем все модели из приложения 'bodies'
        app_models = apps.get_app_config('bodies').get_models()
        
        for model in app_models:
            # Название модели
            model_name = model.__name__
            
            # Добавляем сущность
            diagram += f'\n    {model_name} {{\n'
            
            # Получаем все поля
            for field in model._meta.get_fields():
                # Пропускаем reverse отношения
                if isinstance(field, django_models.ManyToOneRel):
                    continue
                if isinstance(field, django_models.ManyToManyRel):
                    continue
                if isinstance(field, django_models.OneToOneRel):
                    continue
                
                # Имя и тип поля
                field_name = field.name
                field_type = field.get_internal_type()
                
                # Форматируем тип для читаемости
                type_display = {
                    'AutoField': 'int',
                    'BigAutoField': 'bigint',
                    'CharField': 'string',
                    'TextField': 'text',
                    'DecimalField': 'decimal',
                    'IntegerField': 'int',
                    'BooleanField': 'boolean',
                    'DateTimeField': 'datetime',
                    'ForeignKey': 'int (FK)',
                    'OneToOneField': 'int (1-1)',
                    'ManyToManyField': 'many-to-many',
                }.get(field_type, field_type)
                
                # Добавляем информацию о обязательности
                if field.null:
                    type_display += ' "nullable"'
                
                diagram += f'        {field_name} {type_display}\n'
            
            diagram += '    }\n'
        
        # Добавляем связи
        diagram += '\n    %% Связи (relationships)\n'
        
        for model in app_models:
            for field in model._meta.get_fields():
                if isinstance(field, django_models.ForeignKey):
                    from_model = model.__name__
                    to_model = field.related_model.__name__
                    diagram += f'    {from_model} ||--o| {to_model} : "{field.name}"\n'
                
                elif isinstance(field, django_models.OneToOneField):
                    from_model = model.__name__
                    to_model = field.related_model.__name__
                    diagram += f'    {from_model} ||--|| {to_model} : "{field.name}"\n'
                
                elif isinstance(field, django_models.ManyToManyField):
                    from_model = model.__name__
                    to_model = field.related_model.__name__
                    diagram += f'    {from_model} }}o--o{{ {to_model} : "{field.name}"\n'
        
        return diagram

    def generate_text_diagram(self):
        """Генерирует текстовую диаграмму всех моделей"""
        
        output = "\n" + "=" * 70
        output += "\n📊 ДИАГРАММА БАЗЫ ДАННЫХ\n"
        output += "=" * 70 + "\n"
        
        app_models = apps.get_app_config('bodies').get_models()
        
        for model in app_models:
            output += f"\n📦 Модель: {model.__name__}\n"
            output += f"{'─' * 70}\n"
            
            # Таблица базы данных
            output += f"Таблица: {model._meta.db_table}\n\n"
            
            # Поля
            output += "Поля:\n"
            for field in model._meta.get_fields():
                # Пропускаем reverse отношения
                if isinstance(field, (django_models.ManyToOneRel, 
                                     django_models.ManyToManyRel,
                                     django_models.OneToOneRel)):
                    continue
                
                field_info = f"  • {field.name}"
                field_type = field.get_internal_type()
                
                # Тип поля
                field_info += f" ({field_type})"
                
                # Дополнительная информация
                if isinstance(field, django_models.ForeignKey):
                    field_info += f" → связь на {field.related_model.__name__}"
                elif isinstance(field, django_models.OneToOneField):
                    field_info += f" → взаимосвязь 1-1 с {field.related_model.__name__}"
                elif isinstance(field, django_models.ManyToManyField):
                    field_info += f" → связь многие-ко-многим с {field.related_model.__name__}"
                
                # Обязательность
                if field.primary_key:
                    field_info += " [PRIMARY KEY]"
                elif not field.null and not hasattr(field, 'default'):
                    field_info += " [REQUIRED]"
                
                # Максимальная длина (для CharField)
                if hasattr(field, 'max_length') and field.max_length:
                    field_info += f" (max: {field.max_length})"
                
                output += field_info + "\n"
            
            # Связи обратные
            reverse_relations = [f for f in model._meta.get_fields() 
                                if isinstance(f, (django_models.ManyToOneRel,
                                                 django_models.ManyToManyRel,
                                                 django_models.OneToOneRel))]
            
            if reverse_relations:
                output += "\nОбратные связи:\n"
                for rel in reverse_relations:
                    if isinstance(rel, django_models.ManyToOneRel):
                        output += f"  • {rel.related_model.__name__}.{rel.get_accessor_name()} (один-ко-многим)\n"
                    elif isinstance(rel, django_models.ManyToManyRel):
                        output += f"  • {rel.related_model.__name__}.{rel.get_accessor_name()} (многие-ко-многим)\n"
                    elif isinstance(rel, django_models.OneToOneRel):
                        output += f"  • {rel.related_model.__name__}.{rel.get_accessor_name()} (один-к-одному)\n"
            
            # Meta информация
            output += f"\nУпорядочивание по умолчанию: {model._meta.ordering if model._meta.ordering else 'Нет'}\n"
            
        output += "\n" + "=" * 70 + "\n"
        return output

    def handle(self, *args, **options):
        """Главная обработчик команды"""
        self.stdout.write(self.style.SUCCESS("🔧 Генератор диаграмм базы данных\n"))
        
        # Генерируем текстовую диаграмму
        text_diagram = self.generate_text_diagram()
        self.stdout.write(text_diagram)
        
        # Сохраняем в файл
        with open('DATABASE_DIAGRAM.txt', 'w', encoding='utf-8') as f:
            f.write(text_diagram)
        self.stdout.write(self.style.SUCCESS("✓ Текстовая диаграмма сохранена в: DATABASE_DIAGRAM.txt\n"))
        
        # Генерируем Mermaid диаграмму
        mermaid_diagram = self.generate_mermaid_diagram()
        
        # Сохраняем в файл
        with open('DATABASE_ER_DIAGRAM.md', 'w', encoding='utf-8') as f:
            f.write("# 📊 Диаграмма Entity-Relationship (ER)\n\n")
            f.write("```mermaid\n")
            f.write(mermaid_diagram)
            f.write("```\n\n")
            f.write("## Обозначения\n")
            f.write("- `||--o|` - один-ко-многим (1..N)\n")
            f.write("- `||--|` - один-к-одному (1..1)\n")
            f.write("- `}o--o{` - многие-ко-многим (M..N)\n")
        
        self.stdout.write(self.style.SUCCESS("✓ Mermaid диаграмма сохранена в: DATABASE_ER_DIAGRAM.md\n"))
        
        self.stdout.write(self.style.WARNING("📁 Файлы:\n"))
        self.stdout.write("  • DATABASE_DIAGRAM.txt - подробная текстовая схема\n")
        self.stdout.write("  • DATABASE_ER_DIAGRAM.md - визуальная ER диаграмма (для просмотра в GitHub/IDE)\n")
