import random
from django.core.management.base import BaseCommand
from apps.shop.models import Category, Brand, Product, ProductImage
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta


class Command(BaseCommand):
    help = "Seed the database with sample data for production"

    def handle(self, *args, **kwargs):
        self.stdout.write("Seeding database...")

        # Categories
        cats = {}
        for name, slug in [
            ("Tecnología", "tecnologia"),
            ("Deportes", "deportes"),
            ("Hogar", "hogar"),
            ("Ropa", "ropa"),
            ("Accesorios", "accesorios"),
            ("Electrodomésticos", "electrodomesticos"),
            ("Belleza", "belleza"),
            ("Juguetes", "juguetes"),
        ]:
            c, _ = Category.objects.get_or_create(slug=slug, defaults={"name": name})
            cats[slug] = c

        # Brands
        brands = {}
        for name, slug in [
            ("Nike", "nike"),
            ("Adidas", "adidas"),
            ("Samsung", "samsung"),
            ("Apple", "apple"),
            ("LG", "lg"),
            ("Sony", "sony"),
            ("Xiaomi", "xiaomi"),
            ("Bosch", "bosch"),
        ]:
            b, _ = Brand.objects.get_or_create(slug=slug, defaults={"name": name})
            brands[slug] = b

        # Product images
        imgs = [
            "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=600&h=600&fit=crop",
            "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=600&h=600&fit=crop",
            "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=600&h=600&fit=crop",
            "https://images.unsplash.com/photo-1585386959984-a4155224a1ad?w=600&h=600&fit=crop",
            "https://images.unsplash.com/photo-1491553895911-0055eca6402d?w=600&h=600&fit=crop",
            "https://images.unsplash.com/photo-1560343090-f0409e92791a?w=600&h=600&fit=crop",
            "https://images.unsplash.com/photo-1526170375885-4d8ecf77b99f?w=600&h=600&fit=crop",
            "https://images.unsplash.com/photo-1572569511254-d8f925fe2cbb?w=600&h=600&fit=crop",
        ]

        # Products
        products = [
            ("iPhone 15 Pro Max 256GB", "iphone-15-pro-max", 6999000, 15, "tecnologia", "apple", True, True, True),
            ("Samsung Galaxy S24 Ultra", "samsung-galaxy-s24", 5499000, 10, "tecnologia", "samsung", True, True, False),
            ('MacBook Air M3 15"', "macbook-air-m3", 7999000, 0, "tecnologia", "apple", True, False, True),
            ("Audífonos Sony WH-1000XM5", "sony-wh1000xm5", 1199000, 20, "tecnologia", "sony", False, True, False),
            ("Xiaomi Redmi Note 13 Pro", "redmi-note-13", 1299000, 25, "tecnologia", "xiaomi", True, True, False),
            ('Smart TV LG 55" OLED', "lg-55-oled", 3499000, 12, "tecnologia", "lg", False, True, True),
            ("Nike Air Max 270", "nike-air-max-270", 459000, 30, "deportes", "nike", True, True, False),
            ("Adidas Ultraboost 23", "adidas-ultraboost", 599000, 15, "deportes", "adidas", True, False, True),
            ("Camiseta Colombia 2024", "camiseta-colombia", 289000, 0, "ropa", "nike", True, True, False),
            ("Jeans Levi's 501 Classic", "levis-501", 349000, 10, "ropa", "nike", False, True, False),
            ("Reloj Casio G-Shock", "casio-gshock", 599000, 0, "accesorios", "sony", True, True, False),
            ('Mochila Samsonite 15.6"', "samsonite-mochila", 459000, 20, "accesorios", "samsung", False, False, True),
            ("Aspiradora Bosch BSG7", "bosch-aspiradora", 1299000, 10, "hogar", "bosch", False, True, False),
            ("Licuadora Oster 10 Velocidades", "oster-licuadora", 299000, 15, "hogar", "bosch", True, True, False),
            ("Set de Cocina T-fal 10 Piezas", "tfal-cocina", 459000, 0, "hogar", "bosch", False, False, True),
            ("Crema Hidratante Neutrogena", "neutrogena-crema", 45000, 25, "belleza", "samsung", True, True, False),
            ("Perfume Carolina Herrera 212", "carolina-212", 299000, 10, "belleza", "samsung", False, True, True),
            ("Lego City Space Set", "lego-city-space", 299000, 0, "juguetes", "samsung", True, False, True),
            ("PlayStation 5 Slim Digital", "ps5-slim", 1899000, 5, "tecnologia", "sony", True, True, True),
            ("Funko Pop Marvel Spider-Man", "funko-spiderman", 89000, 0, "juguetes", "samsung", True, True, False),
            ('Bicicleta MTB 26" Toroid', "toroid-mtb", 899000, 10, "deportes", "nike", False, True, False),
            ("Impresora HP Smart Tank 515", "hp-smart-tank", 699000, 15, "tecnologia", "samsung", True, False, False),
            ("Plancha a Vapor Philips", "philips-plancha", 189000, 20, "hogar", "samsung", False, True, False),
            ("Tenis Adidas Runfalcon 4", "adidas-runfalcon", 299000, 0, "deportes", "adidas", True, True, True),
            ("Tablet Samsung Galaxy Tab S9", "galaxy-tab-s9", 2499000, 10, "tecnologia", "samsung", True, False, True),
        ]

        for name, slug, price, disc, cat, brand, is_new, is_top, is_feat in products:
            p, created = Product.objects.get_or_create(
                slug=slug,
                defaults={
                    "name": name,
                    "description": f"Descripcion del producto {name}. Alta calidad y garantia.",
                    "price": price,
                    "discount": disc,
                    "discount_end_date": timezone.now() + timedelta(days=30) if disc > 0 else None,
                    "stock": random.randint(5, 50),
                    "is_new": is_new,
                    "is_top": is_top,
                    "is_featured": is_feat,
                    "ratings": round(random.uniform(3.5, 5.0), 2),
                    "reviews_count": random.randint(5, 200),
                    "category": cats.get(cat),
                    "brand": brands.get(brand),
                },
            )
            if created:
                for _ in range(3):
                    ProductImage.objects.create(product=p, url=random.choice(imgs))

        # Demo user
        u, created = User.objects.get_or_create(
            username="demo",
            defaults={"email": "demo@demo.com", "first_name": "Manuel", "last_name": "Forero"},
        )
        if created:
            u.set_password("demo1234")
            u.save()

        self.stdout.write(
            self.style.SUCCESS(
                f"Done! {Product.objects.count()} products, "
                f"{Category.objects.count()} categories, "
                f"{Brand.objects.count()} brands"
            )
        )
