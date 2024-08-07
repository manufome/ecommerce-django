from django.core.management.base import BaseCommand
from apps.shop.models import Category, Brand, Product, ProductImage, Wishlist
from django.contrib.auth.models import User
import pandas as pd
import random
import os

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

        self.stdout.write("Starting to populate the database...")

        os.system('python manage.py clear_shop')
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

        # Crear productos
        for _, row in data.iterrows():
            category = subcategory_objs[row['subcategoria']]
            brand = random.choice(list(brand_objs.values()))
            product = Product(
                name=row['producto'],
                slug=row['producto'].lower().replace(' ', '-'),
                description=f"Descripción de {row['producto']}",
                price = int(row['precio'].split(' ')[1].replace('.', '').strip()),
                discount=random.randint(0, 25),
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
                url=f'https://via.placeholder.com/600x600.png?text={product.name}',
                width=600,
                height=600
            )

        # Crear lista de deseos
        wishlist = Wishlist.objects.create(user=user)
        for product in Product.objects.all()[:10]:
            wishlist.products.add(product)
            

        self.stdout.write(self.style.SUCCESS('Database populated successfully!'))

# python manage.py populate_shop data/products.csv

