from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from apps.shop.models import Product, Category, ProductImage
from apps.orders.models import Order
from apps.orders.choices import PaymentMethod

User = get_user_model()

class OrderTests(APITestCase):
    def setUp(self):
        self.orders_url = '/api/v1/orders/orders/'
        
        # Create User
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword123'
        )
        self.client.force_authenticate(user=self.user)
        
        # Create Category and Product
        self.category = Category.objects.create(name='Test Category', slug='test-category')
        self.product = Product.objects.create(
            name='Test Product',
            slug='test-product',
            category=self.category,
            price=100.00,
            stock=10
        )
        ProductImage.objects.create(product=self.product, url='http://example.com/img.jpg')
        
        # Address Data
        self.address_data = {
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'test@example.com',
            'phone': '1234567890',
            'locality': 'CHA', # Chapinero
            'street_type': 'CL', # Calle
            'street_value': '79a',
            'number': '123',
            'complement': 'Apt 401'
        }

    def test_create_order(self):
        """
        Ensure we can create an order and stock is deducted.
        """
        payload = {
            'address': self.address_data,
            'products': [
                {
                    'product_id': self.product.id,
                    'qty': 2
                }
            ],
            'payment_method': PaymentMethod.CASH_ON_DELIVERY,
            'notes': 'Test order'
        }
        
        response = self.client.post(self.orders_url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Verify Order Created
        self.assertEqual(Order.objects.count(), 1)
        order = Order.objects.first()
        self.assertEqual(order.user, self.user)
        self.assertEqual(order.notes, 'Test order')
        
        # Verify Stock Deducted
        self.product.refresh_from_db()
        self.assertEqual(self.product.stock, 8) # 10 - 2 = 8
