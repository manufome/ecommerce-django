from django.core.management.base import BaseCommand
from apps.shop.models import Category, Brand, Product, ProductImage, Wishlist

class Command(BaseCommand):
    help = "Clear the shop"

    def handle(self, *args, **kwargs):
        ProductImage.objects.all().delete()
        Product.objects.all().delete()
        Category.objects.all().delete()
        Brand.objects.all().delete()
        Wishlist.objects.all().delete()
        self.stdout.write(self.style.SUCCESS("Shop cleared!"))

