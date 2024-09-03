from rest_framework import serializers
from apps.orders.models import Address, Order, OrderItem, Payment, Coupon, Refund
from apps.shop.models import Product
from apps.shop.api.v1.serializers import ProductSerializer
from apps.orders.choices import PAYMENT_METHODS, ORDER_STATUS

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['first_name', 'last_name', 'email', 'phone', 'locality', 'street_type', 'street_value', 'number', 'complement']

class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    subtotal = serializers.SerializerMethodField()
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity', 'price', 'subtotal']

    def get_subtotal(self, obj):
        return obj.quantity * obj.price


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'

class CouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coupon
        fields = '__all__'

class RefundSerializer(serializers.ModelSerializer):
    class Meta:
        model = Refund
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True, read_only=True, source='orderitem_set')
    payments = PaymentSerializer(many=True, read_only=True, source='payment_set')
    refunds = RefundSerializer(many=True, read_only=True, source='refund_set')
    shipping_address = AddressSerializer(read_only=True)
    billing_address = AddressSerializer(read_only=True)
    items_count = serializers.SerializerMethodField()
    status = serializers.CharField(source='get_status_display')
    created_at = serializers.DateTimeField(format='%d %b %Y')

    class Meta:
        model = Order
        fields = '__all__'

    def get_items_count(self, obj):
        return sum(item.quantity for item in obj.orderitem_set.all())

class OrderItemCreateSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField(write_only=True)
    qty = serializers.IntegerField(write_only=True)

    class Meta:
        model = OrderItem
        fields = ['product_id', 'qty']

class OrderCreateSerializer(serializers.ModelSerializer):
    address = AddressSerializer()
    products = OrderItemCreateSerializer(many=True, write_only=True)
    payment_method = serializers.ChoiceField(choices=PAYMENT_METHODS)
    notes = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = Order
        fields = ['address', 'products', 'payment_method', 'notes']

    def create(self, validated_data):
        user = self.context['request'].user
        address_data = validated_data.pop('address')
        products_data = validated_data.pop('products')
        payment_method = validated_data.pop('payment_method')
        notes = validated_data.pop('notes', '')
        
        existing_address = Address.objects.filter(user=user, **address_data).first()
        if existing_address:
            address = existing_address
        else:
            address = Address.objects.create(user=user, **address_data)
        
        order = Order.objects.create(user=user, billing_address=address, shipping_address=address, status='P')

        total_amount = 0
        for product_data in products_data:
            product = Product.objects.get(id=product_data['product_id'])
            print('product', product)
            quantity = product_data['qty']
            price = product.get_display_price()[0]
            OrderItem.objects.create(order=order, product=product, quantity=quantity, price=price)
            total_amount += price * quantity

        Payment.objects.create(order=order, amount=total_amount, payment_method=payment_method, status='P')

        if notes:
            order.notes = notes
            order.save()

        return order
    

    # class Order(models.Model):
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    # status = models.CharField(max_length=1, choices=ORDER_STATUS)
    # created_at = models.DateTimeField(auto_now_add=True)
    # billing_address = models.ForeignKey(Address, related_name='billing_address', on_delete=models.SET_NULL, null=True)
    # shipping_address = models.ForeignKey(Address, related_name='shipping_address', on_delete=models.SET_NULL, null=True)
    # notes = models.TextField(blank=True)