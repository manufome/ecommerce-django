from django.core.management.base import BaseCommand
from django.core.management import call_command
from apps.shop.models import Category, Brand, Product, ProductImage, Wishlist
from django.contrib.auth.models import User
import pandas as pd
import random
import os
from django.utils import timezone

class Command(BaseCommand):
    help = 'Populates the database with product data from a CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Path to the CSV file with product data')

    def handle(self, *args, **kwargs):
        csv_file = kwargs['csv_file']
        try:
            data = pd.read_csv(csv_file, delimiter=';')
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR('File not found!'))
            return
        data.drop_duplicates(subset='producto', keep='first', inplace=True)
        data.dropna(subset=['imagen'], inplace=True)

        self.stdout.write("Starting to populate the database...")

        call_command('clear_shop')
        self.stdout.write("Cleared existing data")

        categories = set(data['categoria'].unique())
        subcategories = set(data['subcategoria'].unique()) 
        subcategory_objs = {}

        for category in categories:
            category_obj = Category.objects.create(name=category, slug=category.lower().replace(' ', '-'))

            subcategories = set(data[data['categoria'] == category]['subcategoria'].unique())
            for subcategory in subcategories:
                subcategory_obj = Category.objects.create(name=subcategory, slug=subcategory.lower().replace(' ', '-'), parent=category_obj)
                subcategory_objs[subcategory] = subcategory_obj

        brands = ['Marca 1', 'Marca 2', 'Marca 3']
        brand_objs = {name: Brand.objects.create(name=name, slug=name.lower().replace(' ', '-')) for name in brands}
        user = User.objects.first()

        # create admin if not exists
        if not user:
            user = User.objects.create_superuser('admin', 'admin@admin.com', 'admin')

        # Crear productos
        for _, row in data.iterrows():
            category = subcategory_objs[row['subcategoria']]
            brand = random.choice(list(brand_objs.values()))
            discount = random.randint(0, 25)
            naive_discount_end_date = None if discount == 0 else pd.Timestamp.now() + pd.Timedelta(days=random.randint(1, 30))
            discount_end_date = None if discount == 0 else timezone.make_aware(naive_discount_end_date)
            product = Product(
                name=row['producto'],
                slug=row['producto'].lower().replace(' ', '-').replace('/', '-').replace('.', ''),
                description=f"Descripción de {row['producto']}",
                price = round(int(row['precio'].split(' ')[1].replace('.', '').strip()) / 50) * 50,
                discount=discount,
                discount_end_date=discount_end_date,
                stock=random.randint(0, 100),
                is_new=random.choice([True, False]),
                is_top=random.choice([True, False]),
                is_featured=random.choice([True, False]),
                ratings=random.randint(0, 5),
                reviews_count=random.randint(0, 100),
                category=category,
                brand=brand
            )
            product.save()

            ProductImage.objects.create(
                product=product,
                url=row['imagen'],
                width=600,
                height=600
            )

        # Crear lista de deseos
        wishlist = Wishlist.objects.create(user=user)
        for product in Product.objects.all()[:10]:
            wishlist.products.add(product)
            

        self.stdout.write(self.style.SUCCESS('Database populated successfully!'))

# python manage.py populate_shop data/products.csv

