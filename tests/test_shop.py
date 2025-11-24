from rest_framework.test import APITestCase
from rest_framework import status
from apps.shop.models import Product, Category, ProductImage

class ShopTests(APITestCase):
    def setUp(self):
        self.home_url = '/api/v1/shop/home/'
        
        # Create Category
        self.category = Category.objects.create(name='Test Category', slug='test-category')
        
        # Create Products
        # Best Selling (is_top=True)
        p1 = Product.objects.create(
            name='Best Seller',
            slug='best-seller',
            category=self.category,
            price=100.00,
            stock=10,
            is_top=True,
            discount=10
        )
        ProductImage.objects.create(product=p1, url='http://example.com/img1.jpg')
        
        # Featured (is_featured=True)
        p2 = Product.objects.create(
            name='Featured Product',
            slug='featured-product',
            category=self.category,
            price=200.00,
            stock=5,
            is_featured=True
        )
        ProductImage.objects.create(product=p2, url='http://example.com/img2.jpg')
        
        # On Sale (discount > 0)
        p3 = Product.objects.create(
            name='Sale Product',
            slug='sale-product',
            category=self.category,
            price=150.00,
            stock=20,
            discount=20
        )
        ProductImage.objects.create(product=p3, url='http://example.com/img3.jpg')

    def test_home_data(self):
        """
        Ensure HomeListView returns correct structure and data.
        """
        response = self.client.get(self.home_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        data = response.data
        
        # Check structure
        self.assertIn('best_selling', data)
        self.assertIn('featured', data)
        self.assertIn('latest', data)
        self.assertIn('on_sale', data)
        
        # Check logic
        # Best selling should contain the is_top product
        self.assertTrue(any(p['slug'] == 'best-seller' for p in data['best_selling']))
        
        # Featured should contain the is_featured product
        self.assertTrue(any(p['slug'] == 'featured-product' for p in data['featured']))
        
        # On sale should contain the product with discount
        self.assertTrue(any(p['slug'] == 'sale-product' for p in data['on_sale']))
