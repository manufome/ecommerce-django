# Your custom management commands go here.
from django.core.management.base import BaseCommand
from faker import Faker
from apps.shop.models import Category, Brand, Product, ProductImage, Wishlist
from django.contrib.auth.models import User
from mptt.exceptions import InvalidMove
from mptt.utils import tree_item_iterator
import random


class Command(BaseCommand):
    help = "Populate the shop with some fake data"

    def handle(self, *args, **kwargs):
        fake = Faker()
        categories = []
        brands = []
        user = User.objects.first()

        for _ in range(5):
            category = Category(name=fake.word(), slug=fake.slug())
            category.save()
            categories.append(category)

        for _ in range(5):
            brand = Brand(name=fake.word(), slug=fake.slug())
            brand.save()
            brands.append(brand)

        for _ in range(100):
            product = Product(
                name=fake.sentence(),
                slug=fake.slug(),
                description=fake.text(),
                price=fake.random_int(10, 1000),
                discount=fake.random_int(0, 50),
                stock=fake.random_int(0, 100),
                is_new=fake.boolean(),
                is_top=fake.boolean(),
                is_featured=fake.boolean(),
                ratings=fake.random_int(0, 5),
                reviews_count=fake.random_int(0, 100),
                category=fake.random_element(categories),
                brand=fake.random_element(brands),
            )
            product.save()

            for _ in range(3):
                ProductImage(
                    product=product,
                    url=fake.image_url(),
                ).save()

        for item in tree_item_iterator(Category.objects.all()):
            try:
                item.move_to(random.choice(categories))
            except InvalidMove:
                pass
        
        Wishlist(
            user=user,
            products=Product.objects.all()[:10]
        ).save()


        self.stdout.write(self.style.SUCCESS("Successfully populated the shop with fake data"))